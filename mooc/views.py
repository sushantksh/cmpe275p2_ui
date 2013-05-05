# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mooc.models import MOOC
from time import localtime, strftime
from cStringIO import StringIO

import json
import requests

url = "http://localhost:8080" 

course = "course"
category = "category"
announcement = "announcement"
discussion = "discussion"
quiz = "quiz"

lst = "/list"

latest_mooc_list = None
selected_mooc = None
default_mooc = None

headers = {'content-type': 'application/json', 'charset': 'utf-8'}

# index function
def index(request):
   global latest_mooc_list, url, selected_mooc
   
   latest_mooc_list = MOOC.objects.all()
   for mooc in latest_mooc_list :
      if mooc.is_default :
         print 'Index Primary URL ===>', mooc.group
         selected_mooc = mooc
         break
   print 'Index Primary URL ===>', selected_mooc.group
   return render_to_response("login.html")

# Sign-Up function
def signup(request):
   return render_to_response("signup.html")

# add user
def add_user(request):
   global url, headers
   
   ctx = {}
   email = request.POST.get('email')
   password = request.POST.get('password')
   firstname = request.POST.get('firstname')
   lastname = request.POST.get('lastname')

   try: 
      local_user = User.objects.create_user(email, email, password)
      local_user.first_name = firstname
      local_user.last_name = lastname
      local_user.save()
   except: 
      ctx = {"message" : "User ID Exists. Please Try Again"}
      return render_to_response("signup.html", ctx)
     
   payload = {"_id":email, "own":[], "enrolled":[], "quizzes":[]} 
   response = requests.post(url + "user", data=json.dumps(payload), headers=headers)
   if response.status_code == 200 or response.status_code == 201:
      ctx = {"message" : "User successfully registered, please login to continue."}
      return render_to_response("login.html",ctx,context_instance=RequestContext(request))
   else :
      ctx = {"message" : "Sign Up Failed. Please Try Again"}
      return render_to_response("signup.html", ctx)

# User login related stuff
def login_user(request):
   global latest_mooc_list, selected_mooc
   
   email = request.POST['email']
   password = request.POST['password']
   
   user = authenticate(username=email, password=password)
   if user is not None:
      if user.is_active:
         login(request, user)
         ctx = {"fName": user.first_name, "lName": user.last_name, "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group }
         return render_to_response("home.html",ctx)
      else:
         # Return a 'disabled account' error message
         ctx = {"message" :"Login Failed. Please try Again"}
         return render_to_response("login.html",ctx)
   else:
         ctx = {"message" :"Login Failed. Please try Again"}
         return render_to_response("login.html",ctx)
      
def home(request):
   global latest_mooc_list, selected_mooc, url
   
   mooc_id = request.GET.get('id')
   if mooc_id is not None :
      selected_mooc = MOOC.objects.get(pk=mooc_id)
      url = selected_mooc.primary_URL
   print 'Home Primary URL ===>', url
   ctx = {"fName": request.user.first_name, "lName": request.user.last_name, "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group }
   return render_to_response('home.html',ctx)
      
def profile(request):
   global latest_mooc_list, selected_mooc
   
   ctx = {"fName" :request.user.first_name, "lName": request.user.last_name, "email":request.user.username, "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group}
   return render_to_response("profile.html",ctx)

def update_user(request):
   global latest_mooc_list, selected_mooc
   
   password = request.POST['password']
   firstname = request.POST.get('firstname')
   lastname = request.POST.get('lastname')
   
   if password is not None:
      request.user.set_password(password)
   if firstname is not None:
      request.user.first_name = firstname
   if lastname is not None:
      request.user.last_name = lastname
   request.user.save()

   ctx = {"fName": request.user.first_name, "lName": request.user.last_name, "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group }
   return render_to_response('home.html',ctx)
     
# log out function
def logout_user(request):
   logout(request)
   return render_to_response('login.html')   

# category
def list_category(request, msg=''):
   global url, category, lst, latest_mooc_list, selected_mooc
   
   file_str = StringIO()
   file_str.write(url)
   file_str.write('/category/list')

   tempUrl = file_str.getvalue()
   print 'URL-->', tempUrl
   response = requests.get(tempUrl)
   data = response.json()
   print '--->Category:data=', data
   ctx = {"fName": request.user.first_name, "lName": request.user.last_name, "category_list":data["list"], "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group, "message":msg }
   return render_to_response("categories.html",ctx)

def category(request):
   global latest_mooc_list, selected_mooc
   
   name = request.GET.get('id')
   if name is not None:
      file_str = StringIO()
      file_str.write(url)
      file_str.write('/category/')
      file_str.write(name)
      
      tempUrl = file_str.getvalue()
      print 'URL-->', tempUrl       
      response = requests.get(tempUrl)
      if response.status_code == 200:
         data = response.json()
         print '--->category:data=', data
         
         ctx = {"fName": request.user.first_name, "lName": request.user.last_name, "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group, "id":data["id"], "name": data["name"], "desc":data["description"]}
         return render_to_response("addCategory.html",ctx)
      
   ctx = {"fName": request.user.first_name, "lName": request.user.last_name, "id":"-1", "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group}
   return render_to_response("addCategory.html",ctx)

def add_category(request):
   global url, category, headers, latest_mooc_list, selected_mooc

   cat_id = request.POST.get('catId')
   name = request.POST.get('catName')
   desc = request.POST.get('catDesc')
   
   if cat_id == -1 :
      payload = {"name":name, "description":desc, "createDate":strftime("%Y-%m-%d %H:%M:%S", localtime()), "status":0}    
   else :
      payload = {"_id":cat_id, "name":name, "description":desc, "createDate":strftime("%Y-%m-%d %H:%M:%S", localtime()), "status":0} 
   
   print '--->add_category:data=', payload
   file_str = StringIO()
   file_str.write(url)
   file_str.write('/category')
   
   tempUrl = file_str.getvalue()
   response = requests.post(tempUrl, json.dumps(payload), headers=headers)
   if response.status_code == 200 or response.status_code == 201:
       if cat_id == -1 :
           return list_category(request, "Category added!!!")
       else:
           return list_category(request, "Category edited!!!")
   else:
      ctx = {"fName": request.user.first_name, "lName": request.user.last_name, "id":cat_id, "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group, "message":"Failed to add Category" }
      return render_to_response("addCategory.html",ctx)
   
def get_category(request):
   global url, category, latest_mooc_list, selected_mooc
   
   name = request.GET.get('id')
   response = requests.get(url + category + "/" + name)
   if response.status_code == 200:
      data = response.json()
      print '--->get_category:data=', data
      ctx = {"fName": request.user.first_name, "lName": request.user.last_name, "latest_mooc_list": latest_mooc_list, "selectedMooc": selected_mooc.group, "name": data["name"], "desc":data["description"]}
      return render_to_response("viewCategory.html",ctx)
   else:
      return list_category(request, "Failed to get category!!")
   
def remove_category(request):
   global url, category, headers, latest_mooc_list, selected_mooc
   
   name = request.GET.get('id')
   response = requests.delete(url + category + "/" + name)
   if response.status_code == 200:
      return list_category(request, "Category removed!!!")
   else:
      return list_category(request, "Failed to remove category!!")


# enroll user
def enroll_user(request):
   global headers, url, course
   course_id = request.GET.get('id')
   user_id = request.user.username
   print course_id, user_id
   payload = {"email" : user_id , "courseid" : course_id}
   requests.put(url+ course + "/enroll", data=json.dumps(payload), headers=headers)
   ctx = {"fName": request.user.first_name, "lName": request.user.last_name }
   return render_to_response("home.html",ctx,context_instance=RequestContext(request))      

#
# Course
#
#@login_required(login_url='login') -- > Good to have, need to figure out usage.
def add_course(request):
   global url, headers, course
   payload = {"_id":"course1","category":"annonymous_1","title":"introduction to algebra","section":2,"dept":"eng","term":"Spring","year":2013,"instructor":[{"name":"russel Doe","id":29}],"days":["Monday","Wednesday","Friday"],"hours":["8:00AM","9:15:AM"],"Description":"My course","attachment":"PATH","version":"1"}
   response = requests.post(url + course, data=json.dumps(payload), headers=headers)
   print response.text
   
def get_course(request):
   global url, headers, course
   response = requests.get(url + course +"/course1")
   print response.json()
   
def list_course(request):
   global url, headers, course, lst
   requests.get(url + course + lst)
#   print response.json()
   return render_to_response("courses.html") 

def remove_course():
   global url, headers, course
   response = requests.get(url + course +"/course1")
   print response.text

def update_course():
   global url, headers, course
   payload = {"_id":"course1","category":"annonymous_1","title":"machine learning","section":2,"dept":"eng","term":"Spring","year":2013,"instructor":[{"name":"russel Doe","id":29}],"days":["Monday","Wednesday","Friday"],"hours":["8:00AM","9:15:AM"],"Description":"My course","attachment":"PATH","version":"1"}
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text

#
# announcement
#

def add_announcement():
   global url, headers, announcement
   payload = {"_id": "anid1","courseId": "courseId","title": "Title","description":"desc","postDate": "04-22-2013","status": 0}
   response = requests.post(url + announcement, data=json.dumps(payload), headers=headers)
   print response.text
   
def get_announcement(request):
   global url, headers, announcement
   response = requests.get(url + announcement +"/anid1")
   print response.json()
   
def list_announcement():
   global url, headers, announcement, lst
   response = requests.get(url + announcement + lst)
   print response.json()

def remove_announcement():
   global url, headers, announcement
   response = requests.get(url + announcement +"/anid1")
   print response.text

def update_announcement():
   global url, headers, announcement
   payload = {"_id": "anid1","courseId": "courseId","title": "Title1234","description":"desc","postDate": "04-22-2013","status": 0}
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text


#
# discussion
#

def add_discussion():
   global url, headers, discussion
   payload = {"_id": "disid1","courseId": "course1","title": "Title","description": "desc","messages": [{"messages": "msg1","user": "user1","postDate": "04-22-2013"}, {"messages": "msg2","user": "user2","postDate":"01-22-2013"}]}
   response = requests.post(url + discussion, data=json.dumps(payload), headers=headers)
   print response.text
   
def get_discussion(request):
   global url, headers, discussion
   response = requests.get(url + discussion +"/disid1")
   print response.json()
   
def list_discussion():
   global url, headers, discussion, lst
   response = requests.get(url + discussion + lst)
   print response.json()

def remove_discussion():
   global url, headers, discussion
   response = requests.get(url + discussion +"/disid1")
   print response.text

def update_discussion():
   global url, headers, discussion
   payload = {"_id": "disid1","courseId": "courseId","title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text

#
# quiz
#

def add_quiz():
   global url, headers, quiz
   payload = {"_id": "quizid1","courseId": "courseId","questions": [{"question": "Que1","options": ["option1","option2"],"answer": "option1","point": 1},{"question": "Que2","options": ["option1","option2"],"answer":"option1","point": 1}]}
   response = requests.post(url + quiz, data=json.dumps(payload), headers=headers)
   print response.text
   
def get_quiz(request):
   global url, headers, quiz
   response = requests.get(url + quiz +"/disid1")
   print response.json()
   
def list_quiz():
   global url, headers, quiz, lst
   response = requests.get(url + quiz + lst)
   print response.json()

def remove_quiz():
   global url, headers, quiz
   response = requests.get(url + quiz +"/disid1")
   print response.text

def update_quiz():
   global url, headers, quiz
   payload = {"_id": "disid1","courseId": "courseId","title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text

#
# Utility Methods
#
def update_user_util(payload):
   global url, user
   return requests.put(url + user, data=json.dumps(payload), headers=headers)
