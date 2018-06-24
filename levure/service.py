#-*- coding:utf-8 -*-
"""
Manage namespaces/services.
Listen to pods/deployments events.

The operations are idempotent.
"""
#pylint:disable=line-too-long
import logging
from kubernetes import client
from kubernetes.client.rest import ApiException
import farine.amqp
import farine.settings

LOGGER = logging.getLogger(__name__)

class Levure(object):
    """
    Service which contains the event loops to manage the wrapper objects:
    * delete-namespace
    * create-namespace
    * create-service
    * delete-service
    """

    def __init__(self):
        """
        Create a configurated client to the orchestration system.
        """
        configuration = client.Configuration()
        configuration.host = farine.settings.levure['api_host']
        configuration.ssl_ca_cert = farine.settings.levure['api_ca_file']
        #configuration.cert_file = farine.settings.levure['api_cert_file']
        #configuration.key_file = farine.settings.levure['api_key_file']
        client.Configuration.set_default(configuration)

    @farine.amqp.consume(exchange='namespace', routing_key='delete')
    def delete_namespace(self, body, message):
        """
        Listen to the `exchange` namespace
        | and delete the namespace accordly to the messages.
        | Idempotent.
        :param body: the namespace's name to delete.
        :type body: dict
        :param message: The raw message.
        :type message: kombu.message.Message
        :rtype: bool
        """
        v1 = client.CoreV1Api()
        #Idempotent
        try:
            v1.delete_namespace(name=body['namespace'], body=client.V1DeleteOptions())
        except ApiException as e:
            LOGGER.error(e)
            if e.status not in (404, 409):# 404 == Not found, 409 == Conflict => already deleting
                raise
        message.ack()
        return True

    @farine.amqp.consume(exchange='namespace', routing_key='create')
    def create_namespace(self, body, message):
        """
        Listen to the `exchange` namespace,
        | and create the namespace accordly to the messages.
        | Idempotent.

        :param body: The message's content.
        :type body: dict
        :param message: The namespace to create.
        :type message: kombu.message.Message
        :returns: The creation state
        :rtype: bool
        """
        payload = client.V1Namespace()
        payload.metadata = client.V1ObjectMeta(name=body['namespace'])
        core_v1 = client.CoreV1Api()
        network_v1 = client.NetworkingV1Api()
        policy = client.V1NetworkPolicy(api_version='networking.k8s.io/v1', kind='NetworkPolicy')
        policy.metadata = client.V1ObjectMeta(name='deny-namespaces-traffic', namespace=body['namespace'])
        policy.spec = client.V1NetworkPolicySpec(
                pod_selector=client.V1LabelSelector(match_labels={}),
                ingress=[client.V1NetworkPolicyIngressRule(_from=[client.V1NetworkPolicyPeer(pod_selector=client.V1LabelSelector())])]
        )
        #Idempotent
        try:
            core_v1.create_namespace(payload)
            core_v1.patch_namespaced_service_account('default', body['namespace'], {'automount_service_account_token': False})
            network_v1.create_namespaced_network_policy(body['namespace'], policy)
        except ApiException as e:
            LOGGER.error(e)
            if e.status != 409:# 409 == Conclict => Already exist
                raise
        message.ack()
        return True
