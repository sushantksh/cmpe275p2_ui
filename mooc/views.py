# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mooc.models import MOOC

import json
import requests

url = "http://localhost:8080/" 

course = "course"
category = "category"
announcement = "announcement"
discussion = "discussion"
quiz = "quiz"

lst = "/list"

latest_mooc_list = None

headers = {'content-type': 'application/json', 'charset': 'utf-8'}

def index(request):
   return render_to_response('login.html')

def home(request):
   mooc_id = request.GET.get('id')
   if mooc_id != None :
      mooc = MOOC.objects.get(pk=mooc_id)
      url = mooc.get_primary_url()
   
   ctx = {"fName": user.first_name, "lName": user.last_name, "latest_mooc_list": latest_poll_list }
   return render_to_response('home.html')
url
#
# User login related stuff
#

# Sign Up function
def signup(request):
   return render_to_response("signup.html")

def signin(request):
   return render_to_response("login.html")

def login_user(request):
   latest_poll_list = MOOC.objects.all()
    
   email = request.POST['email']
   password = request.POST['password']
   print password
   user = authenticate(username=email, password=password)
   if user is not None:
      if user.is_active:
         login(request, user)
         ctx = {"fName": user.first_name, "lName": user.last_name, "latest_mooc_list": latest_poll_list }
         return render_to_response("home.html",ctx,context_instance=RequestContext(request))
      else:
         # Return a 'disabled account' error message
         ctx = {"message" :"Login Failed. Please try Again"}
         return render_to_response("login.html",ctx,context_instance=RequestContext(request))
   else:
         ctx = {"message" :"Login Failed. Please try Again"}
         return render_to_response("login.html",ctx,context_instance=RequestContext(request))
      
def change_password(request):
   print "New Password",request.POST.get('password')
   print request.user.first_name
   request.user.set_password(request.POST.get('password'))
   request.user.save()
   ctx = {"fName": request.user.first_name, "lName": request.user.last_name }
   return render_to_response("home.html",ctx,context_instance=RequestContext(request))      

# log out function
def logout_user(request):
   logout(request)
   return render_to_response('login.html')   



#
# user
#

def add_user(request):
   global url, headers
   ctx = {}

   if request.method == "POST" :
      email = request.POST.get("email")
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
         
      payload = {"_id": email,"pwd": password,"fName": firstname,"lName":lastname}
      response = requests.post(url + "user", data=json.dumps(payload), headers=headers)
      if response.status_code == 200:
         return render_to_response("login.html",ctx,context_instance=RequestContext(request))
      else :
         ctx = {"message" : "Sign Up Failed. Please Try Again"}
         return render_to_response("signup.html", ctx)

   
def get_user(request):
   global url, headers
   response = requests.get(url + "user/" + request.user.user_name)
   print response.json()
   
def list_user(request):
   global url, headers, user, lst
   response = requests.get(url + user + lst)
   print response.json()

def remove_user(request):
   global url, headers, user
   response = requests.delete(url + user +"/sugandhi@abc.com")
   print response.text

def profile(request):
   data = {"fName" :request.user.first_name, "lName": request.user.last_name, "password" :request.user.password}
   ctx = {"fName": request.user.first_name, "lName": request.user.last_name,"user_detail":data}

   return render_to_response("profile.html",ctx,context_instance=RequestContext(request))

def update_user(request):
   data = {"fName" :request.user.first_name, "lName": request.user.last_name, "password" :request.user.password}
   ctx = {"fName": request.user.first_name, "lName": request.user.last_name,"user_detail":data}

   return render_to_response("profile.html",ctx,context_instance=RequestContext(request))

   payload = {"_id": "disid1","courseId": "courseId","title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}
   print update_user_util(payload)

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
# Category
#

def category(request):
   return render_to_response("addCategory.html")

def add_category(request):
   global url, headers, category
   global endpoint
   if request.POST:
      name = request.POST.get('catName')
      payload = {"_id":name, "name":name, "description":"desc", "createDate":"01-01-2013", "status":0}
      data=json.dumps(payload)
      print '--->AddCategory:data=', data
      response = requests.post("http://localhost:8080/category", data, headers=headers)
      if response.status_code == 200:
         print 'SUCCESS'
   return list_category(request)
   
def get_category(request):
   global url, headers, category
   global endpoint
   
   name = request.GET.get('id')
   response = requests.get("http://localhost:8080/category/" + name)
   print '--->Category:List', response.text
   data = response.json()
   print '--->Category:data=', data
   ctx = {"category": data["name"]}

   return render_to_response("viewCategory.html",ctx,context_instance=RequestContext(request))   
   
def list_category(request):
   global url, category, lst
   global endpoint
   response = requests.get("http://localhost:8080/category/list")
   print '--->Category:List', response.text
   data = response.json()
   print '--->Category:data=', data
   ctx = {"fName": request.user.first_name, "lName": request.user.last_name,"category_list":data["list"]}
   return render_to_response("categories.html",ctx,context_instance=RequestContext(request))

def remove_category(request):
   global url, headers, category
   
   name = request.GET.get('id')
   requests.delete("http://localhost:8080/category/" + name)
   return list_category(request)
   

def update_category(request):
   global url, headers, category
   request.GET.get('id')
   
   response = requests.get("http://localhost:8080/category/" + id)
   print '--->Category:update=', response.text
   data = response.json()
   print '--->Category:data=', data
   ctx = {"category": data["name"]}
   ctx.update(csrf(request))

   return render_to_response("addCategory.html",ctx,context_instance=RequestContext(request))

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
