from django.conf.urls import patterns, include, url

import mooc.views 


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home$', mooc.views.home),
    url(r'^signup$', mooc.views.signup), #Only Takes care of Loading the Sign Up HTML Page.
    url(r'^signin$', mooc.views.signin), #Only Takes care of Loading the Sign In HTML Page.
    url(r'^login$', mooc.views.login_user),
    url(r'^logout', mooc.views.logout_user),

    url(r'^add_user$', mooc.views.add_user), # Handles User Sign Up Form.
    url(r'^get_user$', mooc.views.get_user),
#     url(r'^list_user$', mooc.views.list_user),
    url(r'^update_user$', mooc.views.update_user),
    url(r'^remove_user$', mooc.views.remove_user),
    url(r'^assets$', mooc.views.remove_user),    
    
    url(r'^add_course$', mooc.views.add_course),
    url(r'^get_course$', mooc.views.get_course),
    url(r'^list_course$', mooc.views.list_course),
    url(r'^update_course$', mooc.views.update_course),
    url(r'^remove_course$', mooc.views.remove_course),

    url(r'^category$', mooc.views.category),
    url(r'^add_category$', mooc.views.add_category),
    url(r'^get_category$', mooc.views.get_category),
    url(r'^list_category$', mooc.views.list_category),
    url(r'^update_category$', mooc.views.update_category),
    url(r'^remove_category$', mooc.views.remove_category),

    url(r'^add_announcement$', mooc.views.add_announcement),
    url(r'^get_announcement$', mooc.views.get_announcement),
    url(r'^list_announcement$', mooc.views.list_announcement),
    url(r'^update_announcement$', mooc.views.update_announcement),
    url(r'^remove_announcement$', mooc.views.remove_announcement),
    
    url(r'^add_discussion$', mooc.views.add_discussion),
    url(r'^get_discussion$', mooc.views.get_discussion),
    url(r'^list_discussion$', mooc.views.list_discussion),
    url(r'^update_discussion$', mooc.views.update_discussion),
    url(r'^remove_discussion$', mooc.views.remove_discussion),

    url(r'^add_quiz$', mooc.views.add_quiz),
    url(r'^get_quiz$', mooc.views.get_quiz),
    url(r'^list_quiz$', mooc.views.list_quiz),
    url(r'^update_quiz$', mooc.views.update_quiz),
    url(r'^remove_quiz$', mooc.views.remove_quiz),
    
    
# Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin', include(admin.site.urls)),
)
