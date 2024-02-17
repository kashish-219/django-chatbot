from django.shortcuts import render,redirect
from django.http import JsonResponse          #required for returning JsonrResponse 
import openai

from django.contrib import auth         #authentication library
from django.contrib.auth.models import User

from .models import Chat
from django.utils import timezone

openai_api_key = 'add your API key here'    #our generated key
openai.api_key = openai_api_key             #send api key to openai from openai_api_key variable

# Create your views here.

#this will send our message to open ai API
def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",                  #or "gpt-4"
            messages = [
                {"role": "system","content": "You are an helpful assistant."},
                {"role": "user","content": message},
            ]
        )
        answer = response.choices[0].message.content.strip()
        return answer 
    except openai.error.RateLimitError as e:
        print(f"RateLimitError: {e}")
        return "Sorry, I'm currently unable to process your request due to API usage limits. Please try again later."

#This will make your home page
def chatbot(request):
    chats = Chat.objects.filter(user = request.user)          #for loading chat history of user i.e returns chat of user from database
    if request.method == 'POST':        #if method is post then do something
        message = request.POST.get('message')   #message is fetched from front-end req and given to message variable
        response = ask_openai(message)

        chat = Chat(user = request.user,message = message,response = response,created_at = timezone.now())     #databse record saving
        chat.save()
        return JsonResponse({'message': message,'response': response})
    return render(request,'chatbot.html', {'chats' : chats})   #render to chatbot.html file when file is opened as well as load the history of user

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username = username,password = password)
        if user is not None:
            auth.login(request,user)
            return redirect(chatbot)
        else:
            error_message = "Invalid Username or Password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except Exception as e:
                if 'username' in str(e):
                    error_message = 'Username already exists'
                else:
                    error_message = f'Error creating account: {e}'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect(login)