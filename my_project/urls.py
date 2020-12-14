"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from items import views as items_views
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static
from items.views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    ItemAcceptView,
    ItemCancelView,
    ItemRecieveView

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ItemListView.as_view(), name='home'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/accept/', ItemAcceptView.as_view(), name='item-accept'),
    path('item/<int:pk>/cancel/', ItemCancelView.as_view(), name='item-cancel'),
    path('item/<int:pk>/recieve/', ItemRecieveView.as_view(), name='item-recieve'),
    path('users/register/', users_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', users_views.show_profile, name='profile'),
    path('profile/edit/', users_views.profile, name='profile-edit'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
