from django.db import models
from account.models import Account
from .utils import generate_isb


class PolyPhrase(models.Model):
    said_by = models.ForeignKey(
        Account,
        verbose_name='said by',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    phrase = models.CharField(
        verbose_name='phrase',
        max_length=150
    )

    def __str__(self):
        return f"phrase number {self.id}"


class BookCategory(models.Model):
    cat_id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        verbose_name='category name',
        max_length=50,
        null=False
    )
    abbrev = models.CharField(
        verbose_name='abbreviation',
        max_length=3,
        null=False
    )
    description = models.CharField(
        verbose_name='description',
        max_length=150,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(
        verbose_name='isbn',
        max_length=13,
        unique=True
    )
    title = models.CharField(
        verbose_name='title',
        max_length=30,
        null=False
    )
    categories = models.ManyToManyField(BookCategory)

    def __str__(self):
        return f"{self.isbn} - {self.title}"

    def get_pages(self):
        return self.bookpage_set.all().order_by('page_id')

    def save(self, *args, **kwargs):
        self.isbn = generate_isb()
        super().save(*args, **kwargs)


class BookPage(models.Model):
    page_id = models.AutoField(
        primary_key=True
    )
    content = models.TextField(
        verbose_name='page content',
        max_length=600,
        null=True
    )
    book = models.ForeignKey(Book, models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.page_id} page. from {self.book.title}"
