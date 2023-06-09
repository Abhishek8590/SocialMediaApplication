from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from myapp.forms import SignUpForm, LoginForm, ProfileEditForm, PostForm, CoverPicForm,PassResetForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from myapp.models import UserProfile, Posts, Comments
from django import forms
from django.db.models import Q
from django.utils.decorators import method_decorator

def signin_required(fn):

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, "you must login to perform this action !!!")
            return redirect("signin")
        else:
            return fn(request, *args, **kwargs)
    return wrapper


# Create your views here.
class SignupView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "reg.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request, "account has been created !!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "failed to create account")
        return super().form_invalid(form)


class SignInView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            usr = authenticate(request, username=uname, password=pwd)
            if usr:
                login(request, usr)
                return redirect("index")
            messages.error(request, "invalid credentials")
        return render(request, self.template_name, {"form": form})

@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView, ListView):
    template_name = "index.html"
    form_class = PostForm
    model = Posts
    context_object_name = "posts"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PassResetView(FormView):
    model=User
    template_name="pass-res.html"
    form_class=PassResetForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)

        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pwd1=form.cleaned_data.get("password1")
            pwd2=form.cleaned_data.get("password2")

            if pwd1==pwd2:
                try:
                    usr=User.objects.get(username=username,email=email)
                    usr.set_password(pwd1)
                    usr.save()
                    messages.success(request,"password changed")
                    return redirect("signin")

                except Exception as e:
                    messages.error("invalid credentials")
                    return render (request,self.template_name,{"form":form})
            else:
                messages.error("password mismatch")
                return render(request,self.template_name,{"form":form})
                    
                    
            

@method_decorator(signin_required,name="dispatch")
class ProfileEditView(UpdateView):
    model = UserProfile
    form_class = ProfileEditForm
    template_name = "profile-edit.html"
    success_url = reverse_lazy("index")




@signin_required
def add_like_view(request, *args, **kwargs):
    id = kwargs.get("pk")
    post_obj = Posts.objects.get(id=id)
    post_obj.liked_by.add(request.user)
    return redirect("index")

# localhost: 8000/ posts/{id}/comments/add

@signin_required
def add_comment_view(request, *args, **kwargs):
    id = kwargs.get("pk")
    post_obj = Posts.objects.get(id=id)
    comment = request.POST.get("comment")
    Comments.objects.create(
        user=request.user, comment_text=comment, post=post_obj)
    return redirect("index")

# localhost: 8000/comments/{id}/remove/

@signin_required
def delete_comment_view(request, *args, **kwargs):
    id = kwargs.get("pk")
    comment_obj = Comments.objects.get(id=id)
    if request.user == comment_obj.user:
        comment_obj.delete()
        return redirect("index")
    else:
        messages.error(request, "you can't delete someone else comment")
        return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = "profile.html"
    context_object_name = "profile"


# profile/{id}/coverpic/change

@signin_required
def change_cover_pic_view(request, *args, **kwargs):
    id = kwargs.get("pk")
    prof_obj = UserProfile.objects.get(id=id)
    form = CoverPicForm(instance=prof_obj,
                        data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("profile-detail", pk=id)
    return redirect("profile-detail", pk=id)

@method_decorator(signin_required,name="dispatch")
class ProfileListView(ListView):
    model = UserProfile
    template_name = "profile-list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return UserProfile.objects.exclude(user=self.request.user)

    def post(self, request, *args, **kwargs):
        pname = request.POST.get('username')
        qs = UserProfile.objects.filter(
            Q(user__username__icontains=pname) | 
            Q(user__first_name__icontains=pname) | 
            Q(user__last_name__icontains=pname)
        )
        return render(request,self.template_name,{"profiles":qs})



    # change queryset to avoid seeing user in profile list
    # def get(self,request,*args,**kwargs):
    #     qs=UserProfile.objects.exclude(user=request.user)
    #     return render(request,self.template_name,{"profiles:qs"})

# localhost:8000/profiles/{id}/follow/

def follow_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    profile_obj=UserProfile.objects.get(id=id)
    user_prof=request.user.profile
    user_prof.following.add(profile_obj)
    user_prof.save()
    return redirect("index")


def unfollow_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    profile_obj=UserProfile.objects.get(id=id)
    user_prof=request.user.profile
    user_prof.following.remove(profile_obj)
    user_prof.save()
    return redirect("index")

def sign_out_view(request,*args,**kargs):
    logout(request)
    return redirect("signin")