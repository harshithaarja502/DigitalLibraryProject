from django.core.management.base import BaseCommand

from library.models import Author, Book, Member


class Command(BaseCommand):
    help = "Create fictional demo authors, books, and members if missing."

    def handle(self, *args, **options):
        authors = {}
        for name, bio in [
            (
                "Mira Sen",
                "Writes imaginative stories about science and society.",
            ),
            (
                "Arjun Mehta",
                "Explores history, culture, and everyday life.",
            ),
            (
                "Leela Rao",
                "Creates practical guides to technology and learning.",
            ),
        ]:
            authors[name], _ = Author.objects.get_or_create(
                name=name,
                defaults={"bio": bio},
            )

        books = [
            {
                "title": "The Glass Observatory",
                "author": authors["Mira Sen"],
                "isbn": "9780000000101",
                "genre": "Science Fiction",
                "description": "A fictional journey through a changing universe.",
                "total_copies": 4,
                "available_copies": 4,
            },
            {
                "title": "Maps of the Monsoon",
                "author": authors["Arjun Mehta"],
                "isbn": "9780000000102",
                "genre": "History",
                "description": "A fictional account of journeys across seasons.",
                "total_copies": 3,
                "available_copies": 3,
            },
            {
                "title": "Small Steps in Data",
                "author": authors["Leela Rao"],
                "isbn": "9780000000103",
                "genre": "Technology",
                "description": "An introduction to working with information.",
                "total_copies": 5,
                "available_copies": 5,
            },
            {
                "title": "The Quiet Algorithm",
                "author": authors["Mira Sen"],
                "isbn": "9780000000104",
                "genre": "Mystery",
                "description": "A fictional mystery in a city of connected devices.",
                "total_copies": 2,
                "available_copies": 2,
            },
        ]
        for book in books:
            isbn = book.pop("isbn")
            Book.objects.get_or_create(isbn=isbn, defaults=book)

        members = [
            {
                "full_name": "Demo Reader One",
                "member_id": "DEMO-READER-001",
                "email": "reader.one@example.com",
            },
            {
                "full_name": "Demo Reader Two",
                "member_id": "DEMO-READER-002",
                "email": "reader.two@example.com",
            },
        ]
        for member in members:
            Member.objects.get_or_create(
                member_id=member["member_id"],
                defaults=member,
            )

        self.stdout.write(self.style.SUCCESS("Demo library data is ready."))
