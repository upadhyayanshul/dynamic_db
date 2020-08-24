# ## DEFINE THE SITE APP URL PATTERN ## #
from django.conf.urls import url
from . import views
from django.contrib.auth import logout

# App NAME REFERENCED TO TEMPLATE
app_name = 'polls'

# REGEX URL PATTERN DEFINEED BELOW 
urlpatterns = [
    url(r'^$', views.home_view, name='home'),
    url(r'^home/?$', views.home_view, name='home'),
    url(r'^signup/?$', views.signup_view, name="signup"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$', views.activate,name='activate'),
    url(r'^login/?$', views.login_view, name='login'),
    url(r'^logout/?$', views.logout_user, name='logout_user'),
    url(r'^forget_password/?$', views.forget_password_view, name='forget_pass'),
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$', views.reset_password_view, name='reset_password'),
    url(r'^reset_password_confirm/?$', views.reset_password_confirm, name='reset_password_confirm'),
    url(r'^dashboard/?$', views.dashboard_view, name='dashboard'),
    url(r'^show_db/(?P<db_name>\w+)$', views.show_db_view, name='show_db'),
    url(r'^show_table/(?P<db_name>\w+)/(?P<db_table>\w+)/?$', views.show_db_view, name='show_table'),
    url(r'^permission_table/?$', views.permission_view, name="permission_table"),
    url(r'^product/(?P<db_name>\w+)/?$', views.product_view, name='product'),
    url(r'^product/?$', views.product_view,name="product"),
    url(r'^edit_permission/(?P<profile_id>[0-9]+)/?$', views.edit_permission, name='edit_permission'),
]

