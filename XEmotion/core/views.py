from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from pymongo import MongoClient
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
from django.conf import settings
import pymongo
=======
>>>>>>> 65b620c9c2ed289b68fac01367925fb52e0ff74a

def index(request):
    return render(request, 'index.html')
#def signin(request):
   # return render(request, 'sign-in.html')

from django.shortcuts import render, redirect
from pymongo import MongoClient

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from pymongo import MongoClient

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms = request.POST.get('terms')

        # Vérifications basiques
        if not terms:
            messages.error(request, "You must agree to the Terms of Service.")
            return render(request, 'registre.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registre.html')

    #    if len(password) < 8:
      #      messages.error(request, "Password must be at least 8 characters.")
       #     return render(request, 'registre.html')

        

       
        # Connexion à MongoDB et insertion de l'utilisateur dans la collection 'users'
<<<<<<< HEAD
        client = pymongo.MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[settings.MONGO_DB]

=======
        client = MongoClient('mongodb://admin:admin123@localhost:27017/tweets_db?authSource=admin')
        db = client['tweets_db']
>>>>>>> 65b620c9c2ed289b68fac01367925fb52e0ff74a
        users_collection = db['users']

        # Préparer le document utilisateur à insérer dans MongoDB
        user_doc = {
            "username": username,
            "email": email,
            "password": password,

            # Ne jamais stocker le mot de passe en clair ! Ici, on peut stocker un hash ou un identifiant utilisateur.
            # Exemple: stocker uniquement le username et email, ou un champ ID Django si besoin
        }

        users_collection.insert_one(user_doc)

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('sign-in')

    else:
        return render(request, 'registre.html')

from pymongo import MongoClient
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

#@login_required
from datetime import datetime
from django.shortcuts import render
from pymongo import MongoClient
import pymongo
def chart(request):
    try:
<<<<<<< HEAD
        client = pymongo.MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)

=======
        client = pymongo.MongoClient(
            "mongodb://admin:admin123@host.docker.internal:27017/",
            authSource="admin",
            serverSelectionTimeoutMS=5000
        )
>>>>>>> 65b620c9c2ed289b68fac01367925fb52e0ff74a
        
        print("Test de connexion...")
        client.admin.command('ping')
        print("Connexion réussie!")
        
<<<<<<< HEAD
        db = client[settings.MONGO_DB]
=======
        db = client["tweets_db"]
>>>>>>> 65b620c9c2ed289b68fac01367925fb52e0ff74a
        print("Collections disponibles:", db.list_collection_names())
        
        # Récupération des tweets
        tweets = list(db.tweets.find().sort("_id", -1).limit(1000))  # tu peux ajuster la limite
        print(f"{len(tweets)} tweets récupérés")
        
        # Calcul des totaux de sentiments
        total = len(tweets)
        positive = negative = neutral = 0
        
        for tweet in tweets:
            sentiment = tweet.get("sentiment", "").lower()
            if "pos" in sentiment:
                positive += 1
            elif "neg" in sentiment:
                negative += 1
            else:
                neutral += 1
        
        print(f"Stats => Total: {total}, Positive: {positive}, Negative: {negative}, Neutral: {neutral}")
        
        return render(request, 'chart.html', {
            "tweets": tweets,
            "total": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
        })
        
    except Exception as e:
        print(f"ÉCHEC Connexion MongoDB: {str(e)}")
        return render(request, 'chart.html', {
            "tweets": [],
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "error": f"Impossible de se connecter à MongoDB: {str(e)}"
        })



from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from pymongo import MongoClient
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def chart_view(request):
    # Your view logic for /chart/ page
    return render(request, 'chart.html')
@csrf_protect
def signin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Connect to MongoDB using the service name 'mongodb' (for Docker)
<<<<<<< HEAD
            client = pymongo.MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            db = client[settings.MONGO_DB]
=======
            client = MongoClient('mongodb://admin:admin123@localhost:27017/tweets_db?authSource=admin')
            db = client['tweets_db']
>>>>>>> 65b620c9c2ed289b68fac01367925fb52e0ff74a
            users_collection = db['users']
            #users_collection.insert_one({"username": "admin", "password": "admin123", "email": "admin@gmail.com","image": "/static/images/im.png"})
            #users_collection.insert_one({"username": "wissal", "password": "w123", "email": "w@gmail.com"})


            # Query MongoDB to find user with matching username and password
            user = users_collection.find_one({"username": username, "password": password})

            if user:
                # Save the username in the session for logged-in state
                user_session = {
                      'username': user.get('username'),
                      'email': user.get('email'),
                      'password': user.get('password'),
                       # Optionnellement, convertir _id en string
                      'id': str(user.get('_id'))
                }
    
                request.session['username'] = user.get('username')
                request.session['user'] = user_session

                # Redirect to chart.html or any page after successful login
                return redirect('chart')  # Ensure 'chart' is the correct URL name
            else:
                # Display error message if authentication fails
                messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
                return render(request, 'sign-in.html', {'username': username})

        except Exception as e:
            print("Sign-in error:", e)
            # Display a generic error message if something goes wrong
            messages.error(request, "Une erreur interne est survenue.")
            return render(request, 'sign-in.html', {'username': '', 'error': 'Une erreur interne est survenue.'})

    # Render sign-in page if not a POST request
    return render(request, 'sign-in.html')

def logout_view(request):
    request.session.flush()  # clears all session data
    return redirect('index')
from django.shortcuts import redirect, render
from pymongo import MongoClient

def delete_account(request):
    if request.method == 'POST':
        try:
<<<<<<< HEAD
            client = pymongo.MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            db = client[settings.MONGO_DB]
=======
            client = MongoClient('mongodb://admin:admin123@localhost:27017/', authSource='admin')
            db = client['tweets_db']
>>>>>>> 65b620c9c2ed289b68fac01367925fb52e0ff74a
            users_collection = db['users']

            current_user = request.session.get('user')
            if not current_user:
                return redirect('index')

            username = current_user.get('username')
            print(f"[SUPPRESSION] Suppression de l'utilisateur : {username}")

            # Supprimer l'utilisateur de la base de données
            users_collection.delete_one({'username': username})

            # Supprimer la session
            request.session.flush()

            return redirect('index')

        except Exception as e:
            print(f"[ERREUR] Suppression compte : {e}")
            return render(request, 'parametres.html', {'error': 'Une erreur est survenue.'})
    
    return redirect('parametres')

def about_view(request):
    return render(request, 'about.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient

from django.shortcuts import render
from pymongo import MongoClient

from django.shortcuts import render, redirect
from pymongo import MongoClient

from pymongo import MongoClient

from django.shortcuts import render
from pymongo import MongoClient
from django.shortcuts import render
from pymongo import MongoClient

def parametres_view(request):
    try:
<<<<<<< HEAD
        client = pymongo.MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[settings.MONGO_DB]
=======
        client = MongoClient(
            'mongodb://admin:admin123@localhost:27017/',
            authSource='admin'
        )
        db = client['tweets_db']
>>>>>>> 65b620c9c2ed289b68fac01367925fb52e0ff74a
        users_collection = db['users']

        current_user = request.session.get('user')
        if not current_user:
            return render(request, 'parametres.html', {
                'error': 'Aucun utilisateur connecté.'
            })
        current_username = current_user['username']

        if request.method == "POST":
            # … your other fields …
            new_image = request.POST.get('image')
            print(f"[DEBUG] Posted image field: {new_image}")      # 🔍 Debug print

            # load the old record
            user = users_collection.find_one({'username': current_username})
            print(f"[DEBUG] Stored image in DB: {user.get('image')}")  # 🔍 Debug print

            update_fields = {}
            if new_image and new_image != user.get('image'):
                update_fields['image'] = new_image

            # … rest of your update logic …

            if update_fields:
                users_collection.update_one(
                    {'username': current_username},
                    {'$set': update_fields}
                )

            # reload user
            updated_user = users_collection.find_one({
                'username': update_fields.get('username', current_username)
            })

            return render(request, 'parametres.html', {
                'username': updated_user.get('username'),
                'email':    updated_user.get('email'),
                'image':    updated_user.get('image'),
                'password': updated_user.get('password'),
                'success':  'Profil mis à jour avec succès.',
            })

        else:
            user = users_collection.find_one({'username': current_username})
            print(f"[DEBUG] GET load image from DB: {user.get('image')}")  # 🔍 Debug print
            return render(request, 'parametres.html', {
                'username': user.get('username'),
                'email':    user.get('email'),
                'image':    user.get('image'),
                'password': user.get('password'),
            })

    except Exception as e:
        print(f"[ERREUR EXCEPTION] {e}")
        return render(request, 'parametres.html', {
            'error': f'Erreur : {str(e)}'
        })

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash

@csrf_exempt
@login_required
def p(request):
    if request.method == 'POST':
        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('parametres')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('parametres')

        if len(new_password) < 8:
            messages.error(request, "New password must be at least 8 characters long.")
            return redirect('parametres')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully.")
        return redirect('parametres')

    return render(request, 'parametres.html')


from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
import pymongo

from .grpc_client_ml import get_ml_sentiment

@csrf_exempt
def analyze_view(request):
    result = ""
    sentiment = ""
    score = 0.0
    tweets = []
    positive = negative = neutral = total = 0

    if request.method == 'POST':
        text = request.POST.get('search_term', '')
        num_tweets = int(request.POST.get('num_tweets', 20))

        if not text:
            result = "Aucun texte fourni."
        else:
            try:
                # Connexion à MongoDB
                client = pymongo.MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
                client.admin.command("ping")
                db = client[settings.MONGO_DB]
                filtre = {"text": {"$regex": f".*{text}.*", "$options": "i"}}
                tweets = list(db.tweets.find(filtre).sort("_id", -1).limit(num_tweets))

                # Statistiques
                for t in tweets:
                    s = t.get("sentiment", "").lower()
                    if s == "positive":
                        positive += 1
                    elif s == "negative":
                        negative += 1
                    else:
                        neutral += 1
                total = len(tweets)
                result = f"{total} tweets trouvés contenant '{text}'"

            except Exception as e:
                result = f"Erreur MongoDB : {str(e)}"

    return render(request, 'chart.html', {
        "tweets": tweets,
        "result": result,
        "text": text,
        "sentiment": sentiment,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "total": total
    })
