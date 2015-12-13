from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import uuid
from django.core.mail import send_mail
from accounts.models import Account

def rendering(request, tpl, ctx):
    return render_to_response(tpl, ctx, context_instance=RequestContext(request))

"""
def handle_request(request, tpl):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    ctx = {}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return do_get()
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(reverse('me_endpoint'))
        else:
            ctx["error"] = "Incorrect username or password!"
            return rendering(request, tpl, ctx)
    else:
        raise Http404
"""

def login_endpoint(request):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    tpl = "accounts/login.html"
    ctx = {}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return rendering(request, tpl, ctx)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(reverse('me_endpoint'))
        else:
            ctx["error"] = "Incorrect username or password!"
            return rendering(request, tpl, ctx)
    else:
        raise Http404
        
def signup_endpoint(request):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    tpl = "accounts/signup.html"
    ctx = {}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return rendering(request, tpl, ctx)
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
            return rendering(request, tpl, ctx)
    else:
        raise Http404

@login_required        
def me_endpoint(request):
    ctx = {}
    return render_to_response("accounts/me.html", ctx, context_instance=RequestContext(request))
    
def logout_endpoint(request):
    logout(request)
    return redirect(reverse("login_endpoint"))
    
def recovery_endpoint(request):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    tpl = "accounts/recovery.html"
    ctx = {}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return render_to_response(tpl, ctx, context_instance=RequestContext(request))
    elif request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            
            code = str(uuid.uuid4())
            
            account = Account.get_account(user)
            account.password_recovery_code = code
            account.save()
            
            try:
                send_mail('Password recovery', 'Pin-code: {0}'.format(code), 'info@alexkorotkov.ru', [user.email], fail_silently=False)
            except:
                ctx["error"] = "Pin sending error!"
                return render_to_response("accounts/recovery.html", ctx, context_instance=RequestContext(request))
            return redirect(reverse("recovery_form_endpoint"))
        except User.DoesNotExist:
            ctx["error"] = "User with email {0} doesn't exist!".format(email)
            return render_to_response(tpl, ctx, context_instance=RequestContext(request))
    else:
        raise Http404
        
def recovery_form_endpoint(request):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    tpl = "accounts/recovery_form.html"
    ctx = {}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return rendering(request, tpl, ctx)
    elif request.method == 'POST':
        pin = request.POST['pin']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        try:
            assert password == confirm_password, "Password and confirmation are not equal."
            
            try:
                account = Account.objects.get(password_recovery_code=pin)
            except Account.DoesNotExist:
                raise Exception("Pin {0} not found.".format(pin))
                
            account.user.set_password(password)
            account.user.save()
            
            account.password_recovery_code = None
            account.save()
            
            return redirect(reverse('login_endpoint'))
        except Exception as e:
            ctx["error"] = str(e)
            return rendering(request, tpl, ctx)
    else:
        raise Http404
