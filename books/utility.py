import requests
from django.utils.crypto import get_random_string


class ApiRequest:
    def __init__(
        self,
        title=None,
        author=None,
        publisher=None,
        subject=None,
        isbn=None,
        lccn=None,
        oclc=None,
    ):
        self.url = "https://www.googleapis.com/books/v1/volumes?q="
        self.title = title
        self.author = author
        self.publisher = publisher
        self.subject = subject
        self.isbn = isbn
        self.lccn = lccn
        self.oclc = oclc

        self.query = self.__make_query()

    def __make_query(self):
        """
        Making query from class.
        :return:
        """
        query = ""
        query += (
            f"intitle:{self.title}"
            if self.title is not None and self.title != ""
            else ""
        )
        query += (
            f"+inauthor:{self.author}"
            if self.author is not None and self.author != ""
            else ""
        )
        query += (
            f"+inpublisher:{self.publisher}"
            if self.publisher is not None and self.publisher != ""
            else ""
        )
        query += (
            f"+subject:{self.subject}"
            if self.subject is not None and self.subject != ""
            else ""
        )
        query += (
            f"+isbn:{self.isbn}" if self.isbn is not None and self.isbn != "" else ""
        )
        query += (
            f"+lccn:{self.lccn}" if self.lccn is not None and self.lccn != "" else ""
        )
        query += (
            f"+oclc:{self.oclc}" if self.oclc is not None and self.oclc != "" else ""
        )
        return query

    def __make_request(self):
        """
        Do request and return JSON.
        :return:
        """
        request = requests.get(self.url + self.query)
        return request.json()

    def get_data(self):
        """
        Return list of books from Google API.
        :return:
        """
        raw_data = self.__make_request()
        data = []
        for book in raw_data["items"]:
            try:
                data.append(
                    {
                        "title": book["volumeInfo"]["title"],
                        "authors": book["volumeInfo"]["authors"],
                        "publication_date": book["volumeInfo"]["publishedDate"],
                        "isbn": book["volumeInfo"]["industryIdentifiers"],
                        "page_count": book["volumeInfo"]["pageCount"]
                        if book["volumeInfo"]["pageCount"]
                        else None,
                        "thumbnail": book["volumeInfo"]["imageLinks"]["smallThumbnail"],
                        "lang": book["volumeInfo"]["language"],
                    }
                )
            except Exception as e:
                print(e)
        return data


def generate_secret_key(env_file_name):
    """
    Create secret_key and write to .env file.
    :param env_file_name:
    :return:
    """
    env_file = open(env_file_name, "w+")
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    generated_secret_key = get_random_string(50, chars)
    env_file.write(f"SECRET_KEY = '{generated_secret_key}'\n")
    env_file.close()


def generate_debug_mode(env_file_name, debug_mode=False):
    """
    Add to .env file debug mode settings.
    :param env_file_name:
    :param debug_mode:
    :return:
    """
    env_file = open(env_file_name, "a")
    env_file.write(f"DEBUG = {debug_mode}\n")
    env_file.close()
