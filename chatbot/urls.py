from django.urls import path      #this allows us to specify each django url as path
from . import views

urlpatterns = [
    path('' , views.chatbot , name = 'chatbot'),   #render to chatbot.html file when file is opened  
    path('login' , views.login , name = 'login'), 
    path('register' , views.register , name = 'register'), 
    path('logout' , views.logout, name = 'logout'), 
]