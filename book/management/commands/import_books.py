import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from book.models import Book, Author, Category


class Command(BaseCommand):
    help = "Import books from books_import.csv"

    def handle(self, *args, **options):

        csv_file = Path(__file__).resolve().parents[2] / "books_import.csv"

        if not csv_file.exists():
            self.stdout.write(
                self.style.ERROR("CSV file not found!")
            )
            return

        imported = 0
        skipped = 0

        with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                title = row["title"].strip()
                first_name = row["author_first_name"].strip()
                last_name = row["author_last_name"].strip()
                description = row["description"].strip()
                category_name = row["category"].strip()
                source = (row.get("source")or"").strip()
                license = (row.get("license")or"").strip()
                pdf_url =(row.get("pdf_url")or"").strip()

                if not title or not first_name or not category_name:
                    self.stdout.write(f"Skipped (missing information): {title}")
                    skipped += 1
                    continue

                if Book.objects.filter(title=title).exists():
                    self.stdout.write(f"Skipped (already exists): {title}")
                    skipped += 1
                    continue

                author = Author.objects.filter(
                    first_name=first_name,
                    last_name=last_name
                ).first()

                if author is None:
                    author = Author.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        biography="Biography not yet added."
                    )

                category = Category.objects.filter(name=category_name).first()

                if category is None:
                    category = Category.objects.create(
                    name=category_name,
                    description="Imported category"
                    )

                book = Book.objects.create(
                    title=title,
                    description=description,
                    author=author
                )

                book.category.add(category)

            imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {imported} books. "
                f"Skipped {skipped} books."
            )
        )