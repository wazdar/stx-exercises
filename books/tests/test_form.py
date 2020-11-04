from django.test import SimpleTestCase

from books.forms import BookForm


class TestForms(SimpleTestCase):
    def test_book_form_valid_no_data(self):
        form = BookForm(data={})
        self.assertFalse(form.is_valid())

        self.assertEquals(len(form.errors), 8)

    def test_book_form_valid_isbns_are_valid(self):
        form = BookForm(
            data={
                "title": "TestCase",
                "author": "Test Case",
                "publication_date": "2020-11-05",
                "isbn10": "142674949X",
                "isbn13": "9781426749490",
                "page_count": 666,
                "lang": "EN",
                "thumbnail": "http://www.google.pl",
            }
        )

        self.assertTrue(form.is_valid())

    def test_book_form_valid_isbn10_is_invalid(self):
        form = BookForm(
            data={
                "title": "TestCase",
                "author": "Test Case",
                "publication_date": "2020-11-05",
                "isbn10": "142374949X",
                "isbn13": "9781426749490",
                "page_count": 666,
                "lang": "EN",
                "thumbnail": "http://www.google.pl",
            }
        )

        self.assertFalse(form.is_valid())

    def test_book_valid_isbn13_is_invalid(self):
        form = BookForm(
            data={
                "title": "TestCase",
                "author": "Test Case",
                "publication_date": "2020-11-05",
                "isbn10": "142674949X",
                "isbn13": "9780026749490",
                "page_count": 666,
                "lang": "EN",
                "thumbnail": "http://www.google.pl",
            }
        )

        self.assertFalse(form.is_valid())
