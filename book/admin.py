from django.contrib import admin
from .models import Author, Book, Category, Book
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin) :
    list_display = ("first_name","last_name","nationality","biography")
    search_fields = ("first_name", "last_name", "nationality")
    list_filter = ("nationality",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin) :
    list_display = ("name", "description")
    search_fields= ("name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "show_categories","pdf_file","pdf_url")
    search_fields= ("title", "author__first_name", "author__last_name")
    list_filter = ("category",)

    @admin.display(description="Categories")
    def show_categories(self, obj):
        return ", ". join(category.name for category in obj.category.all())