from django.views import generic
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from . import models


class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "home.html"
    paginate_by = 2

def search(request):
    if 's' in request.GET:
    	s = request.GET['s']
    	lis = models.Entry.objects.filter(title__icontains=s)
    	if len(lis) == 0:
    		x = 0
    	else:
    		x = 1
    	return render(request,'search.html',{'x':x,'post':lis})
    else:
    	x = 0
    	return render(request,'search.html',{'x':x})

def message(request):
	uname = request.GET['uname']
	fname = request.GET['fname']
	lname = request.GET['lname']
	mail = request.GET['usermail']
	pswd = request.GET['password']
	if len(User.objects.filter(username = uname)) == 0:
		user = User.objects.create_user(uname,first_name=fname,last_name=lname,email=mail,password=pswd)
		return render(request,'login.html')
	else:
		return render(request,'register.html')

class Authen(generic.ListView):
	paginate_by = 2

	def get_queryset(self):
		uname =  self.request.GET['username']
		pswd = self.request.GET['password']
		user = authenticate(username=uname, password=pswd)
		if user is not None:
			login(self.request,user);
			self.template_name = "home.html"
			return models.Entry.objects.filter(publish=True)
		else:
			self.template_name = "login.html"
			return []

class BlogDetail(generic.DetailView):
	model = models.Entry
	template_name = "post.html"
	def get_context_data(self, **kwargs):
		context = super(BlogDetail, self).get_context_data(**kwargs)
		uname = self.request.user
		url = self.request.get_full_path()
		x = url.split("/")
		y = x[len(x)-2]
		z = x[len(x)-1]
		blog = models.Entry.objects.filter(slug=y)
		#import pdb; pdb.set_trace()
		if self.request.user.is_authenticated():
			t = models.Like.objects.filter(user=uname, blog=blog)
		else:
			t = []
		if z == "?home":
			if not t:
				l=0;
			else:
				l=1;
		else:
			if not t:
				if self.request.user.is_authenticated():
					models.Like.objects.create(user=uname, blog=blog[0])
					l=1;
				else :
					l=0;
			else:
				t.delete()
				l=0;
		num = len(models.Like.objects.filter(blog=blog))
		context['check'] = l
		context['num'] = num
 		return context
class send(generic.ListView):
	paginate_by = 2
	template_name = "home.html"
	def get_queryset(self):
		title = self.request.GET['title']
		content = self.request.GET['content']
		tags = self.request.GET.getlist('tags')
		t = []
		for p in tags:
			x = models.Tag.objects.get(slug=p)
			t.append(x.id)
		curr_entry = models.Entry.objects.create(title=title,body=content,slug=slugify(title),publish=False)
		#import pdb;pdb.set_trace()
		curr_entry.tags = t
		return models.Entry.objects.filter(publish=True)

class features(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "features.html"

class req(generic.ListView):
	queryset = models.Tag.objects.all()
	template_name = "req.html"

class register(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "register.html"

class Login(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "login.html"

class Logout(generic.ListView):
	def get_queryset(self):
		logout(self.request)
		return []
	template_name = "login.html"