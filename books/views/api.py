from django_filters import rest_framework as filters
from rest_framework import viewsets

from books.models import Book
from books.serialisers import BooksSerializer


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    author = filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    lang = filters.CharFilter(lookup_expr="icontains")

    publication_date_from = filters.DateFilter(
        field_name="publication_date", lookup_expr="gte"
    )
    publication_date_to = filters.DateFilter(
        field_name="publication_date", lookup_expr="lte"
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "author__name",
            "lang",
        ]


class ApiBooksList(viewsets.ModelViewSet):
    serializer_class = BooksSerializer
    queryset = Book.objects.all()
    filterset_class = BookFilter
