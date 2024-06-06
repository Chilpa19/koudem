from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render
from .form import UserForm
from django.contrib.auth import logout

def login(request):
    if request.method=='GET':
        form=UserForm()
        context={"form":form}
        return render(request,"./users/login.html",context)
    else:
        username=request.POST['username']
        context={"username":username}
        return render(request,'./test.html',context)
    

def exit(request):
    logout(request)
    return redirect('portal')




