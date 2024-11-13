from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import Post,Title,Message
from .form import PostForm
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django import forms



def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    
    posts =Post.objects.filter(Q(title__name__icontains=q)|
                               Q(name__icontains=q)|
                               Q(description__icontains=q))
    titles= Title.objects.all()
    post_count=posts.count()
    
    comments = Message.objects.filter(Q(post__title__name__icontains=q))
    
    
    context = {'posts':posts,'titles':titles,'post_count':post_count,'comments':comments}
    return render(request,'base/home.html',context)

def post(request,pk):
    post=Post.objects.get(id=pk)
    comments= post.message_set.all()
    participants=post.participant.all()
    
    if request.method=='POST':
        comment=Message.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        post.participant.add(request.user)
        return redirect('post',pk=post.id)
        
    context = {'post':post,'comments':comments,'participants':participants}
    return render(request,'base/post.html',context)

@login_required(login_url='login')
def createPost(request):
    form=PostForm()
    title=Title.objects.all()
    if request.method == 'POST':
        titleName=request.POST.get('title')
        titles, created=Title.objects.get_or_create(name=titleName)
        Post.objects.create(
            user=request.user,
            title= titles,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            
        )
        
        return redirect('home')
    else:
        form = PostForm()  

    context = {'form': form,'title':title}
    return render(request, 'base/form.html', context)


@login_required (login_url='login')
def updatePost(request,pk):
    post=Post.objects.get(id=pk)
    form =PostForm(instance=post)
    # title=Title.objects.get(id=pk)
    if request.user !=post.user:
        return HttpResponse("Not allowed!!")
    
    if request.method=='POST':
        titleName=request.POST.get('title')
        titles, created=Title.objects.get_or_create(name=titleName)
        post.name=request.POST.get('name')
        post.title=titles
        post.description=request.POST.get('description')
        post.save()
        return redirect('home')
    context={'form':form,'post':post}
    return render (request,'base/form.html',context)

@login_required (login_url='login')  
def deletePost(request,pk):
    
    post=Post.objects.get(id=pk)
    if request.user !=post.user:
        return HttpResponse("Not allowed!!")
    if request.method=='POST':
        post.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':post})

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
            
        except:
            messages.error(request,"User doesn't exist")
            
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password is not correct')
    context={'page':page}
    return render(request,'base/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Registration Error')
    return render (request,'base/login.html',{'form':form})

@login_required (login_url='login')  
def deleteComment(request,pk):
    post=Message.objects.get(id=pk)
    if request.user !=post.user:
        return HttpResponse("Not allowed!!")
    if request.method=='POST':
        post.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':post})

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    posts=user.post_set.all()
    comments= user.message_set.all()
    titles=Title.objects.all()
    context = {'user': user, 'posts': posts, 'comments': comments, 'titles': titles}
    return render(request, 'base/profile.html', context)

@login_required (login_url='login')
def editUser(request):
    return render(request,'base/editUser.html')