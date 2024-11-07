
from django.urls import path
from . import views

urlpatterns = [
    # Beispiel einer API-URL
    path('login/', views.login, name='login'),
    path('get_user_by_id/<int:id>/', views.UserDetailView.as_view(), name='get_user_by_id'),
]