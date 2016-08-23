from django.contrib.auth import authenticate
from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status
from user.user_views import render_with_user_info
from django.http import HttpResponse
import json


def homepage(request):
    return render_with_user_info(request, 'html/homepage.html')


def sign_in(request):
    return render_with_user_info(request, 'html/sign_in.html')


def personal(request):
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/personal.html')
    else:
        return render_with_user_info(request, 'html/sign_in.html')


def persontopassword(request):
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/password.html')
    else:
        return render_with_user_info(request,'html/sign_in.html')

def table_example(request):
    return render_with_user_info(request, 'html/table_example.html')

def ajax_password(request):
    if  request.is_ajax():
        data = json.dumps(request.POST)  #
        datas = json.loads(data);
        username=datas['username']
        oldpwd=datas['oldpassword']
        newpwd=datas['newpassword']
        user = authenticate(username=username, password=oldpwd)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                request.user.set_password(newpwd)
                request.user.save()
                return HttpResponse('true')
            else:
                return HttpResponse('false')
        else:
            return HttpResponse('false')

def ajax_user(request):
        if request.is_ajax():
            data = json.dumps(request.POST) #
            datas=json.loads(data);
            firstname= datas['firstname'];
            lastname = datas['lastname'];
            email = datas['email'];
            users = request.user
            users.first_name=firstname
            users.last_name=lastname
            users.email=email
            users.save()
            return HttpResponse('true')

def tablerender(request):
        return  render(request,"html/table_example.html")
def problemManage(request):
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/problem.html')
    else:
        return render_with_user_info(request, 'html/sign_in.html')
def problemAdd(request):
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/problem-add.html')
    else:
        return render_with_user_info(request, 'html/sign_in.html')

def problemModify(request):
    meta_id=request.GET['id']
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/problem-modify.html' ,{'meta_id':meta_id})
    else:
        return render_with_user_info(request, 'html/sign_in.html')

def problemDetail(request):
    meta_id=request.GET['id']
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/problem-details.html' ,{'meta_id':meta_id})
    else:
        return render_with_user_info(request, 'html/sign_in.html')

def problemsManage(request):
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/problems.html')
    else:
        return render_with_user_info(request, 'html/sign_in.html')
def problemsAdd(request):
    meta_id=request.GET['id']
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/problems-add.html',{'meta_id':meta_id})
    else:
        return render_with_user_info(request, 'html/sign_in.html')
def problemsDetail(request):
    problem_id = request.GET['id']
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/problems-details.html', {'id': problem_id})
    else:
        return render_with_user_info(request, 'html/sign_in.html')
def problemsModify(request):
    problem_id = request.GET['problem_id']
    meta_id=request.GET['meta_id']
    if request.user.is_authenticated():
        return render_with_user_info(request, 'html/problems-modify.html', {'id': problem_id ,'meta_id':meta_id})
    else:
        return render_with_user_info(request, 'html/sign_in.html')