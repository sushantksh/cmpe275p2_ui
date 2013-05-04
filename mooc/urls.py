from django.conf.urls import patterns, url

from mooc import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^home$', views.home),
    url(r'^signup$', views.signup), #Only Takes care of Loading the Sign Up HTML Page.
    url(r'^signin$', views.signin), #Only Takes care of Loading the Sign In HTML Page.
    url(r'^login$', views.login_user),
    url(r'^logout', views.logout_user),
    url(r'^profile', views.profile),
    url(r'^change_password', views.change_password),
    url(r'^enroll', views.enroll_user),

    url(r'^add_user$', views.add_user), # Handles User Sign Up Form.
    url(r'^get_user$', views.get_user),
#     url(r'^list_user$', views.list_user),
    url(r'^update_user$', views.update_user),
    url(r'^remove_user$', views.remove_user),
    url(r'^assets$', views.remove_user),    
    
    url(r'^add_course$', views.add_course),
    url(r'^get_course$', views.get_course),
    url(r'^list_course$', views.list_course),
    url(r'^update_course$', views.update_course),
    url(r'^remove_course$', views.remove_course),

    url(r'^category$', views.category),
    url(r'^add_category$', views.add_category),
    url(r'^get_category$', views.get_category),
    url(r'^list_category$', views.list_category),
    url(r'^update_category$', views.update_category),
    url(r'^remove_category$', views.remove_category),

    url(r'^add_announcement$', views.add_announcement),
    url(r'^get_announcement$', views.get_announcement),
    url(r'^list_announcement$', views.list_announcement),
    url(r'^update_announcement$', views.update_announcement),
    url(r'^remove_announcement$', views.remove_announcement),
    
    url(r'^add_discussion$', views.add_discussion),
    url(r'^get_discussion$', views.get_discussion),
    url(r'^list_discussion$', views.list_discussion),
    url(r'^update_discussion$', views.update_discussion),
    url(r'^remove_discussion$', views.remove_discussion),

    url(r'^add_quiz$', views.add_quiz),
    url(r'^get_quiz$', views.get_quiz),
    url(r'^list_quiz$', views.list_quiz),
    url(r'^update_quiz$', views.update_quiz),
    url(r'^remove_quiz$', views.remove_quiz),
)
