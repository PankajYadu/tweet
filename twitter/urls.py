from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', lambda request: redirect('base'), name='home'),    #name home can be used as {% url 'home' %} → / When the browser visits /, Django redirects to the URL named 'base' (which might be /base/)


    path('base/',views.all_tweet, name = 'base'),
    path('create/',views.create_tweet,name ='create'), # this name "create will be used in url in templates in htmlfiles"
    path('edit/<int:tweet_id>',views.edit_tweet,name ='edit'),
    path('delete/<int:tweet_id>',views.delete_tweet,name ='delete'),
    path('register/',views.register,name ='register'),
    path('accounts/logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
