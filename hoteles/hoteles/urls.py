"""hoteles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^login', 'gestion.views.login_view'),
    url(r'^logout', 'gestion.views.logout_view'),
    url(r'^about', 'gestion.views.about'),
    url(r'^refresh', 'gestion.views.refresh'),
    url(r'^admin/', admin.site.urls),
    url(r'^alojamientos/(.+)$', 'gestion.views.alojamientos_id'),
    url(r'^alojamientos', 'gestion.views.alojamientos'),     
    url(r'^templates/(.+)$', 'django.views.static.serve', 
        {'document_root': 'templates/'}),    
    url(r'^(favicon.ico)', 'django.views.static.serve', 
        {'document_root': 'images/'}),
    url(r'^images/(.*\.jpg)', 'django.views.static.serve', 
        {'document_root': 'images/'}),
    url(r'^images/(.*\.png)', 'django.views.static.serve', 
        {'document_root': 'images/'}), 
    url(r'^$', 'gestion.views.inicio'),
    url(r'^(.+)', 'gestion.views.usuario'),
]
