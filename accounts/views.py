from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def login_endpoint(request):
    if request.user.is_authenticated():
        return redirect(reverse('me_endpoint'))
    if request.method == 'GET':
        ctx = {}
        ctx.update(csrf(request))
        return render_to_response("accounts/login.html", ctx, context_instance=RequestContext(request))
    elif request.method == 'POST':
        print (111)
    else:
        raise Http404

@login_required        
def me_endpoint(request):
    ctx = {}
    return render_to_response("accounts/me.html", ctx, context_instance=RequestContext(request))
