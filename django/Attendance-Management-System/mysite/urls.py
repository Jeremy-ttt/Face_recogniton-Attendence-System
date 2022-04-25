
from django.conf.urls import url
from django.contrib import admin
from app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^register_verify/', views.register_verify),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    url(r'^check/', views.check),
    url(r'^classManage/', views.classManage),
    url(r'^edit_class', views.edit_class),
    url(r'^delete_class', views.delete_class),
    url(r'^add_class/', views.add_class),
    url(r'^majorManage/', views.majorManage),
    url(r'^add_major/', views.add_major),
    url(r'^delete_major', views.delete_major),
    url(r'^edit_major/', views.edit_major),
    url(r'^memberManage/', views.member_manage),
    url(r'^delete_member', views.delete_member),
    url(r'^edit_member', views.edit_member),
    url(r'^total', views.total),
    url(r'^sign_solve/', views.total),
    url(r'^notice/', views.notice),
    url(r'^noticeManage/', views.noticeManage),
    url(r'^leave/', views.leave),
    # url(r'^exam/',views.exam),
    # url(r'^exam_manage/',views.exam_manage),
    url(r'^change_pwd/', views.change_pwd),
]
