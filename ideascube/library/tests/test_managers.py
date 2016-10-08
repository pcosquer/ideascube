import pytest

from ..models import Book
from .factories import BookSpecimenFactory

pytestmark = pytest.mark.django_db


def test_available_should_return_only_book_with_specimen(book, specimen):
    books = Book.objects.available()
    assert specimen.item in books
    assert book not in books


def test_available_should_be_chainable(book, specimen):
    specimen1 = BookSpecimenFactory(barcode='321654')
    specimen2 = BookSpecimenFactory(barcode='987456')
    books = Book.objects.available().filter(specimens__barcode='321654')
    assert specimen1.item in books
    assert specimen2.item not in books


def test_objects_should_return_all_books(book, specimen):
    books = Book.objects.all()
    assert specimen.item in books
    assert book in books
