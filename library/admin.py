
from decimal import Decimal

from django.contrib import admin
from .models import Author, Book, Member, CirculationRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title", "author", "isbn", "genre",
        "total_copies", "available_copies",
    )
    search_fields = ("title", "author__name", "isbn")
    list_filter = ("genre",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "member_id", "email")
    search_fields = ("full_name", "member_id", "email")


@admin.register(CirculationRecord)
class CirculationRecordAdmin(admin.ModelAdmin):
    list_display = (
        "book", "member", "issue_date",
        "due_date", "returned_on", "fine_amount",
    )
    list_filter = ("issue_date", "due_date", "returned_on")

    def save_model(self, request, obj, form, change):
        if obj.returned_on:
            overdue_days = max(
                (obj.returned_on - obj.due_date).days, 0
            )
            obj.fine_amount = Decimal("5.00") * overdue_days

        super().save_model(request, obj, form, change)
