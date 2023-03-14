from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
 path('', views.PostList.as_view(), name='home'),
  path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
  path('register/',views.signup,name='register'),
 path("login/", views.login_request, name="login"),
path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
  path('profile/', views.profile, name='users-profile'),

path('add_blogs/',views.add_blogs,name='Add_Blogs'),
 path('blogpost-like/<int:pk>', views.BlogPostLike, name="blogpost_like"),
path("logout/", views.logout_request, name= "logout"),
path('post/<slug:slug>/update', views.updatePost, name='blog-update'),
path('post/<slug:slug>/delete', views.deletePost, name='blog-delete'),
    
          ] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
