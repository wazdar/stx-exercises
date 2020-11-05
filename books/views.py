from datetime import datetime

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from books.forms import BookAddForm
from books.models import Author
from books.models import Book
from books.utility import ApiRequest


class BooksListView(ListView):
    model = Book
    context_object_name = "books"
    template_name = "books/book_list.html"
    paginate_by = 10

    def get_queryset(self):
        """
        Filtering list of Books
        :return:
        """
        books = Book.objects.all()
        query = self.request.GET
        if query != {}:
            try:
                if query["title"] != "":
                    books = books.filter(title__icontains=query["title"])
                if query["author"] != "":
                    books = books.filter(author__name__contains=query["author"])
                if query["lang"] != "":
                    books = books.filter(lang__contains=query["lang"])
                if query["date_start"] != "":
                    books = books.filter(publication_date__gte=query["date_start"])
                    if query - ["date_end"] != "":
                        books = books.filter(publication_date__lte=query["date_end"])

            except Exception as e:
                print(e)

        return books


class BookAddView(CreateView):
    model = Book
    form_class = BookAddForm
    template_name = "books/book_form.html"
    success_url = "book-list"

    def form_valid(self, form):
        """
        Create a new Book.
        :param form:
        :return:
        """
        try:
            book = Book.objects.create(
                title=form.data.get("title"),
                publication_date=datetime.strptime(
                    form.data.get("publication_date"), "%Y-%m-%d"
                ),
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


class BookEditView(UpdateView):
    model = Book
    form_class = BookAddForm
    template_name = "books/book_form.html"

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        initial["author"] = ", ".join(
            [author.name for author in self.object.author.all()]
        )
        return initial

    def form_valid(self, form):
        """
        Return update Book, and redirect to list
        :param form:
        :return:
        """
        try:
            book = self.object
            data = form.data
            book.title = data.get("title")
            book.publication_date = datetime.strptime(
                data.get("publication_date"), "%Y-%m-%d"
            )
            book.page_count = data.get("page_count")
            book.isbn10 = data.get("isbn10")
            book.isbn13 = data.get("isbn13")
            book.lang = data.get("lang")
            book.thumbnail = data.get("thumbnail")
            book.save()
            for auth in data.get("author").split(","):
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


class BookImportView(View):
    def get(self, request):
        """
        Form to importing data from google api.
        :param request:
        :return:
        """
        return render(request, "books/book_import.html")

    def post(self, request):
        """
        Importing data from google API
        :param request:
        :return:
        """
        query = request.POST.dict()
        api_request = ApiRequest(
            title=query["title"],
            author=query["author"],
            publisher=query["publisher"],
            subject=query["subject"],
            isbn=query["isbn"],
            lccn=query["lccn"],
            oclc=query["oclc"],
        )
        try:
            for data in api_request.get_data():
                try:
                    isbn10 = [a for a in data["isbn"] if a["type"] == "ISBN_10"][0][
                        "identifier"
                    ]
                except IndexError:
                    isbn10 = None
                try:
                    isbn13 = [a for a in data["isbn"] if a["type"] == "ISBN_13"][0][
                        "identifier"
                    ]
                except IndexError:
                    isbn13 = None

                book, book_created = Book.objects.update_or_create(
                    title=data["title"],
                    publication_date=data["publication_date"],
                    isbn10=isbn10,
                    isbn13=isbn13,
                    page_count=data["page_count"],
                    lang=data["lang"],
                    thumbnail=data["thumbnail"],
                )
                for auth in data["authors"]:
                    author, author_created = Author.objects.get_or_create(name=auth)
                    book.author.add(author)
            return redirect(reverse("book-list"))
        except Exception as e:
            print(e)
            return render(
                request,
                "books/book_import.html",
                {
                    "error": "Internal Error. Check data and try again.",
                },
            )
