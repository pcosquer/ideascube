import pytest

from django.contrib.auth import get_user_model
from django.db import models

from ..models import JSONField, User
from .factories import UserFactory

pytestmark = pytest.mark.django_db


def test_get_short_name_should_return_short_name():
    user = UserFactory.build()
    assert user.get_short_name() == "Sankara"


def test_get_full_name_should_return_full_name():
    user = UserFactory.build()
    assert user.get_full_name() == "Thomas Sankara"


def test_create_user():
    model = get_user_model()
    user = model.objects.create_user('123456')
    assert user.pk is not None
    assert user.serial == '123456'


def test_create_superuser():
    model = get_user_model()
    user = model.objects.create_superuser('123456', 'passw0rd')
    assert user.pk is not None
    assert user.serial == '123456'
    assert user.is_staff


def test_list_users():
    model = get_user_model()
    model.objects.create_user('123456')
    model.objects.create_user('__system__')

    users = model.objects.all()
    assert [u.serial for u in users] == ['123456']

    users = model.objects.all(include_system_user=True)
    assert [u.serial for u in users] == ['__system__', '123456']

    systemuser = model.objects.get_system_user()
    assert systemuser.serial == '__system__'


def test_client_login(client, user):
    assert client.login(serial=user.serial, password='password')


def test_user_data_fields_should_return_labels_and_values(settings):
    settings.USER_DATA_FIELDS = ['short_name', 'ar_level']

    user = User(short_name='my name', ar_level=['u', 's'])
    fields = user.data_fields
    assert 'is_staff' not in fields
    assert str(fields['short_name']['value']) == 'my name'
    assert str(fields['short_name']['label']) == 'usual name'
    assert str(fields['ar_level']['value']) == 'Understood, Spoken'
    assert str(fields['ar_level']['label']) == 'Arabic knowledge'


class JSONModel(models.Model):
    class Meta:
        app_label = 'ideascube'

    data = JSONField()


@pytest.mark.parametrize(
    'value',
    [
        True,
        42,
        None,
        'A string',
        [1, 2, 3],
        {'foo': 'bar'}
    ],
    ids=[
        'boolean',
        'int',
        'none',
        'string',
        'list',
        'dict',
    ])
def test_json_field(value):
    obj = JSONModel(data=value)
    obj.save()
    assert JSONModel.objects.count() == 1

    obj = JSONModel.objects.first()
    assert obj.data == value
