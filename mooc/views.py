# Create your views here.

from django.shortcuts import render_to_response
#from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from mooc.models import MOOC
from time import localtime, strftime
from cStringIO import StringIO

import json
import requests

#modules
course = "course"
category = "category"
announcement = "announcement"
discussion = "discussion"
message = "message"
quiz = "quiz"

#global variables
headers = {'content-type': 'application/json', 'charset': 'utf-8'}

latest_mooc_list = None
default_mooc = None

#dictionary to store user selected options
#example 
#dict = { "user1": { "url":"http://localhost:8080", "mooc":{"id":"id1", "name:"myMooc"}, "course": {"id": "id1", "name": "myCourse"}, 
#                    "category": {"id": "id1", "name": "myCategory"}, "discussion": {"id": "id1", "name": "mydiscussion"}, 
#                    "announcement": {"id": "id1", "name": "myAnnouncement"}, "quiz": {"id": "id1","name": "myQuiz"}
#                  },
#         "user2": { "url":"http://localhost:8080", "mooc":{"id":"id1", "name:"myMooc"}, "course": {"id": "id1", "name": "myCourse"}, 
#                    "category": {"id": "id1", "name": "myCategory"}, "discussion": {"id": "id1", "name": "mydiscussion"}, 
#                    "announcement": {"id": "id1", "name": "myAnnouncement"}, "quiz": {"id": "id1","name": "myQuiz"}
#                  }
#       }
#to access:
#    data = dict["user1"]
#    print data["category"]["id"]
#    OR
#    print dict["user1"]["category"]["id"]
user_dict = {}

# store mooc
def store_mooc():
    global latest_mooc_list, default_mooc, headers, user_dict
   
    latest_mooc_list = MOOC.objects.all()
    for mooc in latest_mooc_list :
        if mooc.is_default :
            print 'mooc Primary URL ===>', mooc.group
            default_mooc = mooc
            break    
    print 'default_mooc Primary URL ===>', default_mooc.group

# index function
def index(request):
    store_mooc()
    return render_to_response("login.html")

# Sign-Up function
def signup(request):
    return render_to_response("signup.html")

# add user
def add_user(request):
    global latest_mooc_list, default_mooc, headers, user_dict
   
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
     
    payload = {"email":email, "own":[], "enrolled":[], "quizzes":[]} 
    tempUrl = default_mooc.primary_URL + "/user"
    print 'add_user.URL ===>', tempUrl
    response = requests.post(tempUrl, data=json.dumps(payload), headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        data = response.json()
        print 'add_user.data ===>', data
        ctx = {"message" : "User successfully registered, please login to continue."}
        return render_to_response("login.html",ctx)
    
    ctx = {"message" : "Sign Up Failed. Please Try Again"}
    return render_to_response("signup.html", ctx)

def get_context(request, msg=None):
    global latest_mooc_list, default_mooc, headers, user_dict
    ctx = {"fName": request.user.first_name, "lName": request.user.last_name, "latest_mooc_list": latest_mooc_list, "selectedMooc": user_dict[request.user.username]["mooc"]["name"]}
    if(msg is not None):
        ctx["message"] = msg
    if(user_dict.has_key(request.user.username)):        
        temp_dict = user_dict[request.user.username]
        if(temp_dict.has_key("course")):
            ctx["course_id"] = user_dict[request.user.username]["course"]["id"]
            ctx["course_name"] = user_dict[request.user.username]["course"]["name"]
        if(temp_dict.has_key("category")):        
            ctx["category_id"] = user_dict[request.user.username]["category"]["id"]
            ctx["category_name"] = user_dict[request.user.username]["category"]["name"]
        if(temp_dict.has_key("discussion")):        
            ctx["discussion_id"] = user_dict[request.user.username]["discussion"]["id"]
            ctx["discussion_name"] = user_dict[request.user.username]["discussion"]["name"]
        if(temp_dict.has_key("announcement")):        
            ctx["announcement_id"] = user_dict[request.user.username]["announcement"]["id"]
            ctx["announcement_name"] = user_dict[request.user.username]["announcement"]["name"]
        if(temp_dict.has_key("quiz")):        
            ctx["quiz_id"] = user_dict[request.user.username]["quiz"]["id"]
            ctx["quiz_name"] = user_dict[request.user.username]["quiz"]["name"]          
    return ctx

# User login related stuff
def login_user(request):
    global latest_mooc_list, default_mooc, headers, user_dict
   
    store_mooc()
    email = request.POST['email']
    password = request.POST['password']
   
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
#            user logged in successfully, now we need to start tracking his selections
#            delect any previous selections of this user if present
            if(user_dict.has_key(user.username)):
                del user_dict[user.username]; # remove entry with key 'Name'
#            create empty entry in dictionary so that we can add user selections later
            user_dict[user.username] = {"url": default_mooc.primary_URL, "mooc":{"id":default_mooc.id, "name":default_mooc.group}}
            ctx = get_context(request)
            return render_to_response("home.html",ctx)
        else: 
            # Return a 'disabled account' error message
            ctx = {"message" :"Login disabled. Please Contact Administrator"}
            return render_to_response("login.html",ctx)
    else:
        ctx = {"message" :"Login Failed. Please try Again"}
        return render_to_response("login.html",ctx)
# home page
def home(request):
    global latest_mooc_list, default_mooc, headers, user_dict
   
    mooc_id = request.GET.get('id')
    if mooc_id is not None :
        selected_mooc = MOOC.objects.get(pk=mooc_id)
        user_dict[request.user.username]["url"] = selected_mooc.primary_URL
        user_dict[request.user.username]["mooc"] = {"id":selected_mooc.id, "name":selected_mooc.group}

    print 'Users Primary URL ===>', user_dict[request.user.username]["url"]
    ctx = get_context(request)
    return render_to_response('home.html',ctx)

# user profile - We should show list of course user owns as well as enrolled here. It should be complete userprofile page
def profile(request):
    ctx = get_context(request)
    return render_to_response("profile.html",ctx)

def update_user(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    
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

    ctx = get_context(request)
    return render_to_response('home.html',ctx)
     
# log out function
def logout_user(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    if(user_dict.has_key(request.user.username)):
        del user_dict[request.user.username]; # remove entry with key 'Name'
    
    logout(request)
    return index(request)

# list category
def list_category(request, msg=''):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    ctx = get_context(request, msg)    
    
    file_str = StringIO()
    file_str.write(user_dict[request.user.username]["url"])
    file_str.write('/category/list')
    
    tempUrl = file_str.getvalue()
    print 'list_category.URL ===>', tempUrl
    response = requests.get(tempUrl)
    if response.status_code == 200:
        data = response.json()
        print 'list_category:data ===>', data
        ctx["category_list"] = data["list"]

    return render_to_response("categories.html",ctx)

# show category add / edit page
def category(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    ctx = get_context(request)
    ctx["id"] = "-1"
    name = request.GET.get('id')
    if name is not None:
        file_str = StringIO()
        file_str.write(user_dict[request.user.username]["url"])
        file_str.write('/category/')
        file_str.write(name)
        
        tempUrl = file_str.getvalue()
        print 'category.URL ===>', tempUrl
        response = requests.get(tempUrl)
        if response.status_code == 200:
            data = response.json()
            print 'category:data ===>', data
            ctx["id"] = data["id"]
            ctx["name"] = data["name"]
            ctx["desc"] = data["description"]
    
    return render_to_response("category_add.html",ctx)

# add/edit category form submit request
def add_category(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    cat_id = request.POST.get('catId')
    name = request.POST.get('catName')
    desc = request.POST.get('catDesc')
   
    if cat_id == "-1" :
        data = {"name":name, "description":desc, "createDate":strftime("%Y-%m-%d %H:%M:%S", localtime()), "status":0}    
    else:
        data = {"_id":cat_id, "name":name, "description":desc, "createDate":strftime("%Y-%m-%d %H:%M:%S", localtime()), "status":0} 
    print 'add_category:data ===>', data

    file_str = StringIO()
    file_str.write(user_dict[request.user.username]["url"])
    file_str.write('/category')
    
    tempUrl = file_str.getvalue()
    print 'add_category.URL ===>', tempUrl
    response = requests.post(tempUrl, json.dumps(data), headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        if cat_id == "-1" :
            data = response.json()
            print 'category:data ===>', data            
            return list_category(request, "Category added!!!")
        else:
            return list_category(request, "Category edited!!!")
    
    ctx = get_context(request, "Failed to add Category")
    ctx["id"] = data["id"]
    ctx["name"] = data["name"]
    ctx["desc"] = data["description"]    
    
    return render_to_response("category_add.html",ctx)
    
def remove_category(request):
    global latest_mooc_list, default_mooc, headers, user_dict
   
    name = request.GET.get('id')
    if name is not None and name != "-1" :
        file_str = StringIO()
        file_str.write(user_dict[request.user.username]["url"])
        file_str.write('/category/')
        file_str.write(name)        
        
        tempUrl = file_str.getvalue()
        print 'remove_category.URL ===>', tempUrl
        response = requests.delete(tempUrl)
        if response.status_code == 200:
            return list_category(request, "Category removed!!!")

    return list_category(request, "Failed to remove category!!")    
    
# build list of courses owned and enrolled for this mooc by logged in user
# this is required so that we can allow only owner to edit/delete course and drop if already enrolled    
def fetch_user(request, ctx):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    file_str = StringIO()
    file_str.write(default_mooc.primary_URL)
    file_str.write('/user/')
    file_str.write(request.user.username)
    
    tempUrl = file_str.getvalue()
    print 'fetch_user.URL ===>', tempUrl
    response = requests.get(tempUrl)
    if response.status_code == 200:
        data = response.json()
        print 'fetch_user:data ===>', data
        
        ctx["courses_own"] = data["own"]
        ctx["courses_enrolled"] = data["enrolled"]
    
# fetch course list for selected category and show them   
def list_course(request, msg=''):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    ctx = get_context(request, msg)
    ctx["course_list"] = []
    
    file_str = StringIO()
    file_str.write(user_dict[request.user.username]["url"])
    file_str.write('/course/list')

    name = request.GET.get('id')
    if name is not None and name != "-1" :
        user_dict[request.user.username]["category"] = {"id": name, "name":request.GET.get('name')}
        
        file_str.write("/")
        file_str.write(name)
   
    tempUrl = file_str.getvalue()
    print 'list_course.URL ===>', tempUrl
    response = requests.get(tempUrl)
    if response.status_code == 200:
        data = response.json()
        print 'category_course:data ===>', data
        ctx["course_list"] = data["list"]
        
#    build list of courses enrolled and owned for this mooc
    fetch_user(request, ctx)
    return render_to_response("courses.html",ctx)

# show course add / edit page
def course(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    ctx = get_context(request)
    ctx["id"] = "-1"
    ctx["instructor"] = request.user.username
    name = request.GET.get('id')
    if name is not None:
        file_str = StringIO()
        file_str.write(user_dict[request.user.username]["url"])
        file_str.write('/course/')
        file_str.write(name)
        
        tempUrl = file_str.getvalue()
        print 'course.URL ===>', tempUrl
        response = requests.get(tempUrl)
        if response.status_code == 200:
            data = response.json()
            print 'course:data ===>', data
            ctx["id"] = data["id"]
            ctx["title"] = data["title"]
            ctx["category"] = data["category"]
            ctx["section"] = data["section"]
            ctx["dept"] = data["dept"]
            ctx["term"] = data["term"]
            ctx["days"] = data["days"]
            ctx["description"] = data["description"]
            ctx["attachment"] = data["attachment"]
    
    ctx["category_list"] = []
    file_str = StringIO()
    file_str.write(user_dict[request.user.username]["url"])
    file_str.write('/category/list')
    
    tempUrl = file_str.getvalue()
    print 'course.list_category.URL ===>', tempUrl
    response = requests.get(tempUrl)
    if response.status_code == 200:
        data = response.json()
        print 'list_category:data ===>', data
        ctx["category_list"] = data["list"]    
    
    return render_to_response("course_add.html",ctx)

#
# Course
#
# @login_required(login_url='login') -- > Good to have, need to figure out usage.
def add_course(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    data = {} 
    
    course_id = request.POST.get('courseId')
    if course_id is not None and course_id != "-1" :
        data["_id"] = course_id
    data["category"] = request.POST.get("category")
    data["title"] = request.POST.get("title")
    data["dept"] = request.POST.get("dept")
    data["section"] = request.POST.get("section")
    data["term"] = request.POST.get("term")
    data["instructor"] = request.user.username
    data["days"] = request.POST.get("days")
    data["description"] = request.POST.get("description")
    data["attachment"] = request.POST.get("attachment")
    data["hours"] = ["8:00AM","9:15:AM"]
    data["version"] = "1"

    print 'add_course:data ===>', data
    
    file_str = StringIO()
    file_str.write(user_dict[request.user.username]["url"])
    file_str.write('/course')
    
    tempUrl = file_str.getvalue()
    print 'add_course.URL ===>', tempUrl
    response = requests.post(tempUrl, json.dumps(data), headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        res_data = response.json()
        print 'add_course:data ===>', res_data
        if course_id == "-1" :
            # Now we need to add course to user object
            file_str = StringIO()
            file_str.write(default_mooc.primary_URL)
            file_str.write('/user/')
            file_str.write(request.user.username)
    
            tempUrl = file_str.getvalue()
            print 'add_course.fetch_user.URL ===>', tempUrl
            user_response = requests.get(tempUrl)
            if user_response.status_code == 200:
                user_data = user_response.json()
                print 'add_course.fetch_user:data ===>', user_data
            
                own_course = user_dict[request.user.username]["mooc"]["name"] + ":" + res_data["id"]
                user_data["own"].append(own_course)
    
                tempUrl = default_mooc.primary_URL + "/user"
                user_update_response = requests.post(tempUrl, data=json.dumps(user_data), headers=headers)
                if user_update_response.status_code == 200:
                    user_update_data = user_update_response.json()
                    print 'add_course.update_user:data ===>', user_update_data
                    # TODO - what to do if add to user fails
                return list_course(request, "Course added!!!")
        else:
            return list_course(request, "Course edited!!!")
    
    ctx = get_context(request, "Failed to add Course")
    ctx["id"] = data["id"]
    ctx["instructor"] = request.user.username
    ctx["title"] = data["title"]
    ctx["category"] = data["category"]
    ctx["dept"] = data["dept"]
    ctx["section"] = data["section"]
    ctx["term"] = data["term"]
    ctx["days"] = data["days"]
    ctx["description"] = data["description"]
    ctx["attachment"] = data["attachment"]    
    
    return render_to_response("course_add.html",ctx)    

def remove_course(request):
    global latest_mooc_list, default_mooc, headers, user_dict
   
    name = request.GET.get('id')
    if name is not None and name != "-1" :
        file_str = StringIO()
        file_str.write(user_dict[request.user.username]["url"])
        file_str.write('/course/')
        file_str.write(name)        
        
        tempUrl = file_str.getvalue()
        print 'remove_course.URL ===>', tempUrl
        response = requests.delete(tempUrl)
        if response.status_code == 200:
            data = response.json()
            print 'remove_course:data ===>', data            
            # Now we need to remove course from user object
            file_str = StringIO()
            file_str.write(default_mooc.primary_URL)
            file_str.write('/user/')
            file_str.write(request.user.username)
    
            tempUrl = file_str.getvalue()
            print 'remove_course.fetch_user.URL ===>', tempUrl
            user_response = requests.get(tempUrl)
            if user_response.status_code == 200:
                user_data = user_response.json()
                print 'remove_course.fetch_user:data ===>', user_data
            
                own_course = user_dict[request.user.username]["mooc"]["name"] + ":" + name
                try:
                    user_data["own"].remove(own_course)
                    tempUrl = default_mooc.primary_URL + "/user"
                    user_update_response = requests.post(tempUrl, data=json.dumps(user_data), headers=headers)
                    if user_update_response.status_code == 200:
                        user_update_data = user_update_response.json()
                        print 'remove_course.update_user:data ===>', user_update_data                    
                except:
                    print 'remove_course.remove_from_user ===> failed'

            return list_course(request, "Course removed!!!")
    return list_course(request, "Failed to remove course!!")  

def get_course(request):
    name = request.GET.get('id')
    if name is not None:
        return view_course(request, name)
    return 

def view_course(request, course_id):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    ctx = get_context(request)
    #    build list of courses enrolled and owned for this mooc
    fetch_user(request, ctx)
    
    ctx["instructor"] = request.user.username

    file_str = StringIO()
    file_str.write(user_dict[request.user.username]["url"])
    file_str.write('/course/')
    file_str.write(course_id)
    
    tempUrl = file_str.getvalue()
    print 'get_course.URL ===>', tempUrl
    response = requests.get(tempUrl)
    if response.status_code == 200:
        data = response.json()
        print 'get_course:data ===>', data
        ctx["id"] = data["id"]
        ctx["title"] = data["title"]
        ctx["category"] = data["category"]
        ctx["section"] = data["section"]
        ctx["dept"] = data["dept"]
        ctx["term"] = data["term"]
        ctx["days"] = data["days"]
        ctx["description"] = data["description"]
        ctx["attachment"] = data["attachment"]
        ctx["enrolled"] = False
        
        courses_enrolled = ctx["courses_enrolled"]
        if(courses_enrolled):
            enroll_course = user_dict[request.user.username]["mooc"]["name"] + ":" + ctx["id"]
            for course_name in courses_enrolled:
                if( course_name == enroll_course ):
                    ctx["enrolled"] = True
                    break
    
        file_str = StringIO()
        file_str.write(user_dict[request.user.username]["url"])
        file_str.write('/category/')
        file_str.write(ctx["category"])
        
        tempUrl = file_str.getvalue()
        print 'get_course.get_category.URL ===>', tempUrl
        response = requests.get(tempUrl)
        if response.status_code == 200:
            data = response.json()
            print 'get_course.get_category:data ===>', data
            ctx["category"] = data["name"]    
    
    return render_to_response("course_view.html",ctx)   

# enroll user
def enroll_course(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    name = request.GET.get('id')
    if name is not None:
        # Now we need to enroll course for user object
        file_str = StringIO()
        file_str.write(default_mooc.primary_URL)
        file_str.write('/user/')
        file_str.write(request.user.username)
    
        tempUrl = file_str.getvalue()
        print 'enroll_user.fetch_user.URL ===>', tempUrl
        response = requests.get(tempUrl)
        if response.status_code == 200:
            data = response.json()
            print 'enroll_user.fetch_user:data ===>', data
        
            enroll_course = user_dict[request.user.username]["mooc"]["name"] + ":" + name
            try:
                data["enrolled"].append(enroll_course)
                tempUrl = default_mooc.primary_URL + "/user"
                user_update_response = requests.post(tempUrl, data=json.dumps(data), headers=headers)
                if user_update_response.status_code == 200:
                    user_update_data = user_update_response.json()
                    print 'enroll_user.update_user:data ===>', user_update_data                    
            except:
                print 'enroll_user.append_to_user ===> failed'    
    else:
        print 'enroll_user ===> failed'  
        return list_course(request, "Course not found!!!")
    return view_course(request, name)

# enroll user
def drop_course(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    
    name = request.GET.get('id')
    if name is not None:
        # Now we need to enroll course for user object
        file_str = StringIO()
        file_str.write(default_mooc.primary_URL)
        file_str.write('/user/')
        file_str.write(request.user.username)
    
        tempUrl = file_str.getvalue()
        print 'drop_course.fetch_user.URL ===>', tempUrl
        response = requests.get(tempUrl)
        if response.status_code == 200:
            data = response.json()
            print 'drop_course.fetch_user:data ===>', data
        
            enroll_course = user_dict[request.user.username]["mooc"]["name"] + ":" + name
            try:
                data["enrolled"].remove(enroll_course)
                tempUrl = default_mooc.primary_URL + "/user"
                user_update_response = requests.post(tempUrl, data=json.dumps(data), headers=headers)
                if user_update_response.status_code == 200:
                    user_update_data = user_update_response.json()
                    print 'drop_course.update_user:data ===>', user_update_data                    
            except:
                print 'drop_course.remove_from_user ===> failed'    
    else:
        print 'drop_course ===> failed'    
        return list_course(request, "Course not found!!!")
    return view_course(request, name)    

#
# announcement
#
def add_announcement(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    payload = {"_id": "anid1","courseId": "courseId","title": "Title","description":"desc","postDate": "04-22-2013","status": 0}
    response = requests.post(user_dict[request.user.username]["url"] + announcement, data=json.dumps(payload), headers=headers)
    print response.text
   
def get_announcement(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + announcement +"/anid1")
    print response.json()
   
def list_announcement(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + announcement + "/list")
    print response.json()

def remove_announcement(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + announcement +"/anid1")
    print response.text

def update_announcement(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    payload = {"_id": "anid1","courseId": "courseId","title": "Title1234","description":"desc","postDate": "04-22-2013","status": 0}
    response = requests.put(user_dict[request.user.username]["url"] + course, data=json.dumps(payload), headers=headers)
    print response.text


#
# discussion
#

def add_discussion(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    payload = {"_id": "disid1","courseId": "course1","title": "Title","description": "desc","messages": [{"messages": "msg1","user": "user1","postDate": "04-22-2013"}, {"messages": "msg2","user": "user2","postDate":"01-22-2013"}]}
    response = requests.post(user_dict[request.user.username]["url"] + discussion, data=json.dumps(payload), headers=headers)
    print response.text
   
def get_discussion(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + discussion +"/disid1")
    print response.json()
   
def list_discussion(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + discussion + "/list")
    print response.json()

def remove_discussion(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + discussion +"/disid1")
    print response.text

def update_discussion(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    payload = {"_id": "disid1","courseId": "courseId","title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}
    response = requests.put(user_dict[request.user.username]["url"] + course, data=json.dumps(payload), headers=headers)
    print response.text

#
# quiz
#

def add_quiz(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    payload = {"_id": "quizid1","courseId": "courseId","questions": [{"question": "Que1","options": ["option1","option2"],"answer": "option1","point": 1},{"question": "Que2","options": ["option1","option2"],"answer":"option1","point": 1}]}
    response = requests.post(user_dict[request.user.username]["url"] + quiz, data=json.dumps(payload), headers=headers)
    print response.text
   
def get_quiz(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + quiz +"/disid1")
    print response.json()
   
def list_quiz(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + quiz + "/list")
    print response.json()

def remove_quiz(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    response = requests.get(user_dict[request.user.username]["url"] + quiz +"/disid1")
    print response.text

def update_quiz(request):
    global latest_mooc_list, default_mooc, headers, user_dict
    payload = {"_id": "disid1","courseId": "courseId","title": "Title","description": "desc","messages": [{"messages": "msg1234","user": "user1","postDate": "DATE"},{"messages": "msg2","user": "user2","postDate": "DATE"}]}
    response = requests.put(user_dict[request.user.username]["url"] + course, data=json.dumps(payload), headers=headers)
    print response.text