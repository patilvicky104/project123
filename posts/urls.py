from django.conf.urls import url

from posts import views


app_name='posts'

urlpatterns = [
    url(r"^$", views.PostList.as_view(), name="all"),
    url(r"new/$", views.CreatePost.as_view(), name="create"),
    url(r"pdf/$",views.upload_list,name='upload_list'),
    url(r"pdf/upload/$",views.upload_pdf,name='upload_pdf'),
    # url(r"pdf/delete/<int:pk>/$", views.delete_pdf, name='delete_pdf'),

    
    url(r"by/(?P<username>[-\w]+)/$",views.UserPosts.as_view(),name="for_user"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.PostDetail.as_view(),name="single"),
    url(r"delete/(?P<pk>\d+)/$",views.DeletePost.as_view(),name="delete"),
]
