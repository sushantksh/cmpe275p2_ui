# Create your views here.
# Create your views here.
from django.shortcuts import render_to_response, render
# from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template import RequestContext
import json
import requests
from requests import session

url = "http://localhost:8080/" 

user = "user"
course = "course"
category = "category"
announcement = "announcement"
discussion = "discussion"
quiz = "quiz"

lst = "/list"

headers = {'content-type': 'application/json', 'charset': 'utf-8'}

#
# user
#

def add_user(request):
   global url, headers, user
   payload = '{"_id": "userid1","courseId": "courseId","questions": [{"question": "Que1","options": ["option1","option2"],"answer": "option1","point": 1},{"question": "Que2","options": ["option1","option2"],"answer":"option1","point": 1}]}'
   response = requests.post(url + user, data=json.dumps(payload), headers=headers)
   print response.text
# print response.status_code
   
def get_user(request):
   global url, headers, user
   response = requests.get(url + user +"/disid1")
   print response.json()
   
def list_user():
   global url, headers, user, lst
   response = requests.get(url + user + lst)
   print response.json()

def remove_user():
   global url, headers, user
   response = requests.get(url + user +"/disid1")
   print response.text

def update_user():
   global url, headers, user
   payload = '{"_id": "disid1",“courseId”: “courseId”,"title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}'
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text


#
# Course
#

def add_course(request):
   global url, headers, course
   payload = '{"_id":"course1","category":"annonymous_1","title":"introduction to algebra","section":2,"dept":"eng","term":"Spring","year":2013,"instructor":[{"name":"russel Doe","id":29}],"days":["Monday","Wednesday","Friday"],"hours":["8:00AM","9:15:AM"],"Description":"My course","attachment":"PATH","version":"1"}'
   response = requests.post(url + course, data=json.dumps(payload), headers=headers)
   print response.text
   
def get_course(request):
   global url, headers, course
   response = requests.get(url + course +"/course1")
   print response.json()
   
def list_course():
   global url, headers, course, lst
   response = requests.get(url + course + lst)
   print response.json()

def remove_course():
   global url, headers, course
   response = requests.get(url + course +"/course1")
   print response.text

def update_course():
   global url, headers, course
   payload = '{"_id":"course1","category":"annonymous_1","title":"machine learning","section":2,"dept":"eng","term":"Spring","year":2013,"instructor":[{"name":"russel Doe","id":29}],"days":["Monday","Wednesday","Friday"],"hours":["8:00AM","9:15:AM"],"Description":"My course","attachment":"PATH","version":"1"}'
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text
#
# Category
#

def add_category():
   global url, headers, category
   payload = '{"_id":"annonymous_1", "name":"Cooking"}'
   response = requests.post(url + category, data=json.dumps(payload), headers=headers)
   print response.text
   
def get_category(request):
   global url, headers, category
   response = requests.get(url + category +"/annonymous_1")
   print response.json()
   
def list_category():
   global url, headers, category, lst
   response = requests.get(url + category + lst)
   print response.json()

def remove_category():
   global url, headers, category
   response = requests.get(url + category +"/annonymous_1")
   print response.text

def update_category():
   global url, headers, category
   payload = '{"_id":"annonymous_1", "name":"Home Cooking"}'
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text


#
# announcement
#

def add_announcement():
   global url, headers, announcement
   payload = '{"_id": "anid1","courseId": "courseId","title": "Title","description":"desc","postDate": "04-22-2013","status": 0}'
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
   payload = '{"_id": "anid1","courseId": "courseId","title": "Title1234","description":"desc","postDate": "04-22-2013","status": 0}'
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text


#
# discussion
#

def add_discussion():
   global url, headers, discussion
   payload = '{"_id": "disid1","courseId": "course1","title": "Title","description": "desc","messages": [{"messages": "msg1","user": "user1","postDate": "04-22-2013"}, {"messages": "msg2","user": "user2","postDate":"01-22-2013"}]}'
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
   payload = '{"_id": "disid1",“courseId”: “courseId”,"title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}'
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text

#
# quiz
#

def add_quiz():
   global url, headers, quiz
   payload = '{"_id": "quizid1","courseId": "courseId","questions": [{"question": "Que1","options": ["option1","option2"],"answer": "option1","point": 1},{"question": "Que2","options": ["option1","option2"],"answer":"option1","point": 1}]}'
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
   payload = '{"_id": "disid1",“courseId”: “courseId”,"title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}'
   response = requests.put(url + course, data=json.dumps(payload), headers=headers)
   print response.text


def login(request):
   if request.POST:
      username = request.POST.get('username')
      password = request.POST.get('password')
      
   payload = {'email':username,'pwd':password}
   #with session() as c:
      #c.post('http://127.0.0.1:8000/login/', data=payload)
      #request = c.get('http://127.0.0.1:8000/login/')
      #print request.headers
      #print request.text
   
   print "Calling bottle from Django ...... from sign in HOME "
   r = requests.post("http://localhost:8080/login",data=json.dumps(payload))
   print str(r)+" ---- > Call Back from Bottle Achieved "
   ctx = r.json()
   #name = request.session['username']
   #print name
   print ctx
   
   return render_to_response("home.html",ctx,context_instance=RequestContext(request))

# Sign Up function
def signup(request):
   return render(request, 'signUp.html')

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
   #request.session['username'] = 'Sushant'
   return render_to_response("home.html",ctx,context_instance=RequestContext(request))
   #return render(request, "home.html",{"email": email})

# log out function
# def logout(request):
#    r = requests.get("http://localhost:8080/logout/:email",data=json.dumps(payload))
#    print str(r)+" ---- > Call Back from Bottle Achieved "
#    ctx = r.json()
#    print ctx
#    return render_to_response("login.html",ctx,context_instance=RequestContext(request))   

