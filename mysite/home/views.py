from django.shortcuts import render ,HttpResponse , redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post
# Create your views here.
def home(request):
    return render(request,'home/home.html')

def contact(request):
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<4 or len(email)<5 or len(phone)<10 or len(content)<5:
            messages.error(request, 'Please fill the form correctly')
            return render(request,'home/contact.html')
        else:
            ct = Contact(name=name,email=email,phone=phone,content=content)
            ct.save()
            messages.success(request, "Your Message has been successfully sent")
            return render(request,'home/contact.html')
    else:
        return render(request,'home/contact.html')

def about(request):
    #messages.success(request, 'Welcome to About')
    return render(request,'home/about.html')

def viewprofile(request):
    if request.method == 'POST':
        id = request.POST['id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        userdata = User.objects.get(id=id)
        userdata.first_name = first_name
        userdata.last_name = last_name
        userdata.email = email
        userdata.save()
        messages.success(request, "Your Profile Updated successfully.")
    user = request.user
    profile = User.objects.filter(username=user)
    context = {'profile' : profile}
    return render(request,'home/viewprofile.html',context)

def change_password(request):
    if request.method == 'POST':
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        confirm_pass = request.POST['confirm_pass']
        user = request.POST['user']
        profile = User.objects.filter(username=user)
        oldps = User.objects.check_password(old_pass)
        for i in profile:
            pawd = i.password
        print(pawd)
    return render(request,'home/change_password.html')

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostTitle.union(allPostContent)
    if allPosts.count ==0:
        messages.warning(request,"No search results found. Please refine your query.")
    params = {'allPosts':allPosts, 'query':query}
    return render(request,'home/search.html',params)



def handleSignup(request):
    if request.method == 'POST':
        # This is all parameter
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for errorenous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters.")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username should only cantain letters and number.")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Your Password do not match.")
            return redirect('home')

        # Create the user

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name= firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "Your account has been successfulliy created.")
        return redirect('home')
    else:
        return HttpResponse('404- Not Found')


def loginhandle(request):
    if request.method == 'POST':
        #GET the all parameter
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(request,username=loginusername, password=loginpass)

        if user:
            login(request,user)
            messages.success(request,'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials , PLease Try again.')
            return redirect('home')
    return HttpResponse('Login')




def userlogout(request):
    logout(request)
    #messages.success(request,'Successfully Logged out')
    return redirect('/')