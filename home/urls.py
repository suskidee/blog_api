from django.urls import path, include
from . import views
urlpatterns = [
    path('blog/', views.BlogView.as_view()),
    path('all/', views.PublicBlogView.as_view()),
]
