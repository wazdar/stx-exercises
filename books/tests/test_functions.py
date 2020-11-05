from django.http import QueryDict
from django.test import TestCase

from books.templatetags.books_pagination import get_book_url


class TestGeneratePaginationUrl(TestCase):
    def test_pagination_link_no_data(self):
        test_data = QueryDict({})

        result = get_book_url(test_data)

        self.assertRaises(Exception, result)

    def test_pagination_link_only_page_number(self):
        test_data = QueryDict("")

        self.assertEqual(get_book_url(test_data, 1), "?page=1")
        self.assertEqual(get_book_url(test_data, 2), "?page=2")

        self.assertRaises(Exception, get_book_url(test_data, 0))

    def test_pagination_link_with_data(self):
        test_data = QueryDict("", mutable=True)
        test_data.update(
            {"page": 1, "title": "Test Case", "author": "Test Author", "lang": "PL"}
        )
        should_be = "?page=1&title=Test Case&author=Test Author&lang=PL"

        result = get_book_url(test_data)

        self.assertEqual(result, should_be)
