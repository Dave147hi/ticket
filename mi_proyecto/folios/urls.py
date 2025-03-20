from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear/', views.crear_folio, name='crear_folio'),
    path('<int:folio_id>/editar/', views.editar_folio, name='editar_folio'),
    path('<int:folio_id>/', views.ver_folio, name='ver_folio'),

    # NUEVAS RUTAS PARA CONTROL DE ENCUESTAS
    path('encuestas/', views.control_encuestas, name='control_encuestas'),
    path('encuestas/folio/<int:folio_id>/', views.ver_folio_encuesta, name='ver_folio_encuesta'),
    path('encuestas/folio/<int:folio_id>/primer_contacto/', views.primer_contacto, name='primer_contacto'),
    path('encuestas/folio/<int:folio_id>/envio_encuesta/', views.envio_encuesta, name='envio_encuesta'),
]
