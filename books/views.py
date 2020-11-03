from django.views.generic import CreateView
from django.views.generic import ListView

from books.forms import BookForm
from books.models import Book


class BooksList(ListView):
    model = Book
    context_object_name = "books"
    template_name = "books/list.html"
    paginate_by = 1


class BookAdd(CreateView):
    model = Book
    form_class = BookForm
