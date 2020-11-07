from django.test import SimpleTestCase
from django.urls import resolve
from django.urls import reverse

from books.views import BookAddView
from books.views import BookEditView
from books.views import BookImportView
from books.views import BooksListView


class TestUrls(SimpleTestCase):
    def test_book_list_resolves(self):
        url = reverse("books")
        self.assertEquals(resolve(url).func.view_class, BooksListView)

    def test_book_add_resolves(self):
        url = reverse("book-add")
        self.assertEquals(resolve(url).func.view_class, BookAddView)

    def test_book_edit_resolves(self):
        url = reverse("book-edit", kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, BookEditView)

    def test_book_import_resolves(self):
        url = reverse("book-import")
        self.assertEquals(resolve(url).func.view_class, BookImportView)
