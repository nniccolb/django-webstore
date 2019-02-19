
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'games'

urlpatterns = [
    #front page
    path('', login_required(views.IndexView.as_view()), name='index'),

    path('', include('django.contrib.auth.urls'), {'template_name': 'games/login.html'}),

    #for registration
    path('register/', views.Registration.as_view(), name='registration'),

    #Profile information
    path('profile/', login_required(views.profile), name='profile'),

    #See all games for a specified category
    path('<int:category_pk>/', login_required(views.DetailView.as_view()), name='categoryView'),

    #Buy the game if you haven't done so yet
    path('<int:category_pk>/<int:game_pk>/', login_required(views.checksum), name='gameView'),

    #add a new game
    path('add/', login_required(views.GameCreate.as_view()), name='game-add'),

    #Successful payment for a game
    path('<int:category_pk>/<int:game_id>/success/',login_required(views.success_payment),name='payment_success'),

    #Send account activation email to the console
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),

    #Activate the user account
    path('register/<uidb64>/<token>/', views.activate, name='activate'),

    #Save your score for a game you have been playing
    path('save/', views.save, name='save')
]
