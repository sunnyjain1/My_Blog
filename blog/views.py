from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import render
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

class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "post.html"

class features(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "features.html"


class register(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "register.html"

class login(generic.ListView):
	queryset = models.Entry.objects.published()
	template_name = "login.html"
