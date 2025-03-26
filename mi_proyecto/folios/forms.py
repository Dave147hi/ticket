from django import forms
from .models import Folio, Comentario
from django.contrib.auth.models import User

class FolioForm(forms.ModelForm):
    """
    Formulario para la creación de un nuevo folio.
    Incluye todos los campos necesarios.
    """
    class Meta:
        model = Folio
        fields = [
            'llamada', 'motivo', 'medio_recepcion', 'medio_contacto', 'caso', 'area',
            'responsable_area', 'responsable_solucion', 'localidad', 'industria_sector',
            'estado', 'contacto', 'empresa', 'municipio', 'cp', 'telefono_local',
            'celular', 'email', 'direccion', 'comentarios'
        ]


class FolioEditForm(forms.ModelForm):
    """
    Formulario para editar un folio existente.
    Se excluyen campos de solo lectura (folio, asesor, fecha_apertura y hora_apertura).
    """
    class Meta:
        model = Folio
        fields = [
            'motivo', 'medio_recepcion', 'medio_contacto', 'caso', 'area',
            'responsable_area', 'responsable_solucion', 'localidad', 'estatus',
            'contacto', 'empresa', 'industria_sector', 'direccion', 'estado',
            'municipio', 'cp', 'telefono_local', 'celular', 'email'
        ]


class ComentarioForm(forms.ModelForm):
    """
    Formulario para agregar comentarios.
    """
    class Meta:
        model = Comentario
        fields = ['texto']


# ================================
# FORMULARIOS PARA ENCUESTAS
# ================================

class PrimerContactoForm(forms.ModelForm):
    """
    Formulario para actualizar el estado del primer contacto de una encuesta,
    permitiendo asignar un asesor para el primer contacto.
    """
    class Meta:
        model = Folio
        fields = ['status_primer_contacto', 'estado_primer_contacto', 'fecha_primer_contacto']

    def __init__(self, *args, **kwargs):
        super(PrimerContactoForm, self).__init__(*args, **kwargs)
        self.fields['status_primer_contacto'].queryset = User.objects.filter(is_active=True, is_staff=False)
        self.fields['status_primer_contacto'].required = False


class EnvioEncuestaForm(forms.ModelForm):
    """
    Formulario para actualizar el estado de envío de una encuesta,
    permitiendo asignar un asesor para el envío.
    """
    class Meta:
        model = Folio
        fields = ['status_envio', 'estado_envio', 'fecha_envio']

    def __init__(self, *args, **kwargs):
        super(EnvioEncuestaForm, self).__init__(*args, **kwargs)
        self.fields['status_envio'].queryset = User.objects.filter(is_active=True, is_staff=False)
        self.fields['status_envio'].required = False
