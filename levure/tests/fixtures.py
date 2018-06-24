#-*- coding:utf-8 -*-
#pylint:disable=missing-docstring,unused-import,no-member,line-too-long,no-name-in-module,redefined-outer-name
import collections
import json
import random
import string
import mock
import pytest
import farine.settings
from farine.tests.fixtures import amqp_factory, message_factory, queue_factory
from kubernetes.client.rest import ApiException

@pytest.fixture(autouse=True)
def settings(tmpdir):
    """
    auto load the settings.
    """
    farine.settings.load()
    farine.settings.levure['ca_file'] = str(tmpdir)
    farine.settings.levure['cert_file'] = str(tmpdir)
    farine.settings.levure['key_file'] = str(tmpdir)

def gen_str(length=15):
    """
    Generate a string of `length`.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in xrange(length))

@pytest.fixture()
def levure():
    """
    Network service fixture.
    """
    import levure.service
    return levure.service.Levure()

@pytest.fixture()
def request_factory():
    def factory(status, data, reason=''):
        import kubernetes.client.rest
        resp = mock.Mock()
        resp.status = status
        resp.data = json.dumps(data)
        resp.reason = reason
        return kubernetes.client.rest.RESTResponse(resp)
    return factory
