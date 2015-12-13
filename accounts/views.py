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


def handle_request(request, tpl, do_post):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    ctx = {}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return rendering(request, tpl, ctx)
    elif request.method == 'POST':
        try:
            return do_post(request, ctx)
        except:
            ctx["error"] = str(e)
            return rendering(request, tpl, ctx)
    else:
        raise Http404


def login_proc(request, ctx):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    assert user is not None and user.is_active, "Incorrect username or password!"
    login(request, user)
    return redirect(reverse('me_endpoint'))


def signup_proc(request, ctx):
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    email = request.POST['email']
    assert password == confirm_password, "Password and confirmation are not equal."
    user = User.objects.create_user(username, email, password)
    user.is_active = True
    user.save()
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect(reverse('me_endpoint'))


def recovery_proc(request, ctx):
    email = request.POST['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise Exception("User with email {0} doesn't exist!".format(email))
    code = str(uuid.uuid4())
        
    account = Account.get_account(user)
    account.password_recovery_code = code
    account.save()
        
    try:
        send_mail('Password recovery', 'Pin-code: {0}'.format(code), 'info@alexkorotkov.ru', [user.email], fail_silently=False)
    except:
        raise Exception("Pin sending error!")
        
    return redirect(reverse("recovery_form_endpoint"))


def recovery_form_proc(request, ctx):
    pin = request.POST['pin']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
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
    

def recovery_endpoint(request):
    return handle_request(request, "accounts/recovery.html", recovery_proc)


def login_endpoint(request):
    return handle_request(request, "accounts/login.html", login_proc)

    
def signup_endpoint(request):
    return handle_request(request, "accounts/signup.html", signup_proc)


@login_required        
def me_endpoint(request):
    ctx = {}
    return render_to_response("accounts/me.html", ctx, context_instance=RequestContext(request))

    
def logout_endpoint(request):
    logout(request)
    return redirect(reverse("login_endpoint"))


def recovery_form_endpoint(request):
    return handle_request(request, "accounts/recovery_form.html", recovery_form_proc)
