# Create your views here.

# from django.contrib.auth import authenticate, login

from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf

import json
import requests

url = "http://localhost:8080/" 

user = "user"
course = "course"
category = "category"
announcement = "announcement"
discussion = "discussion"
quiz = "quiz"

lst = "/list"

headers = {'content-type': 'application/json', 'charset': 'utf-8'}

def home(request):
   return render_to_response('home.html')
#
# user
#

def add_user(request):
   global url, headers, user
   c = {}
   if request.method == "POST" :
      email = request.POST.get("email")
      password = request.POST.get('password')
      firstname = request.POST.get('firstname')
      lastname = request.POST.get('lastname')
         
      payload = {"_id": email,"pwd": password,"firstName": firstname,"lastName":lastname}
      print '---> payload:',payload
      response = requests.post(url + user, data=json.dumps(payload), headers=headers)
      if response.status_code == 200:
         c.update(csrf(request))
   return render_to_response("home.html", c)
   
def get_user(request):
   global url, headers, user
   response = requests.get(url + user +"/sugandhi@abc.com")
   print response.json()
   
def list_user(request):
   global url, headers, user, lst
   response = requests.get(url + user + lst)
   print response.json()

def remove_user(request):
   global url, headers, user
   response = requests.delete(url + user +"/sugandhi@abc.com")
   print response.text

def update_user(request):
   global url, headers, user
   payload = {"_id": "disid1","courseId": "courseId","title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}
   print update_user_util(payload)


#
# Course
#

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
   c = {}
   c.update(csrf(request))
   return render_to_response("addCategory.html", c)

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
   ctx = {"fName": "Manoj", "lName": "Dhoble","category_list":data["list"]}

   return render_to_response("categories.html",ctx,context_instance=RequestContext(request))

def remove_category(request):
   global url, headers, category
   
   name = request.GET.get('id')
   response = requests.delete("http://localhost:8080/category/" + name)
   return list_category(request)
   

def update_category(request):
   global url, headers, category
   c = {}
   c.update(csrf(request))
   return render_to_response("addCategory.html", c)

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

def signin(request):
   c = {}
   c.update(csrf(request))
   return render_to_response("login.html", c)

def login(request):
   global url, user
   if request.method == "POST" :
      email = request.POST.get("email")
      password = request.POST.get("password")
         
      response = requests.get(url + user + "/" + email)
      data = response.json() 
      print data
      pwd = data["pwd"]

      if password == pwd:
         ctx = {"fName": data["fName"], "lName": data["lName"]}
         data['Status'] = 1
         update_user_util(data)
         return render_to_response("home.html",ctx,context_instance=RequestContext(request))
   
   c = {}
   c.update(csrf(request))
   return render_to_response("login.html", c)
      
# Sign Up function
def signup(request):
   c = {}
   c.update(csrf(request))
   return render_to_response("signUp.html", c)


# signup_home page fucntion is called when there is new user entry
def signup_home(request):
   global endpoint
   if request.POST:
      username = request.POST.get('username')
      password = request.POST.get('password')
      firstname = request.POST.get('firstname')
      lastname = request.POST.get('lastname')

   payload = { "email": username,"pwd": password,"fName": firstname,"lName": lastname} 
   print "Calling bottle from Django ......from SignUp Home "
   r = requests.post(endpoint + "signup",data=json.dumps(payload))
   print str(r)+" ---- > Call Back from Bottle Achieved "
   ctx = r.json()
   print ctx
   return render_to_response("signin.html",ctx,context_instance=RequestContext(request))
   #return render(request, "home.html",{"email": email})

# log out function
def logout(request):
   global url, user
   r = requests.get("http://localhost:8080/user/sugandhi@abc.com")
   ctx = r.json()
   print ctx
   ctx['Status'] = 0
   update_user_util(ctx)
   return render_to_response('login.html')   


#
# Utility Methods
#
def update_user_util(payload):
   global url, user
   return requests.put(url + user, data=json.dumps(payload), headers=headers)
