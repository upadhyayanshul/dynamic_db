# ## DEFINE THE MAIN APP URL PATTERN ## #
from django.conf.urls import url,include
from django.contrib import admin

# REGEX URL PATTERN DEFINEED BELOW 
urlpatterns = [
    # Handle App Routes
    url(r'^polls/', include('polls.urls')),
    
    # Handle Other Routes
    # url(r'^.*', include('polls.urls')),

    # Handle Admin Routes
    url(r'^admin/', admin.site.urls),
]
