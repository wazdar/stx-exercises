from datetime import datetime

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import ListView

from books.forms import BookForm
from books.models import Author
from books.models import Book


class BooksList(ListView):
    model = Book
    context_object_name = "books"
    template_name = "books/book_list.html"
    paginate_by = 10


class BookAdd(CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = "book-list"

    def form_valid(self, form):
        try:
            book = Book.objects.create(
                title=form.data.get("title"),
                publication_date=datetime.strptime("2020-11-05", "%Y-%m-%d"),
                page_count=form.data.get("page_count"),
                isbn10=form.data.get("isbn10"),
                isbn13=form.data.get("isbn13"),
                lang=form.data.get("lang"),
                thumbnail=form.data.get("thumbnail"),
            )
            for auth in form.data.get("author").split(","):
                author, author_created = Author.objects.get_or_create(
                    name=auth.lstrip(" ")
                )
                book.author.add(author)
            return redirect(reverse("book-list"))
        except Exception as e:
            print(e)
            return render(
                self.request,
                self.template_name,
                {
                    "error": "Internal Error. Check data and try again.",
                    "form": self.form_class,
                },
            )
