# Libraries :

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import Todo
from django.contrib.auth import authenticate, login, logout
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# Functions : 
#----------------------------------------------------------

def signup(request):
    if request.method =='POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pswrd = request.POST.get('pswrd')
        my_user = User.objects.create_user(fnm,email, pswrd)
        my_user.save()
        return redirect('/login')

    return render(request, "signup.html")
#--------------------------------------------------------------------

def loginn(request):
    if request.method =='POST':
        fnm = request.POST.get('fnm')
        pswrd = request.POST.get('pswrd')
        userr = authenticate(request, username=fnm, password = pswrd)
        if userr is not None:
            login(request,userr)
            return redirect('/todopage')
        else:
            return redirect('/login')
    
    return render(request, "login.html")
#------------------------------------------------------------------

def reset_srno(user):
    tasks = Todo.objects.filter(user=user).order_by('date')
    for idx, task in enumerate(tasks, start=1):
        task.srno = idx
        task.save()
#--------------------------------------------------------------------


def delete_task(request, id):
    task = Todo.objects.get(id=id, user=request.user)
    task.delete()
    reset_srno(request.user)
    return redirect('/todopage')


#-------------------------------------------------------------------


def edit_task(request, id):
    task = Todo.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        new_title = request.POST.get('title')
        task.title = new_title
        task.save()
        return redirect('/todopage')

    return render(request, 'edit.html', {'task': task})


#-------------------------------------------------------------


def logout_view(request):
    logout(request)  # This clears the session
    return redirect('login')  # Redirects to login page


#-------------------------------------------------------------

@login_required(login_url='login')
@never_cache
def ToDoo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Todo.objects.create(title=title, user=request.user, srno=0)  # Temporary srno
        reset_srno(request.user)
        return redirect('/todopage')

    res = Todo.objects.filter(user=request.user).order_by('srno')
    return render(request, "todo.html", {'res': res})
