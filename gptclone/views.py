from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



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
                messages.error(request, "Tous les champs sont obligatoire")
                return redirect("register")
    

        if password != password1:
                messages.error(request, "les mots de passes ne correspondent pas") 
                return redirect("register")

            
        if User.objects.filter(username=username).exists():
                messages.error(request, "Cet utilisateur existe déja")
                return redirect("register")

        
        if User.objects.filter(email=email).exists():
                messages.error(request, "Cet email est déja utilisé")   
                return redirect("register")
        

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Succès")


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
            messages.success(request, "Connexion réussie.")
            return redirect("home")
        else:
            messages.error(request, "Erreur lor de l'authentifiaction")
              

   return render(request, "login.html")



def deconnexion(request):
    if logout(request) :
        messages.success(request,"Déconnecté")
        return redirect("index")
    
    return render(request, "index.html")



