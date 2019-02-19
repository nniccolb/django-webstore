from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    #create model Category for games
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    #user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userType = models.CharField(max_length=100) #developer or customer
    games = models.ManyToManyField('Game') #user can have games (developed or bought)
    email_confirmed = models.BooleanField(default=False) #tells wheter email confirmation is valid or not
    is_active = models.BooleanField(default=False) #after email conf is active

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        #creates userprofile
        UserProfile.objects.create(user=instance)
    if instance.username != 'admin':
        #save it to database
        instance.userprofile.save()

class Game(models.Model):
    #model for game
    category = models.ForeignKey(Category, on_delete=models.PROTECT) #game has category
    price = models.PositiveIntegerField(default=0) #games price
    title = models.CharField(max_length=100) #title (name)
    source = models.CharField(max_length=500) #source URL to game

    image = models.CharField(max_length=500) #game has image in the page
    developer = models.ForeignKey('UserProfile', on_delete=models.PROTECT, default=1) #game has user as a developer
    times_sold = models.PositiveIntegerField(default=0) #keeps count how many times sold

    def get_absolute_url(self):
        return reverse('games:index')

    def __str__(self):
        return self.title

class Score(models.Model):
    #model for counting games highscores
    game = models.ForeignKey(Game, on_delete=models.CASCADE) #current game
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE) #player playing to game
    value = models.PositiveIntegerField(default=0) #number of points

    def __str__(self):
        return self.player.user.username + " - " + str(self.value)
