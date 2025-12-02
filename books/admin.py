from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Book, BookCategory, BookNote


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_book_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def get_book_count(self, obj):
        return obj.get_book_count()
    get_book_count.short_description = _('Books Count')


class BookNoteInline(admin.TabularInline):
    model = BookNote
    extra = 0
    fields = ['title', 'content', 'page_number', 'is_quote', 'is_favorite']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'rating', 'category', 'is_published', 'is_featured', 'created_at']
    list_filter = ['status', 'rating', 'category', 'is_published', 'is_featured', 'language', 'created_at']
    search_fields = ['title', 'author', 'isbn', 'description']
    prepopulated_fields = {'slug': ('title', 'author')}
    readonly_fields = ['created_at', 'updated_at', 'reading_progress']
    filter_horizontal = ['tags']
    inlines = [BookNoteInline]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'author', 'isbn', 'description', 'cover_image')
        }),
        (_('Book Details'), {
            'fields': ('pages', 'publication_date', 'publisher', 'language', 'category', 'tags')
        }),
        (_('Reading Status'), {
            'fields': ('status', 'rating', 'start_date', 'finish_date')
        }),
        (_('Review'), {
            'fields': ('review',),
            'classes': ('collapse',)
        }),
        (_('Publishing'), {
            'fields': ('is_published', 'is_featured', 'added_by')
        }),
        (_('SEO'), {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new book
            obj.added_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(BookNote)
class BookNoteAdmin(admin.ModelAdmin):
    list_display = ['book', 'title', 'page_number', 'is_quote', 'is_favorite', 'created_at']
    list_filter = ['is_quote', 'is_favorite', 'book__category', 'created_at']
    search_fields = ['title', 'content', 'book__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Note Information'), {
            'fields': ('book', 'title', 'content', 'page_number')
        }),
        (_('Options'), {
            'fields': ('is_quote', 'is_favorite')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )