"""stnbooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import routers

from books.views import ApiBooksList
from books.views import BookAddView
from books.views import BookEditView
from books.views import BookImportView
from books.views import BooksListView

router = routers.SimpleRouter()
router.register(r"api", ApiBooksList)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", BooksListView.as_view(), name="books"),
    path("add", BookAddView.as_view(), name="book-add"),
    path("edit/<int:pk>", BookEditView.as_view(), name="book-edit"),
    path("import", BookImportView.as_view(), name="book-import"),
    path("", include(router.urls)),
]
