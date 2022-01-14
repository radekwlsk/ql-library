from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

import pytest

from faker import config
from graphene.test import Client
from pytest_django.lazy_django import skip_if_no_django
from requests_mock import MockerCore
from rest_framework.test import APIRequestFactory

from config.schema import schema as default_schema

config.DEFAULT_LOCALE = "pl_PL"


@pytest.fixture(scope="session")
def faker_locale():
    return "pl_PL"


@pytest.fixture(scope="session")
def setup_view():
    """Returns function able to setup Django's view.

    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to ``reverse()``

    Examples
    ========
    `setup_view` should be used as normal pytest's fixture::

        def test_hello_view(setup_view):
            name = 'django'
            request = RequestFactory().get('/fake-path')
            view = HelloView(template_name='hello.html')
            view = setup_view(view, request, name=name)

            # Example test ugly dispatch():
            response = view.dispatch(view.request, *view.args, **view.kwargs)
    """

    def _inner_setup_view(view, request, *args, **kwargs):
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    return _inner_setup_view


@pytest.fixture(scope="session")
def api_setup_view():
    """Returns function able to setup DRF's view.

    Examples
    ========
    `api_setup_view` should be used as normal pytest's fixture::

        def test_profile_info_view(api_setup_view):
            request = HttpRequest()
            view = views.ProfileInfoView()
            view = api_setup_view(view, request, 'list')
            assert view.get_serializer_class() == view.serializer_class
    """

    def _inner_api_setup_view(view, request, action, *args, **kwargs):
        view.request = request
        view.action = action
        view.args = args
        view.kwargs = kwargs
        return view

    return _inner_api_setup_view


@pytest.fixture()
def api_rf():
    """APIRequestFactory instance"""
    skip_if_no_django()
    return APIRequestFactory()


@pytest.yield_fixture(scope="session")
def requests_mock():
    mock = MockerCore()
    mock.start()
    yield mock
    mock.stop()


@pytest.fixture
def gql_client(client, rf):
    def inner(user=None, schema=default_schema, **kwargs):
        if user is not None:
            client.force_login(user=user)
        else:
            user = AnonymousUser()
        request = rf.post(
            reverse("graphql"),
            content_type="application/json",
        )
        kwargs["context_value"] = request
        request.user = user
        gql_client = Client(schema, **kwargs)
        gql_client.user = user
        return gql_client

    return inner
