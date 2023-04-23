from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from inventory.views import UserProfileView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/profile/', UserProfileView.as_view(), name='user_profile'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('inventory.urls')),
]
