from django.views import generic
import json
from django.http import JsonResponse
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
    def get_context_data(self,**kwargs):
    	context = super(BlogIndex, self).get_context_data(**kwargs)
    	alltag = models.Tag.objects.all()
    	context['alltag'] = alltag
    	context['act'] = "home"
    	return context

class tags(generic.ListView):
    template_name = "home.html"
    paginate_by = 2
    def get_queryset(self):
    	url = self.request.get_full_path()
    	x = url.split("/")
    	y = x[len(x)-2]
    	z = models.Tag.objects.filter(slug=y)
    	return models.Entry.objects.filter(publish=True,tags=z)
    	#import pdb;pdb.set_trace()
    def get_context_data(self,**kwargs):
    	url = self.request.get_full_path()
    	x = url.split("/")
    	y = x[len(x)-2]
    	context = super(tags, self).get_context_data(**kwargs)
    	alltag = models.Tag.objects.all()
    	context['alltag'] = alltag
    	context['act'] = y
    	return context


def search(request):
	alltag = models.Tag.objects.all()
	act = ""
	if 's' in request.GET:
		s = request.GET['s']
		item = request.GET.get('item')
		if item == 'Title':
			lis = models.Entry.objects.filter(title__icontains=s)
		elif item == 'Content':
			lis = models.Entry.objects.filter(body__icontains=s)
		else:
			lis = []
		if len(lis) == 0:
			x = 0
		else:
			x = 1
		return render(request,'search.html',{'x':x,'post':lis,'alltag':alltag,'act':act})
	else:
		x = 0
		return render(request,'search.html',{'x':x,'alltag':alltag,'act':act})

def message(request):
	uname = request.GET['uname']
	fname = request.GET['fname']
	lname = request.GET['lname']
	mail = request.GET['usermail']
	pswd = request.GET['password']
	tgln = request.GET['tl']
	uname = slugify(uname)
	alltag = models.Tag.objects.all()
	act = ""
	if len(User.objects.filter(username = uname)) == 0:
		user = User.objects.create_user(uname,first_name=fname,last_name=lname,email=mail,password=pswd)
		models.Bloguser.objects.create(user=user,slug=uname,tagline=tgln)
		return render(request,'login.html',{'alltag':alltag,'act':act})
	else:
		return render(request,'msg.html',{'alltag':alltag,'act':act})

class Authen(generic.ListView):
	paginate_by = 2

	def get_queryset(self):
		uname =  self.request.GET.get('username')
		pswd = self.request.GET.get('password')
		user = authenticate(username=uname, password=pswd)
		#import pdb;pdb.set_trace()
		if user is not None:
			login(self.request,user);
			self.template_name = "home.html"
			return models.Entry.objects.filter(publish=True)
		else:
			self.template_name = "login.html"
			return []

	def get_context_data(self,**kwargs):
		context = super(Authen, self).get_context_data(**kwargs)
		alltag = models.Tag.objects.all()
		context['alltag'] = alltag
		context['act'] = "home"
		return context

def BlogDetail(request,slug):
	uname = request.user
	url = request.get_full_path()
	x = url.split("/")
	y = x[len(x)-2]
	z = x[len(x)-1]
	blog = models.Entry.objects.filter(slug=y)
	allc = models.Comment.objects.filter(blog=blog)
	#import pdb; pdb.set_trace()
	alltag = models.Tag.objects.all()
	act = ""
	if request.user.is_authenticated():
		t = models.Like.objects.filter(user=uname, blog=blog)
	else:
		t = []
	if z == "?home" or z == "":
		if not t:
			l=0;
		else:
			l=1;
		num = len(models.Like.objects.filter(blog=blog))
		return render(request,'post.html',{'check':l,'num':num,'slug':slug,'object':blog[0],'comm':allc,'alltag':alltag,'act':act})
	elif z == "?like":
		if not t:
			if request.user.is_authenticated():
				models.Like.objects.create(user=uname, blog=blog[0])
				l=1;
			else :
				l=0;
		else:
			t.delete()
			l=0;
		num = len(models.Like.objects.filter(blog=blog))
		resp = {}
		resp['check'] = l
		resp['num'] = num
		return HttpResponse(json.dumps(resp),content_type="application/json")
	else:
		#import pdb;pdb.set_trace()
		content = request.GET.get('val')
		models.Comment.objects.create(user=uname, blog=blog[0],value=content)
		allcom = models.Comment.objects.filter(blog=blog[0])
		x = len(allcom)
		data = {'username':allcom[x-1].user.username,'fn':allcom[x-1].user.first_name,'ln':allcom[x-1].user.last_name,'value':allcom[x-1].value} 
		return HttpResponse(json.dumps(data), content_type="application/json")
		
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
	def get_context_data(self,**kwargs):
		context = super(send, self).get_context_data(**kwargs)
		alltag = models.Tag.objects.all()
		context['alltag'] = alltag
		context['act'] = "home"
		return context

def profile(request,slug):
	url = request.get_full_path()
	x = url.split("/")
	y = x[len(x)-2]
	z = x[len(x)-1]
	user = User.objects.filter(username=slug);
	bu = models.Bloguser.objects.filter(user=user)
	#import pdb;pdb.set_trace()
	alltag = models.Tag.objects.all()
	act = ""
	if z == "":
		return render(request,'profile.html',{'bu':bu[0],'slug':slug,'alltag':alltag,'act':act})
	else:
		likes = models.Like.objects.filter(user = user)
		comment = models.Comment.objects.filter(user = user)
		data = []
		for l in likes:
			data.append({'type':'like','blog':l.blog.title,'created':l.created.strftime('%B %d, %Y %I:%M %p')})
		for c in comment:
			data.append({'type':'comment','blog':c.blog.title,'value':c.value,'created':c.created.strftime('%B %d, %Y %I:%M %p')})
		return HttpResponse(json.dumps(data),content_type="application/json")

class features(generic.ListView):
	queryset = []
	template_name = "features.html"
	def get_context_data(self,**kwargs):
		context = super(features, self).get_context_data(**kwargs)
		alltag = models.Tag.objects.all()
		context['alltag'] = alltag
		context['act'] = "home"
		return context

class req(generic.ListView):
	queryset = models.Tag.objects.all()
	template_name = "req.html"
	def get_context_data(self,**kwargs):
		context = super(req, self).get_context_data(**kwargs)
		alltag = models.Tag.objects.all()
		context['alltag'] = alltag
		context['act'] = "home"
		return context

class register(generic.ListView):
	queryset = []
	template_name = "register.html"
	def get_context_data(self,**kwargs):
		context = super(register, self).get_context_data(**kwargs)
		alltag = models.Tag.objects.all()
		context['alltag'] = alltag
		context['act'] = "home"
		return context

class Login(generic.ListView):
	queryset = []
	template_name = "login.html"
	def get_context_data(self,**kwargs):
		context = super(Login, self).get_context_data(**kwargs)
		alltag = models.Tag.objects.all()
		context['alltag'] = alltag
		context['act'] = "home"
		return context

class Logout(generic.ListView):
	def get_queryset(self):
		logout(self.request)
		return []
	def get_context_data(self,**kwargs):
		context = super(Logout, self).get_context_data(**kwargs)
		alltag = models.Tag.objects.all()
		context['alltag'] = alltag
		context['act'] = "home"
		return context
	template_name = "login.html"
