from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required # all authenticaion related things are placed inside contrib 
from .forms import UserRegistrationForm
from django.contrib.auth import login

# Create your views here.
 
def index(request):
    return render(request,'index.html')


def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

@login_required

def tweet_create(request):# three ways to handle form, 1 user fill form, 2.    3. we need to make an form
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES) # file or photo from form is came through it
         # for security measure
        if form.is_valid(): 
            tweet=form.save(commit=False) # commit =false will prevent from saving into database
            tweet.user= request.user # always a user is associated with request
            tweet.save()
            return redirect('tweet_list') # this is a standard way to handle forms in django

        

    else:
        form=TweetForm() # it will make a new form which as same as TweetForm which we defined on forms.py
    return render(request,'tweet_form.html', {'form':form})

@login_required  # it will make secure user. now you can login without login or false pages like incognitive pages
def tweet_edit(request,tweet_id):
    tweet= get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form= TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user= request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form= TweetForm(instance=tweet)
    return render(request,'tweet_form.html', {'form':form})

def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html', {'tweet':tweet})# before post request we need something to show

def register(request):
    if request.method=='POST':
        form= UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) #secure data cleaning
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html', {'form':form})