import re
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import is_safe_url
from django.contrib import messages

import threading 
request_cfg = threading.local()

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

## LOGIN REQUIRED MIDDLEWARE ##
class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required Middleware"
        print(hasattr(request, 'user'), "The Login Required Middleware",request.user.is_authenticated())
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                redirect_to = settings.LOGIN_URL
                
                # 'next' variable to support redirection to attempted page after login
                if len(path) > 0 and is_safe_url(url=request.path_info, host=request.get_host()):
                    messages.info(request,'Login Required,Please login to access {}'.format(path))
                    redirect_to = settings.LOGIN_URL+"?next="+request.path_info
                return HttpResponseRedirect(redirect_to)

## ROUTER MIDDLEWARE TO HANDLE DATABASE SWITCHING
class RouterMiddleware(MiddlewareMixin):
    def process_request( self, request):
        db_path = request.path_info.lstrip('/')

        if hasattr(settings, 'DATABASE_SWITCHING'):
            DATABASE_SWITCH = [re.compile(url) for url in settings.DATABASE_SWITCHING]

            if any(m.match(db_path.encode("utf8")) for m in DATABASE_SWITCH):
                db_name = list(filter(None, db_path.encode("utf8").split("/")))[-1]
                request_cfg.cfg = db_name.encode("utf8")

    def process_response( self, request, response ):
        if hasattr( request_cfg, 'cfg' ):
            del request_cfg.cfg
        return response


## MANAGE RUN TIME DATABASE
class DatabaseRouter (object):
    def _default_db( self ):
        if hasattr( request_cfg, 'cfg' ):
            if request_cfg.cfg in settings.DATABASES:
                return request_cfg.cfg
            else:
                print("DATABASE INVALID SELECTION ")
        else:
            return 'default'

    def db_for_read( self, model, **hints ):
        return self._default_db()

    def db_for_write( self, model, **hints ):
        return self._default_db()

## CHECK THE ADMIN PERMISSION ##
class PermissionRequiredMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required Middleware"
        print(hasattr(request, 'user'), "The Login Required Middleware",request.user.is_authenticated())
        from django.core.urlresolvers import resolve
        current_url = resolve(request.path_info).url_name

        path = request.path_info.lstrip('/')

        if not request.user.is_superuser:
            if(current_url in settings.USER_REQUEST_PERMISSION):
                messages.info(request," Unauthorize don't have permission to {}".format(path))
                return HttpResponseRedirect('/polls/login/')
       
