from django.forms import ModelForm

from .models import Author
from .models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
        ]


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ["name"]
