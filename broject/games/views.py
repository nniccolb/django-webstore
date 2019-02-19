from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Game, UserProfile, Score
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.views.generic import View
from .forms import UserForm, GameForm
from hashlib import md5
from django.core import serializers
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth.models import User

utype = None

class IndexView(generic.ListView):
    template_name = 'games/index.html'
    context_object_name = 'all_categories'

    def get_queryset(self):
        return Category.objects.all()

def profile(request):
    user = request.user.userprofile
    games = Game.objects.filter(developer=user)
    context = {
			'games': games,
    }
    return render(request, 'games/profile.html', context)

class DetailView(generic.DetailView):
    model = Category
    pk_url_kwarg='category_pk'
    template_name = 'games/categoryView.html'

class GameCreate(View):
    form_class = GameForm
    template_name = 'games/game_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user.userprofile
            game.save()
            return render(request, 'games/game_add_success.html')
        return render(request, self.template_name, {'form': form})
class Registration(View):
    form_class = UserForm
    template_name = 'games/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.cleaned_data['password']
            user.set_password(password)
            usertype = form.cleaned_data['user_type']
            user.save()
            global utype
            utype = usertype

            current_site = get_current_site(request)
            subject = 'Activate your account.'
            message = render_to_string('account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('games:account_activation_sent')

        return render(request, self.template_name, {'form': form})


def checksum(request, game_pk,category_pk):
    game = Game.objects.get(id=game_pk)
    pid = request.user.id
    sid = 'broject112'
    amount = game.price
    secret_key = 'ec5ed80e615f3d4739e689d6e24b4b81'
    unhashed = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(unhashed.encode("ascii"))
    checksum = m.hexdigest()
    scores = Score.objects.filter(game=game).order_by('-value')[:10]
    context = {
			'pid': pid,
			'sid': sid,
			'amount': amount,
			'secret_key': secret_key,
			'checksum': checksum,
			'game_id': game_pk,
			'game': game,
            'scores': scores
    }

	# sending context to payment-template
    return render(request, 'games/gameView.html', context)

def success_payment(request,game_id,category_pk):
    pid = request.GET['pid']
    ref = request.GET['ref']

    url_checksum = request.GET['checksum']

    secret_key = "5ba99a03e46a687041b16ec552bcdf9c"

    checksum_str = "pid={}&ref={}&result={}&token={}".format(pid, ref, "success", secret_key)

    m = md5(checksum_str.encode("ascii"))
    checksum = m.hexdigest()

    #buyer_id = pid.split('-')[0]
    #game_id = pid.split('-')[1]
    game = Game.objects.get(id=game_id)
    category = game.category

    current_user = request.user

    context = {
	    'game': game,
        'category': category,

    }

    if request.user.is_authenticated:
	    if url_checksum == checksum and str(current_user.id) == user_id and str(game_id) == gameid:
		    user = UserProfiles.objects.get(id=current_user.id)

    #add game to user bought games
    request.user.userprofile.games.add(game)
    game.times_sold = game.times_sold + 1

    return render(request, 'games/payment_success.html', context)

def account_activation_sent(request):
    msg = "Your account activation email has been sent to you. Please click the link provided to log in to your account"
    return HttpResponse(msg)

def activate(request, uidb64, token):


    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)


    if user is not None and account_activation_token.check_token(user, token):
        user.userprofile.email_confirmed = True
        user.is_active = True
        global utype
        user.userprofile.userType = utype
        user.save()
        login(request, user)
        return redirect('games:index')
    else:
        return render(request, 'games:categoryView')
def save(request):
    score = request.GET['score']
    user = request.GET['user']
    game = request.GET['game']
    userProf = UserProfile.objects.get(pk=user)
    gameObj = Game.objects.get(pk=game)
    Score.objects.create(game=gameObj, player=userProf, value=score)
    return HttpResponse('Score logged to database!')
