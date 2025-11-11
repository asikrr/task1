from django.test import TestCase

from catalog.models import BookInstance, Book, Author, Language, Genre
import uuid
from datetime import date

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label,'first name')

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label,'died')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length,100)

    def test_last_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(),'/catalog/author/1')

class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='Fantasy')

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        genre = Genre.objects.get(id=1)
        expected_object_name = genre.name
        self.assertEqual(expected_object_name, str(genre))


class LanguageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name='English')

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_name_unique(self):
        language = Language.objects.get(id=1)
        field = language._meta.get_field('name')
        self.assertTrue(field.unique)

    def test_object_name_is_name(self):
        language = Language.objects.get(id=1)
        expected_object_name = language.name
        self.assertEqual(expected_object_name, str(language))

class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем зависимые объекты
        author = Author.objects.create(first_name='test', last_name='testov')
        genre1 = Genre.objects.create(name='test genre 1')
        genre2 = Genre.objects.create(name='test genre 2')
        language = Language.objects.create(name='English')

        # Создаем книгу
        cls.book = Book.objects.create(
            title='test title',
            author=author,
            summary='test summary',
            isbn='9780141439518',
            language=language
        )
        cls.book.genre.add(genre1, genre2)

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_summary_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_genre_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_summary_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEqual(max_length, 1000)

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_object_name_is_title(self):
        book = self.book
        expected_object_name = book.title
        self.assertEqual(expected_object_name, str(book))

    def test_get_absolute_url(self):
        book = self.book
        self.assertEqual(book.get_absolute_url(), '/catalog/book/1')

    def test_display_genre(self):
        book = self.book
        expected_display = 'test genre 1, test genre 2'
        self.assertEqual(book.display_genre(), expected_display)

class BookInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(first_name='test', last_name='testov')
        language = Language.objects.create(name='English')
        book = Book.objects.create(
            title='test title',
            author=author,
            summary='test summary',
            isbn='9780486400595',
            language=language
        )

        cls.book_instance = BookInstance.objects.create(
            book=book,
            imprint='test imprint',
            due_back=date(2026, 6, 15)
        )

    def test_book_label(self):
        book_instance = self.book_instance
        field_label = book_instance._meta.get_field('book').verbose_name
        self.assertEqual(field_label, 'book')

    def test_imprint_label(self):
        book_instance = self.book_instance
        field_label = book_instance._meta.get_field('imprint').verbose_name
        self.assertEqual(field_label, 'imprint')

    def test_due_back_label(self):
        book_instance = self.book_instance
        field_label = book_instance._meta.get_field('due_back').verbose_name
        self.assertEqual(field_label, 'due back')

    def test_borrower_label(self):
        book_instance = self.book_instance
        field_label = book_instance._meta.get_field('borrower').verbose_name
        self.assertEqual(field_label, 'borrower')

    def test_status_label(self):
        book_instance = self.book_instance
        field_label = book_instance._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_imprint_max_length(self):
        book_instance = self.book_instance
        max_length = book_instance._meta.get_field('imprint').max_length
        self.assertEqual(max_length, 200)

    def test_status_max_length(self):
        book_instance = self.book_instance
        max_length = book_instance._meta.get_field('status').max_length
        self.assertEqual(max_length, 1)

    def test_id_is_uuid(self):
        book_instance = self.book_instance
        self.assertIsInstance(book_instance.id, uuid.UUID)

    def test_object_name_is_id_and_title(self):
        book_instance = self.book_instance
        expected_object_name = f'{book_instance.id} ({book_instance.book.title})'
        self.assertEqual(expected_object_name, str(book_instance))

    def test_is_overdue_with_past_date(self):
        book_instance = BookInstance(
            due_back=date(2020, 1, 1)  # дата в прошлом
        )
        self.assertTrue(book_instance.is_overdue)

    def test_is_overdue_with_future_date(self):
        book_instance = BookInstance(
            due_back=date(2100, 1, 1)  # дата в будущем
        )
        self.assertFalse(book_instance.is_overdue)

    def test_is_overdue_with_none_due_back(self):
        book_instance = BookInstance(
            due_back=None
        )
        self.assertFalse(book_instance.is_overdue)