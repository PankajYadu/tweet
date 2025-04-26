
from django.shortcuts import render,redirect,get_object_or_404
from .models import Tweet                         #Tweet is model class name
from .forms import TweetForm,UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now,localtime    #import for current time
from datetime import timedelta          #import for timecalculatiom

def all_tweet(request):
    tweets = Tweet.objects.all().order_by('-created_at')                 #(from model -"Tweet" object is getting data by object.all())
    for tweet in tweets:
        tweet_time_diff = now() - tweet.created_at                     # from models.py created_at
        if tweet_time_diff < timedelta(hours=100):
            if tweet_time_diff < timedelta(minutes=1):
                tweet_time_diff_seconds = tweet_time_diff.seconds
                tweet.time_ago = f"{tweet_time_diff_seconds} seconds ago"
            elif tweet_time_diff < timedelta(hours = 1):
                minutes= tweet_time_diff.seconds // 60
                tweet.time_ago = f"{minutes} minutes ago"
            else:
                tweet.time_ago = f"{tweet_time_diff.seconds // 3600} hours ago"
        else:
             tweet.time_ago = None
        tweet.was_edited = (tweet.updated_at - tweet.created_at) > timedelta(seconds=1)

        #print(f'tweet: {tweet}')
        #print(f"User: {tweet.user.username} | Tweet: {tweet.text} | Created at: {tweet.created_at}")
    return render(request, 'base.html',{'tweets':tweets} )

@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES)   #this is form variable is new filled up form as a new tweet 
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.user = request.user         # request holds the user which is currently loged in
            new_tweet.save()
        return redirect('base')                  #as base.html has name = base and this is redirecting to base.html as all_tweet list will be shown there
    else:
        form = TweetForm()                   # varna blank form milega usko if condition  m bhar denge
        return render(request,'tweet_form.html',{'form':form})

def edit_tweet(request,tweet_id):
    editable_tweet = get_object_or_404(Tweet,pk=tweet_id,user=request.user)
                                                                               # Print the current tweet time details before editing
                                                                               # Add a print statement to check if editable_tweet is being fetched
    print(f"Editable tweet fetched: {editable_tweet}")                                # <-- Debugging

                                                                                 # Print the current tweet time details before editing
    print(f"Before edit: created_at = {editable_tweet.created_at}, updated_at = {editable_tweet.updated_at}")
    if request.method == 'POST':                                                    #iska matlb hi thi h ki form m data aya h 
        editable_form = TweetForm(request.POST,request.FILES,instance=editable_tweet)  # The form gets populated with the existing tweet data for editing and isntance is with existing data form
        if editable_form.is_valid():
            editable_tweet=editable_form.save(commit=False)                          #######abhi database m save nhi krwaya h taki user edit kr sake
            editable_tweet.save()                                                   #######now updated tweet is saved
                                                                                        #print(f"After edit: created_at = {localtime(editable_tweet.created_at)}, updated_at = {localtime(editable_tweet.updated_at)}")
        messages.success(request, 'Your tweet has been updated successfully!')
        return redirect('base')                                                #as base.html has name = base and this is redirecting to base.html as all_tweet list will be shown there
    else:
        editable_form = TweetForm(instance=editable_tweet)         #  ye khali form h 
    return render(request,'edit_tweet.html',{'editable_form':editable_form})

##################################################################################################################
# Stage	  What’s Happening	                                                Handled By
# 1.      Show the form to the user	Pre-fill form with existing tweet data	else block
# 2.      User submits edited form	Validate and save the updated tweet	    if request.method == 'POST' block
###################################################################################################################

def delete_tweet(request,tweet_id):
    deletable_tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
   
    print(deletable_tweet) 
    if request.method == 'POST':
        deletable_tweet.delete()
        messages.success(request, 'Tweet deleted successfully!')
        return redirect('base')
       
    return render(request,'delete_tweet.html',{'deletable_tweet':deletable_tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])       # Make sure to hash the password
            user.save()                                             # Save user to the database
            login(request,user)                                     # Log the user in after registration
            return redirect('base')                                 # Redirect to a page like the homepage or dashboard
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_page(request):
    if request.method == 'POST':                                      #there is button in base.html which will send post request and satisfy this condition
                                                                       # Log the user out and redirect to the home page or login page
        logout(request)
        return redirect('base')  
    
    return render(request, 'logout.html')                              # Render the logout template