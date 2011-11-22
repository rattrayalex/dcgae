import random
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from django.utils import simplejson
from django.forms import ModelForm
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.forms.formsets import formset_factory
from operator import mul
from google.appengine.api import images 
from django.core.files.uploadedfile import InMemoryUploadedFile
from filetransfers.api import prepare_upload
import settings
from google.appengine.ext import db

from app.models import *

import os, sys, datetime, copy, logging


ROW_WIDTH = 3

def image_handler(request, project, ID, size):
  project_name = str(project).replace('%20',' ')
  logging.warning(project_name)
  project = Project.objects.get(name=project_name)
  if project.images:
    headers = "Content-Type: image/png"
    if int(ID) == 0:
#      logging.warning("ID was zero")
      img = project.images.all()[0]
      the_image = img.full if size=='full' else img.medium
    else:
      img = project.images.get(id=int(ID))
      logging.info(size=='full')
      the_image = img.full if size=='full' else img.medium
    return HttpResponse(the_image, headers)

def divide(n, k):
  '''Divide n into sets of size of k or smaller.'''
  for i in range(0, len(n), k):
    yield n[i:i+k]

def index(request):
  projects = Project.objects.all().order_by('name')
  context = {
      'project_table': divide(projects, ROW_WIDTH),
      'user': request.user,
      }
  return render_to_response('index.html', context)

def isUnique(matrix, pair):
  for p in matrix:
    if (p[0]==pair[0] and p[1]==pair[1]) or (p[1]==pair[0] and p[0]==pair[1]):
      return False
  return True

def rank(request, project): 
  project_name = str(project)
  project = Project.objects.get(name=project_name)
  images = [image.id for image in project.images.all()]
  logging.warning(images)
  
  n = len(images)
  k = 2
  nCr = lambda n,k: int(round(
    reduce(mul, (float(n-i)/(i+1) for i in range(k)), 1)
    ))
  max_limit = 5
  limit = min(nCr(n,k), max_limit)
  pairs = []
  for i in range(limit):
##    print "in big for loop"
    left, right = random.sample(images, 2)
    pair = [left, right]
    while isUnique(pairs, pair)!= True:
##      print "in while loop"
      left, right = random.sample(images, 2)
      pair = [left, right]
    pairs.append(pair)
##    print i
      
##  print pairs
  context = {
    'Project': project,
    'limit': limit,
    'img_list': pairs,
    'user': request.user,
    }
  return render_to_response('rank.html',context, context_instance = RequestContext(request))


def vote(request):
  print "in vote method"
  if request.method == 'POST':
    data = request.POST
    print data
    w = Image.objects.get(id__exact=data['winner'])
    l = Image.objects.get(id__exact=data['loser'])
    print w, l
    vote = Vote(
    winner = w,
    loser = l,
    time = datetime.datetime.now(),
    winner_comment = data['winner_comment'],
    loser_comment = data['loser_comment']
    )
  vote.save()
  return HttpResponse('boo!')

def thanks(request, project):
  project_name = str(project)#.replace('%20', ' ')
  project =  Project.objects.get(name=project_name)
  context = {
          'Project': project,
          'user': request.user,
          }
  return render_to_response('thanks.html',context)

class SignUpFormAgain(ModelForm):
    class Meta:
        model = Client

class SignUpForm(forms.Form):
  email = forms.EmailField(max_length=30)
  password = forms.CharField(widget=forms.PasswordInput, label="Your Password")
  name = forms.CharField(max_length=50, label="Publicly visible name")
  description = forms.CharField(widget=forms.Textarea)
  
def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      username = email
      name = form.cleaned_data['name']
      description = form.cleaned_data['description']

      user = User.objects.create_user(username, email, password)
      user.save()
      
      client = Client(name=name, email=email, user=user, description=description)
      client.save()
      
      user = auth.authenticate(username=email, password=password)
      if user is not None:
        auth.login(request, user)
      return HttpResponseRedirect('/loggedin/')
  else:
    form = SignUpForm()
  return render_to_response('signup.html', {'form':form,}, context_instance = RequestContext(request))

class create_project(forms.Form):
  name = forms.CharField(max_length=100, label="Project Name")
  description = forms.CharField(widget=forms.Textarea, label="A description of your project")
  criteria = forms.CharField(max_length=100, label="Criteria (Which one ___?)")
  more_criteria = forms.CharField(widget=forms.Textarea, label="More Criteria (what else is important?)")

def myFileHandler(request):
  # logging.warning(request)
  if request.method == 'POST':
    for field_name in request.FILES:
      uploaded_file = request.FILES[field_name]
      logging.warning(uploaded_file)
      large_size = 330, 230
      medium_size = 210, 150
      project = request.POST['project']
      new_image = Image()
      new_image.project = Project.objects.get(name=project)
      f = uploaded_file.read()
      new_image.full = db.Blob(f)
      img = images.Image(f)
      img.resize(width=330, height=230)
      thumb = img.execute_transforms(output_encoding=images.PNG)
      new_image.large = db.Blob(uploaded_file.read())
      new_image.medium = db.Blob(thumb)
      new_image.save()
    return HttpResponse("ok", mimetype="text/plain")

def upload_project(request):
  if request.method == 'POST':
    logging.warning("trying to upload project")
    logging.warning(request.POST)
##    logging.warning(request.user)
    name = request.POST['name']
    new_project = Project(
      name = name,
      description = request.POST['description'],
      creator = request.user.client,
      reward = 0,
      criteria = request.POST['criteria'],
      more_criteria = request.POST['more_criteria']
      )
    logging.warning(name)
    new_project.save()
    project = Project.objects.get(name=name)
    from django.utils import simplejson
    return HttpResponse(simplejson.dumps({'project':name}), content_type="application/json")

def upload_files(request):
  if request.method == 'POST':
    return upload_project(request)
  else:
      project_form = create_project()
  # This is filetransfers stuff
##  upload_url, upload_data = prepare_upload(request, view_url)
  
  context = {
    'project_form': project_form,
    'user': request.user,
##    'session_cookie_name': settings.SESSION_COOKIE_NAME,
    'session_key': request.session.session_key
    # This is filetransfers stuff
##    'upload_url': upload_url,
##    'upload_data': upload_data,
    }
  return render_to_response('upload.html', context, context_instance = RequestContext(request))

class SignInForm(forms.Form):
  email = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput)
def signin(request): 
  if request.method == 'POST':
##    print "in signin post"
    form = SignInForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = auth.authenticate(username=email, password=password)
      if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/loggedin/')
      else:
        return HttpResponseRedirect('/signin/')
  else:
##    print "in signin else"
    form = SignInForm() 
##  print "in signin "
  return render_to_response('signin.html', {'form': form, 'user': request.user,},context_instance=RequestContext(request))

def loggedin(request):
  username = request.user.client.name
  return render_to_response('loggedin.html',{'username':username, 'user': request.user,})

def logout(request):
  auth.logout(request)
  return HttpResponseRedirect('/')

def results(request, project):
  project_name = str(project)
  project = Project.objects.get(name = project_name)
  images = [img for img in project.images.all()]
##  images = list(Image.objects.filter(project__name=project_name))s
  images.sort(key = lambda x: x.losevotes.count())
  images.sort(key = lambda x: -x.winvotes.count())
  images.sort(key = lambda x: -x.score)
  
  context = {
    'image_list': images,
    'project': project,
    'user': request.user,
    }
  return render_to_response('results.html', context)

