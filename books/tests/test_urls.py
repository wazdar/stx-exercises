from django.test import SimpleTestCase
from django.urls import resolve
from django.urls import reverse

from books.views import BookAdd
from books.views import BooksList


class TestUrls(SimpleTestCase):
    def test_book_list_resolves(self):
        url = reverse("book-list")
        self.assertEquals(resolve(url).func.view_class, BooksList)

    def test_book_add_resolves(self):
        url = reverse("book-add")
        self.assertEquals(resolve(url).func.view_class, BookAdd)
