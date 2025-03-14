"""
URL configuration for ssabu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'user_account.views.handler404'
handler500 = 'user_account.views.handler500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_account.urls')),
    path('pages/', include('blog.urls')),
    path('computer-based-test/', include('cbt.urls')),
    path('api/rest/', include('api.urls')),
    path('resource/', include('material.urls')),
    path('service/', include('service.urls')),
    path('wallet/', include('wallet.urls')),
    path('reader/', include('reader.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('mail/', include('mail.urls')),
    path('', include('app.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)