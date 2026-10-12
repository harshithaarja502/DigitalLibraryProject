
from datetime import timedelta
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from .models import Book, Member, CirculationRecord


FINE_PER_DAY = Decimal("5.00")


def home(request):
    query = request.GET.get("q", "").strip()

    books = Book.objects.select_related("author").all().order_by("title")

    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__name__icontains=query)
            | Q(genre__icontains=query)
            | Q(isbn__icontains=query)
        )

    context = {
        "books": books,
        "query": query,
        "members": Member.objects.all().order_by("full_name"),
        "total_books": Book.objects.count(),
        "available_books": Book.objects.filter(
            available_copies__gt=0
        ).count(),
        "authors": books.model.author.field.related_model.objects.count(),
        "member_count": Member.objects.count(),
    }

    return render(request, "library/home.html", context)


@transaction.atomic
def issue_book(request):
    if request.method != "POST":
        return redirect("home")

    book = get_object_or_404(
        Book.objects.select_for_update(),
        pk=request.POST.get("book_id"),
    )
    member = get_object_or_404(
        Member,
        pk=request.POST.get("member_id"),
    )

    if book.available_copies <= 0:
        messages.error(request, "Sorry, this book is not available.")
        return redirect("home")

    record = CirculationRecord.objects.create(
        book=book,
        member=member,
        issue_date=timezone.localdate(),
        due_date=timezone.localdate() + timedelta(days=14),
    )

    book.available_copies -= 1
    book.save(update_fields=["available_copies"])

    messages.success(
        request,
        f"'{book.title}' issued to {member.full_name}. "
        f"Due date: {record.due_date}.",
    )
    return redirect("circulation_records")


@transaction.atomic
def return_book(request, record_id):
    if request.method != "POST":
        return redirect("circulation_records")

    record = get_object_or_404(
        CirculationRecord.objects.select_for_update(),
        pk=record_id,
    )

    if record.returned_on is not None:
        messages.warning(request, "This book has already been returned.")
        return redirect("circulation_records")

    book = get_object_or_404(
        Book.objects.select_for_update(),
        pk=record.book_id,
    )

    today = timezone.localdate()
    overdue_days = max((today - record.due_date).days, 0)
    fine = FINE_PER_DAY * overdue_days

    record.returned_on = today
    record.fine_amount = fine
    record.save(update_fields=["returned_on", "fine_amount"])

    book.available_copies = min(
        book.available_copies + 1,
        book.total_copies,
    )
    book.save(update_fields=["available_copies"])

    messages.success(
        request,
        f"'{book.title}' returned. Fine: ₹{fine:.2f}",
    )
    return redirect("circulation_records")


def circulation_records(request):
    today = timezone.localdate()
    records = CirculationRecord.objects.select_related(
        "book", "member"
    ).order_by("-issue_date", "-id")

    record_rows = []
    for record in records:
        overdue_days = max((today - record.due_date).days, 0)

        if record.returned_on:
            current_fine = record.fine_amount
            status = "Returned"
        elif overdue_days > 0:
            current_fine = FINE_PER_DAY * overdue_days
            status = "Overdue"
        else:
            current_fine = Decimal("0.00")
            status = "Issued"

        record_rows.append({
            "record": record,
            "status": status,
            "current_fine": current_fine,
        })

    return render(
        request,
        "library/circulation_records.html",
        {
            "record_rows": record_rows,
            "today": today,
        },
    )

