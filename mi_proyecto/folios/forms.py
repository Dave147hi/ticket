from django import forms
from .models import Folio, Comentario

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
# NUEVOS FORMULARIOS PARA ENCUESTAS
# ================================

class PrimerContactoForm(forms.ModelForm):
    """
    Formulario para actualizar el estado del primer contacto de una encuesta.
    """
    class Meta:
        model = Folio
        fields = ['status_primer_contacto']
        widgets = {
            'status_primer_contacto': forms.Select(choices=[
                ('NO CONTESTAN', 'No Contestan'),
                ('NO EXISTE', 'No Existe'),
                ('NO SE ENCUENTRA', 'No Se Encuentra'),
                ('NÚMERO EQUIVOCADO', 'Número Equivocado'),
                ('REALIZADA', 'Realizada'),
                ('NO REALIZADA', 'No Realizada'),
            ])
        }

class EnvioEncuestaForm(forms.ModelForm):
    """
    Formulario para actualizar el estado de envío de una encuesta.
    """
    class Meta:
        model = Folio
        fields = ['status_envio']
        widgets = {
            'status_envio': forms.Select(choices=[
                ('NO CONTESTAN', 'No Contestan'),
                ('NO EXISTE', 'No Existe'),
                ('NO SE ENCUENTRA', 'No Se Encuentra'),
                ('NÚMERO EQUIVOCADO', 'Número Equivocado'),
                ('REALIZADA', 'Realizada'),
                ('NO REALIZADA', 'No Realizada'),
            ])
        }
