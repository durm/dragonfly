from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_endpoint(request):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    ctx = {}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return render_to_response("accounts/login.html", ctx, context_instance=RequestContext(request))
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(reverse('me_endpoint'))
        else:
            ctx["error"] = "Incorrect username or password!"
            return render_to_response("accounts/login.html", ctx, context_instance=RequestContext(request))
    else:
        raise Http404
        
def signup_endpoint(request):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    ctx = {}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return render_to_response("accounts/signup.html", ctx, context_instance=RequestContext(request))
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        
        try:
            assert password == confirm_password, "Password and confirmation are not equal."
            user = User.objects.create_user(username, email, password)
            user.is_active = True
            user.save()
            
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('me_endpoint'))
        except Exception as e:
            ctx["error"] = str(e)
            return render_to_response("accounts/signup.html", ctx, context_instance=RequestContext(request))
    else:
        raise Http404

@login_required        
def me_endpoint(request):
    ctx = {}
    return render_to_response("accounts/me.html", ctx, context_instance=RequestContext(request))
    
def logout_endpoint(request):
    logout(request)
    return redirect(reverse("login_endpoint"))
