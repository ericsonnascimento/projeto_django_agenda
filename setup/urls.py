from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from agenda import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agenda/', views.lista_eventos, name='lista_eventos'),
    path('agenda/lista/', views.json_lista_evento),
    path('agenda/lista/<int:id_usuario>/', views.json_lista_evento_api),
    path('agenda/evento/', views.evento, name='evento'),
    path('agenda/evento/submit', views.submit_evento),
    path('agenda/evento/delete/<int:id_evento>/', views.delete_evento, name='delete_evento'),
    path('', RedirectView.as_view(url='/agenda/')),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) # Adicionar Isto
