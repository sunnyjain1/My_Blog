from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.slug


class EntryQuerySet(models.QuerySet):

    def published(self):
        return self.filter(publish=True)

class Bloguser(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    tagline = models.CharField(max_length=100)
    def get_absolute_url(self):
        return reverse("profile",kwargs={"slug": self.slug})
    def __str__(self):
        return self.slug

class Entry(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    objects = EntryQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"
        ordering = ["-modified"]

class Like(models.Model):
    user = models.ForeignKey(User)
    blog = models.ForeignKey(Entry)
    created = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
	user = models.ForeignKey(User)
	value = models.CharField(max_length=300)
	blog = models.ForeignKey(Entry)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["created"]
