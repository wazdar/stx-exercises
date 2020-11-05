from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=254)
    author = models.ManyToManyField("Author")
    publication_date = models.CharField(max_length=10)
    page_count = models.IntegerField(null=True, default=None)
    lang = models.CharField(max_length=2)
    thumbnail = models.URLField()
    isbn10 = models.CharField(max_length=10, default=None, null=True)
    isbn13 = models.CharField(max_length=13, default=None, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.title)


class Author(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)
