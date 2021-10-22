from django.contrib import admin

# Register your models here.
from .models import Category, Drug, Tag, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'rate', 'create_at']
    readonly_fields = ['subject', 'comment', 'user', 'drug', 'rate']


admin.site.register(Category)
admin.site.register(Drug)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)