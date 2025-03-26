from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('crear/', views.crear_folio, name='crear_folio'),
    path('editar/<int:folio_id>/', views.editar_folio, name='editar_folio'),
    path('ver/<int:folio_id>/', views.ver_folio, name='ver_folio'),
    
    # Control de encuestas
    path('encuestas/', views.control_encuestas, name='control_encuestas'),
    path('ver_folio_encuesta/<int:folio_id>/', views.ver_folio_encuesta, name='ver_folio_encuesta'),
    path('primer_contacto/<int:folio_id>/', views.primer_contacto, name='primer_contacto'),
    path('envio_encuesta/<int:folio_id>/', views.envio_encuesta, name='envio_encuesta'),

    # Nueva vista detallada de encuesta
    path('encuesta_vista/<int:folio_id>/', views.encuesta_vista, name='encuesta_vista'),
]

