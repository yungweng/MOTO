
from django.urls import path
from . import views

urlpatterns = [
    # Beispiel einer API-URL
    path('login/', views.login, name='api_login'),
    path('get_user_by_id/<int:id>/', views.UserDetailView.as_view(), name='api_get_user_by_id'),
    path('rooms/', views.get_rooms_api, name='api_get_rooms'),
]