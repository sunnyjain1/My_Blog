from django.contrib import admin
from . import models
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField


class EntryAdmin(MarkdownModelAdmin):
    list_display = ("title", "created","modified")
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

class LikeAdmin(MarkdownModelAdmin):
	list_display = ("user","blog","created")

class CommentAdmin(MarkdownModelAdmin):
	list_display = ("user","value","blog")

admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Like,LikeAdmin)
