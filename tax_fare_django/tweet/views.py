from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegrestrationForm
from django.shortcuts import get_object_or_404,redirect # Fetches an object from the database or returns a 404 error if it doesn’t exist.
from django.contrib.auth.decorators import login_required #login_required is used to restrict access to a view so that only authenticated (logged-in) users can access it.
from django.contrib.auth import login

def logout(request):
    return render(request,"logged_out.html")

def index(request):
    return render(request,"index.html")


def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-updated_at')
    return render(request,'tweet_list.html',{'tweets':tweets,'user':request.user})



@login_required
def tweet_create(request):
    if request.method=="POST":
        form =TweetForm(request.POST,request.FILES) #→ builds the form with submitted data (including uploaded images).
        if form.is_valid():                          #checks if the data respects the model rules (max_length, required fields, etc).
            tweet=form.save(commit=False)            #creates a Tweet object but doesn’t save to DB yet (lets you modify before saving).
            tweet.user=request.user                  #This way, the currently logged-in user is linked to the tweet.
            tweet.save()
            return redirect("tweet_list")              #→ sends the user to the list view after creation.
    else:
        form=TweetForm()
    return render(request,"tweet_form.html",{"form":form})




@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk= tweet_id,user=request.user)
    if request.method=="POST":
        form=TweetForm(request.POST,request.FILES,instance=tweet)  #tells the form that you’re editing an existing Tweet object, not creating a new one.
        if form.is_valid():                          #checks if the data respects the model rules (max_length, required fields, etc).
            tweet=form.save(commit=False)            #creates a Tweet object but doesn’t save to DB yet (lets you modify before saving).
            tweet.user=request.user                  #This way, the currently logged-in user is linked to the tweet.
            tweet.save()
            return redirect("tweet_list")   
    else:
        form=TweetForm(instance=tweet)
    return render(request,"tweet_form.html",{"form":form})





@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect("tweet_list")
    return render(request,"tweet_confirm_delete.html",{"tweet":tweet})



def register(request):
    if request.method=="POST":
        form= UserRegrestrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) #set_password() ek built-in method hai jo Django ke User model me hota hai.Iska kaam hota hai: Password ko hash (encrypt) karna.
            user.save()
            login(request,user)# imported from the liberari and autometically login the user
            return redirect('tweet_list')
    else:
        form=UserRegrestrationForm()


    return render(request,'registration/register.html',{'form':form})
### Step-by-Step Flow of Django User Registration (Hinglish me samjha hua)

# 1.                                                       **User register page open karta hai (GET request hoti hai)**
#    * Jab user registration page open karta hai, tab browser Django server ko **GET request** bhejta hai.
#    * Django code check karta hai:
#      ```python
#      if request.method == "POST":
#      ```
#      Ye condition **False** hoti hai, kyunki abhi form submit nahi hua hai.

#2. **`else` block run hota hai**
#    * Django ek **empty form** banata hai:
#      ```python
#      form = UserRegrestrationForm()
#      ```
#    * Ye blank form user ko HTML page par dikhaya jata hai taaki wo apna data fill kare.

#3. **User form fill karke “Register” button dabata hai**

#    * Ab jab user form submit karta hai, to browser ek **POST request** bhejta hai Django ko, jisme user ka data hota hai (username, password, etc.).

# 4. **Django ko POST request milti hai**

#    * Ab ye condition **True** hoti hai:

#      ```python
#      if request.method == "POST":
#      ```
#    * Django user ke submit kiye hue data ko form me daal deta hai:

#      ```python
#      form = UserRegrestrationForm(request.POST)
#      ```

# 5. **Form validation hoti hai**

#    * Django check karta hai:

#      ```python
#      if form.is_valid():
#      ```
#    * Validation me ye sab check hota hai:
#      * Kya sab required fields fill hui hain?
#      * Password1 aur Password2 same hain ya nahi?
#      * Username already exist karta hai ya nahi?

# 6. **Agar form valid hai**

#    * To Django ek **naya user object** create karta hai:

#      ```python
#      user = form.save()
#      ```
#    * Ye user ab database me save ho jata hai.

# 7. **User ko login karaya jata hai**

#    * Form valid hone ke baad Django use turant login karata hai:

#      ```python
#      login(request, user)
#      ```
#    * `login()` ka kaam hai user session create karna taaki wo logged-in rahe.

# 8. **User ko kisi page par redirect kar diya jata hai (jaise home page)**

#    * Example:

#      ```python
#      return redirect('home')
#      ```
#    * Ab user successful registration ke baad home page par pahunch jata hai.

# 9. **Agar form invalid hai**

#    * Django wapas wahi form render karta hai, jisme error messages show hote hain (jaise “username already exists” ya “passwords don’t match”).

# **In short:**
# ➡️ GET → blank form dikhao
# ➡️ POST → form validate karo
# ➡️ Valid → user banao + login karao + redirect karo
# ➡️ Invalid → error ke sath form wapas dikhao
