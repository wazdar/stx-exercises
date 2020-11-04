from django.test import TestCase

from books.models import Author
from books.models import Book


class TestModels(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="TestCase",
            publication_date="2020-11-05",
            isbn10="142674949X",
            isbn13="9781426749490",
            page_count=666,
            lang="EN",
            thumbnail="http://www.google.pl",
        )
        self.author1 = Author.objects.create(name="Test Author")
        self.book1.author.add(self.author1)
        self.book1.save()

    def test_author_is_assigned_to_book(self):
        self.assertEquals(self.book1.author.all().first(), self.author1)
