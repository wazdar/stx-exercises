from django.test import TestCase
from django.urls import reverse

from books.models import Book


class TestImportFromGAPI(TestCase):
    def setUp(self):
        self.import_url = reverse("book-import")

    def test_book_import_GET(self):
        response = self.client.get(self.import_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/book_import.html")

    def test_book_import_POST_no_data(self):
        response = self.client.post(self.import_url)

        self.assertEqual(response.status_code, 400)

    def test_book_import_POST_with_data(self):
        query = {"title": "war"}
        response = self.client.post(self.import_url, query)

        self.assertEqual(response.status_code, 302)

        books = Book.objects.filter(title__icontains="war")
        self.assertEqual(len(books), 6)
