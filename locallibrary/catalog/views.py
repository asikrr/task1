from django.shortcuts import render

from .models import Book, Author, BookInstance, Genre

def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()

    search_for_book = 'book1'
    search_for_genre = 'fantasy'

    num_books_contain_search = Book.objects.filter(title__icontains=search_for_book).count()
    num_genres_contain_search = Genre.objects.filter(name__icontains=search_for_genre).count()

    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,
                 'num_authors':num_authors,'search_for_book':search_for_book,'search_for_genre':search_for_genre,
                 'num_books_contain_search':num_books_contain_search, 'num_genres_contain_search':num_genres_contain_search},
    )