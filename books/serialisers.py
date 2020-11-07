from rest_framework import serializers

from books.models import Book


class BooksSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publication_date",
            "page_count",
            "lang",
            "thumbnail",
            "isbn10",
            "isbn13",
        ]
