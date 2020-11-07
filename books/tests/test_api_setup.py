import random

from django.urls import reverse
from rest_framework.test import APITestCase

from books.models import Author
from books.models import Book

BOOKS = [
    {
        "title": "First book",
        "authors": ["First Author", "Second Author"],
        "page_count": random.randint(100, 1000),
        "lang": "pl",
        "publication_date": "2001-01-01",
        "thumbnail": "http//www.google.pl",
    },
    {
        "title": "Second book",
        "authors": ["Third Author", "Second Author"],
        "page_count": random.randint(100, 1000),
        "lang": "pl",
        "publication_date": "2002-01-01",
        "thumbnail": "http//www.google.pl",
    },
    {
        "title": "Third book",
        "authors": ["Fourth Author", "Third Author"],
        "page_count": random.randint(100, 1000),
        "lang": "pl",
        "publication_date": "2003-01-01",
        "thumbnail": "http//www.google.pl",
    },
]


class TestSetUp(APITestCase):
    def setUp(self):
        self.book_list_url = reverse("book-list")
        self.raw_data = BOOKS

        for book in self.raw_data:
            b = Book.objects.create(
                title=book["title"],
                page_count=book["page_count"],
                lang=book["lang"],
                publication_date=book["publication_date"],
                thumbnail=book["thumbnail"],
            )
            for auth in book["authors"]:
                author, created = Author.objects.get_or_create(name=auth)
                b.author.add(author)
            b.save()

        self.books = Book.objects.all()
        return super(TestSetUp, self).setUp()

    def tearDown(self):
        return super().tearDown()
