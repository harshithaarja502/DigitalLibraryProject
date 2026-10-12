
from datetime import timedelta

from django.db import models
from django.utils import timezone


def default_due_date():
    return timezone.localdate() + timedelta(days=14)


class Author(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )
    isbn = models.CharField(max_length=20, unique=True)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Member(models.Model):
    full_name = models.CharField(max_length=150)
    member_id = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    joined_on = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"{self.full_name} ({self.member_id})"


class CirculationRecord(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="circulation_records"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="circulation_records"
    )
    issue_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(default=default_due_date)
    returned_on = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    @property
    def is_returned(self):
        return self.returned_on is not None

    @property
    def is_overdue(self):
        check_date = self.returned_on or timezone.localdate()
        return not self.is_returned and check_date > self.due_date

    def __str__(self):
        return f"{self.book.title} - {self.member.full_name}"
