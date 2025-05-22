from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home_view, name='home'),
    path('produtos/', include('catalogo.urls')),
    path('carrinho/', include(('carrinho.urls', 'carrinho'), namespace='carrinho')),
    
    # Aqui o namespace usuarios e o app_name devem bater, como você já tem no usuarios/urls.py
    path('usuario/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')), 
    
    path('sobre/', views.sobre_view, name='sobre'),
    path('contato/', views.contato_view, name='contato'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
