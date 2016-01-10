from django.views import generic
from . import models


class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "home.html"
    paginate_by = 2


class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "post.html"

class press(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "press.html"

class features(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "features.html"

class hires(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "hires.html"

class about(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "about.html"