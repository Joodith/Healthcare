from django.conf.urls import url
from blog import views
app_name="blog"
urlpatterns=[
    url(r'^$',views.PostListView.as_view(),name="post_list"),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/',views.user_logout,name="logout"),
    url(r'^about/$', views.AboutView.as_view(), name="about"),
    url(r'^detail/(?P<pk>\d+)/$',views.PostDetailView.as_view(),name="post_detail"),
    url(r'^create/$',views.PostCreateView.as_view(),name="post_create"),
    url(r'^update/(?P<pk>\d+)/$',views.PostUpdateView.as_view(),name="post_edit"),
    url(r'^delete/(?P<pk>\d+)/$', views.PostDeleteView.as_view(),name="post_remove"),
    url(r'^draft/$',views.DraftListView.as_view(),name="draft_list"),
    url(r'^add_comment/(?P<pk>\d+)/$',views.add_comment_to_post,name="add_comment_to_post"),
    url(r'^comment_approve/(?P<pk>\d+)/$',views.comment_approve,name="comment_approve"),
    url(r'^comment_delete/(?P<pk>\d+)/$',views.comment_delete,name="comment_delete"),
    url(r'^post_publish/(?P<pk>\d+)/$',views.post_publish,name="post_publish"),

]