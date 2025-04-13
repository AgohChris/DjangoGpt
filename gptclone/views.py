from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import openai
from openai.error import OpenAIError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json
from dotenv import load_dotenv
import os


load_dotenv()

# Create your views here.
# @login_required
def home(request):
   return render(request, "index.html")


def registerV(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password1 = request.POST.get("password2")


        

        if not (username and password and password1 and email):
                # messages.error(request, "Tous les champs sont obligatoire")
                return redirect("register")
    

        if password != password1:
                # messages.error(request, "les mots de passes ne correspondent pas") 
                return redirect("register")

            
        if User.objects.filter(username=username).exists():
                # messages.error(request, "Cet utilisateur existe déja")
                return redirect("register")

        
        if User.objects.filter(email=email).exists():
                # messages.error(request, "Cet email est déja utilisé")   
                return redirect("register")
        

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        # messages.success(request, "Succès")

       
        Objet_email = "Creation de Compte Mini Gpt"
        Corps_email = render_to_string("emails/Succes.html", {"username": username})
        
        
        message_email = EmailMessage(
            Objet_email, Corps_email, "chatminipy@gmail.com", [email]
        )
        message_email.content_subtype = "html"
        message_email.send()
        return redirect("login")
        


    return render(request, "register.html")



def loginV(request):
   if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # if not user.is_active:
            #     messages.error(request, "Votre compte n'est pas encore activé. Vérifiez votre email")
            #     return redirect("login")
            
            login(request, user)
            # messages.success(request, "Connexion réussie.")
            return redirect("home")
        # else:
        #     messages.error(request, "Erreur lor de l'authentifiaction")
              

   return render(request, "login.html")



def deconnexion(request):
    if logout(request) :
        # messages.success(request,"Déconnecté")
        return redirect("index")
    
    return render(request, "index.html")


@login_required
@csrf_exempt
def chat_avec_gtp(request):
    openai.api_key = os.getenv("OPEN_AI_KEY")
    if request.method == "POST":
        try:
            body  = json.loads(request.body)
            message = body.get("message")
            
            if not message:
                return JsonResponse({"erreur": "Message vide"}, status=400)
            
            print(f"Message reçu : {message}")

            reponse = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "systeme", "content": "Tu es l'assistant de Py"},
                    {"role": "user", "content": message}
                ]
            )
            reponsechat = reponse.choices[0].message.content
            return JsonResponse({"response": reponsechat})
        
        except OpenAIError as e:
            print(f"Erreur OpenAi: {str(e)}")
            return JsonResponse({"erreur": "Oups vous avez depasser le cota de la journée revenuez plus tart"}, status=500)
        
        except Exception as e:
            print(f"Erreur : {str(e)}")
            return JsonResponse({"erreur": str(e)}, status=500)
