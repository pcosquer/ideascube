from __future__ import unicode_literals

from django.conf import settings

from .exceptions import (
    NoSuchConfigurationKeyError,
    NoSuchConfigurationNamespaceError,
)


# Please try and keep this stored in alphabetical order
REGISTRY = {
    # 'namespace': {
    #     'key': {
    #         'summary': 'Help text for the management command',
    #         'pretty_type': 'Pretty type(s) for the management command',
    #         'type': str,
    #         'default': 'Default value',
    #     },
    # },
    'server': {
        'site-name': {
            'summary': 'The pretty name of the server, as seen by users of '
                       'the web interface.',
            'pretty_type': 'A string',
            'type': str,
            'default': getattr(settings, 'IDEASCUBE_NAME', 'Ideas Cube'),
        },
    },
    'home-page': {
        'displayed-package-ids': {
            'summary': 'The list of package-related cards displayed on the '
                       'home page.',
            'pretty_type': 'A list of strings',
            'type': list,
            'default': [],
        },
    },
}


def get_all_namespaces():
    yield from sorted(REGISTRY)


def get_config_data(namespace, key):
    try:
        namespace_registry = REGISTRY[namespace]

    except KeyError:
        raise NoSuchConfigurationNamespaceError(namespace)

    try:
        return namespace_registry[key]

    except KeyError:
        raise NoSuchConfigurationKeyError(namespace, key)


def get_default_value(namespace, key):
    return get_config_data(namespace, key)['default']


def get_expected_type(namespace, key):
    return get_config_data(namespace, key)['type']


def get_namespaced_configs(namespace):
    try:
        namespace_registry = REGISTRY[namespace]

    except KeyError:
        raise NoSuchConfigurationNamespaceError(namespace)

    yield from sorted(namespace_registry)
