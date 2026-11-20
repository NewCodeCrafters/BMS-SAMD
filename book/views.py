from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Book, Category

# Create your views here.

def book_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '').strip()
    sort_by = request.GET.get('sort','title')

    books = Book.objects.all()
    categories = Category.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )

    if category_id.isdigit():
        books = books.filter(category__id=int(
            category_id))
    else:
        category_id = ''

    books = books.distinct()
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "books": page_obj,
        "query": query,
        "categories": categories,
        "selected_category": category_id,
        "sort_by" : sort_by,
        "page_obj": page_obj,

    }

    return render(request, "book_list.html", context)


def book_details(request, id):
    book = get_object_or_404(Book, id=id)

    context = {
        "book": book
    }
    return render(request, "book_details.html", context)