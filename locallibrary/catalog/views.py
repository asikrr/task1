from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime

from .forms import RenewBookModelForm

def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()

    search_for_book = 'book1'
    search_for_genre = 'fantasy'

    num_books_contain_search = Book.objects.filter(title__icontains=search_for_book).count()
    num_genres_contain_search = Genre.objects.filter(name__icontains=search_for_genre).count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,
                 'num_authors':num_authors,'search_for_book':search_for_book,'search_for_genre':search_for_genre,
                 'num_books_contain_search':num_books_contain_search, 'num_genres_contain_search':num_genres_contain_search,
                 'num_visits':num_visits},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()

            return HttpResponseRedirect(reverse('all-borrowed-books') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_books_list.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

class AuthorCreate(PermissionRequiredMixin, generic.CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}

    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

    permission_required = 'catalog.delete_author'

class BookCreate(PermissionRequiredMixin, generic.CreateView):
    model = Book
    fields = '__all__'

    permission_required = 'catalog.add_book'

class BookUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Book
    fields = ['title','author','summary','isbn','genre','language']

    permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy('books')

    permission_required = 'catalog.delete_book'