import isbnlib
from django import forms
from django.core.exceptions import ValidationError

from .models import Book


class BookForm(forms.ModelForm):
    author = forms.CharField(
        label="Author",
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "publication_date",
            "isbn10",
            "isbn13",
            "page_count",
            "lang",
            "thumbnail",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "publication_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "page_count": forms.NumberInput(attrs={"class": "form-control"}),
            "lang": forms.TextInput(attrs={"class": "form-control"}),
            "thumbnail": forms.URLInput(attrs={"class": "form-control"}),
            "isbn10": forms.TextInput(attrs={"class": "form-control"}),
            "isbn13": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_isbn10(self):
        """
        Function to validate isbn-10
        """
        if not isbnlib.is_isbn10(self.data["isbn10"]):
            raise ValidationError("ISBN-10 is not valid!")
        return True

    def clean_isbn13(self):
        """
        Function to validate isbn-10
        """
        if not isbnlib.is_isbn13(self.data["isbn13"]):
            raise ValidationError("ISBN-13 is not valid!")
        return True

    def is_valid(self):
        """
        Function to css class if field in form have validation error
        """
        result = super().is_valid()
        for field in self.fields if "__all__" in self.errors else self.errors:
            attrs = self.fields[field].widget.attrs
            attrs.update({"class": attrs.get("class", "") + " is-invalid"})
        return result
