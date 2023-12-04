from django.urls import path, include
from . import views
urlpatterns = [
    path('account/', include('account.urls')),
    path('home/', include('home.urls')),
]
