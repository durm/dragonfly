from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

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
            ctx["error"] = "Incorrect login or password!"
            return render_to_response("accounts/login.html", ctx, context_instance=RequestContext(request))
    else:
        raise Http404

@login_required        
def me_endpoint(request):
    ctx = {}
    return render_to_response("accounts/me.html", ctx, context_instance=RequestContext(request))
    
def logout_endpoint(request):
    logout(request)
    return redirect(reverse("login_endpoint"))
