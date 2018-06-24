#-*- coding:utf-8 -*-
"""
Unit tests for the service module.
"""
#pylint:disable=wildcard-import,unused-wildcard-import,redefined-outer-name,unused-argument,invalid-name,line-too-long
import logging
from .fixtures import *

def test_create_namespace_ok(levure, request_factory):
    """
    Try to create a namespace:
    must succeed.
    """
    body = {'namespace': 'test'}
    request = request_factory(200, {})
    with mock.patch('kubernetes.client.rest.RESTClientObject.request', mock.Mock(return_value=request)) as namespaces:
        assert levure.create_namespace(body, mock.Mock())

def test_create_namespace_idempotent_409(levure, request_factory):
    """
    Try to create a namespace that already exist:
    must succeed anyway.
    """
    body = {'namespace': 'test'}
    request = request_factory(409, {})
    with mock.patch('kubernetes.client.rest.RESTClientObject.request', mock.Mock(return_value=request)) as namespaces:
        namespaces.side_effect = ApiException(status=409)
        assert levure.create_namespace(body, mock.Mock())

def test_delete_namespace_ok(levure, request_factory):
    """
    Try to delete a namespace that exist once:
    must succeed.
    """
    body = {'namespace': 'test'}
    request = request_factory(200, {})
    with mock.patch('kubernetes.client.rest.RESTClientObject.request', mock.Mock(return_value=request)) as namespaces:
        assert levure.delete_namespace(body, mock.Mock())

def test_delete_namespace_idempotent_409(levure, request_factory):
    """
    Try to delete a namespace that is already deleting:
    must succeed anyway.
    """
    body = {'namespace': 'test'}
    request = request_factory(409, {})
    with mock.patch('kubernetes.client.rest.RESTClientObject.request', mock.Mock(return_value=request)) as namespaces:
        namespaces.side_effect = ApiException(409)
        assert levure.delete_namespace(body, mock.Mock())

def test_delete_namespace_idempotent_404(levure, request_factory):
    """
    Try to delete a namespace that does not exist:
    must succeed anyway.
    """
    body = {'namespace': 'test'}
    request = request_factory(404, {})
    with mock.patch('kubernetes.client.rest.RESTClientObject.request', mock.Mock(return_value=request)) as namespaces:
        namespaces.side_effect = ApiException(404)
        assert levure.delete_namespace(body, mock.Mock())
