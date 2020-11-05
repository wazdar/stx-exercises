from django.test import Client
from django.test import TestCase
from django.urls import reverse

from books.models import Author
from books.models import Book


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("book-list")
        self.add_url = reverse("book-add")
        self.book = Book.objects.create(
            title="TestCase",
            publication_date="2020-11-05",
            isbn10="142674949X",
            isbn13="9781426749490",
            page_count=666,
            lang="EN",
            thumbnail="http://www.google.pl",
        )
        self.edit_url = reverse("book-edit", kwargs={"pk": 1})

    def test_books_list_GET(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_add_GET(self):
        response = self.client.get(self.add_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/book_form.html")

    def test_book_add_POST(self):
        response = self.client.post(
            self.add_url,
            {
                "title": "TestCase",
                "author": "Test Case",
                "publication_date": "2020-11-05",
                "isbn10": "142674949X",
                "isbn13": "9781426749490",
                "page_count": 666,
                "lang": "EN",
                "thumbnail": "http://www.google.pl",
            },
        )

        test_case = Book.objects.get(id=2)
        test_author = Author.objects.get(pk=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_case.title, "TestCase")
        self.assertEqual(test_author.name, "Test Case")

    def test_book_edit_GET(self):
        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books/book_form.html")

    def test_book_edit_GET_not_exist(self):
        url = reverse("book-edit", kwargs={"pk": 666})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_book_edit_POST(self):
        response = self.client.post(
            self.edit_url,
            {
                "title": "Edit",
                "author": "Edit Case",
                "publication_date": "2020-11-05",
                "isbn10": "142674949X",
                "isbn13": "9781426749490",
                "page_count": 666,
                "lang": "EN",
                "thumbnail": "http://www.google.pl",
            },
        )

        self.book.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book.title, "Edit")

    def test_book_edit_POST_no_data(self):
        response = self.client.post(self.edit_url, {})
        book = self.book
        self.book.refresh_from_db()

        self.assertEqual(self.book, book)
        self.assertNotEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "books/book_form.html")
