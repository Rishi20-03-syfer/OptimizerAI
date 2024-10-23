from PIL import Image
from django.shortcuts import render # for the html pages
from .models import Content, Expriment        # model Content to store the data
import google.generativeai as genai # google ai api     
import os
from django.utils.safestring import mark_safe
import markdown
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests
from django.core.files.base import ContentFile

try:
    genai.configure(api_key="AIzaSyD5NMUH15XM9nbZKcyePE60EliMc86owRw")
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print( f"Api key fault {e}")

response=""

@login_required(login_url="/login_page")
def index(request):
    global model, response
    
    if request.method == "POST":
        text = request.POST.get("text")
        file = request.FILES.get("file")
        image = request.FILES.get("image")
        query = Content(text=text)

        if text and not file and not image:
            query.save()
            response = mark_safe(f"{markdown.markdown(text)}<br>{forText(text)}")
        elif text and file:
            query.file.save(file.name,ContentFile(file.read()),save=True)
            response = mark_safe(f"{markdown.markdown(text)}<br>{forFile(text,file)}")
        elif text and image:
            query.image.save(image.name,ContentFile(image.read()),save=True)
            response = mark_safe(f"{markdown.markdown(text)}<br>{forImage(text,image)}")
        else:
            response = "No data provided"
    return render(request, "index2.html", context={"response": response})
def forText(text):
    response = model.generate_content(text)
    return markdown.markdown(response.text)

def forFile(text,file):
    file_path = save_inmemory_file_to_path(file)
    file_obj = genai.upload_file(file_path)
    response = model.generate_content([text,file_obj]).text
    return markdown.markdown(response)

def forImage(text,image):
    image_path = save_inmemory_image_to_path(image)
    image_obj = genai.upload_file(image_path)
    response = model.generate_content([text,image_obj]).text
    return markdown.markdown(response)

def save_inmemory_file_to_path(uploaded_file):
    save_directory = 'media/files' 
    file_path = os.path.join(save_directory, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

def save_inmemory_image_to_path(uploaded_file):
    save_directory = 'media/images' 
    file_path = os.path.join(save_directory, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

def logout_page(request):
    logout(request)
    return redirect("/login_page")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            messages.error(request,"User does not exist")
            return render(request,"login.html")
        
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"Invalid username or password")
            return render(request,"login.html")
        else:
            login(request,user)
            return redirect("/")
    return render(request,"login.html")
    
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect(reverse('register'))

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.save()

        messages.success(request, "User created successfully and you can login now")
        return redirect(reverse('login_page'))  # Redirect to login page after registration

    return render(request, "register.html")

def feedback(request):
    return render(request,"feedback.html")


def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


@login_required(login_url="/login_page")
def experiment(request):
    image_path = None
    audio_path = None

    if request.method == "POST":
        text1 = request.POST.get('text1')
        text2 = request.POST.get('text2')
        if text1:
             query_test = Expriment(text=text1)
             image_bytes = query({"inputs": text1})
             query_test.image.save("generated_image",ContentFile(image_bytes),save=True)
             image_path = query_test.image.url
        if text2:
            query_test = Expriment(text=text2)
            audio_bytes = text_to_musicBytes(text2)
            query_test.audio.save("generated_audio",ContentFile(audio_bytes),save=True)
            audio_path = query_test.audio.url
            print(audio_path)

    return render(request,"experiments.html",{"image":image_path,"audio":audio_path})

def text_to_musicBytes(text):
     API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
     headers = {"Authorization": "Bearer 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"}
     response = requests.post(API_URL, headers=headers, json={"inputs":text})
     return response.content    
   
def about(request):
    return render(request,"about.html")

def help(request):
    return render(request,"help.html")