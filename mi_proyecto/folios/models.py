from django.db import models
from django.contrib.auth.models import User
import re

class Folio(models.Model):
    folio = models.CharField(max_length=50, unique=True, verbose_name="Folio", editable=False)
    asesor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Asesor", editable=False)
    fecha_apertura = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Apertura", editable=False)
    hora_apertura = models.TimeField(auto_now_add=True, verbose_name="Hora de Apertura", editable=False)

    estatus = models.CharField(
        max_length=20,
        choices=[('Abierta', 'Abierta'), ('Pendiente', 'Pendiente'), ('Cerrada', 'Cerrada')],
        default='Abierta',
        verbose_name="Estatus"
    )
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Cierre", editable=False)
    hora_cierre = models.TimeField(null=True, blank=True, verbose_name="Hora de Cierre", editable=False)

    llamada = models.CharField(max_length=20, choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')])
    motivo = models.CharField(max_length=50, choices=[('Solicitud', 'Solicitud'), ('Queja', 'Queja'), ('Correctivo', 'Correctivo')])
    medio_recepcion = models.CharField(max_length=50, choices=[('Llamada', 'Llamada'), ('Correo', 'Correo'), ('Chat', 'Chat')])
    medio_contacto = models.CharField(max_length=50, choices=[('Página web', 'Página web'), ('Atención.cliente', 'Atención.cliente'), ('Referido', 'Referido')])
    area = models.CharField(max_length=50, choices=[('Ventas PDE', 'Ventas PDE'), ('Ventas ACT', 'Ventas ACT'), ('Medical', 'Medical')])
    localidad = models.CharField(max_length=50, choices=[('Matriz', 'Matriz'), ('Servicio', 'Servicio')])
    industria_sector = models.CharField(max_length=50, choices=[('Manufactura', 'Manufactura'), ('Servicios Profesionales', 'Servicios Profesionales'), ('Energía', 'Energía'), ('Gobierno', 'Gobierno')])
    estado = models.CharField(max_length=50, choices=[('Aguascalientes', 'Aguascalientes'), ('Baja California', 'Baja California'), ('CDMX', 'CDMX')])

    caso = models.TextField()
    responsable_area = models.CharField(max_length=100)
    responsable_solucion = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    cp = models.CharField(max_length=10)
    telefono_local = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()
    comentarios = models.TextField(blank=True, null=True)

    # Encuesta - Primer contacto
    status_primer_contacto = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='primer_contacto_folios')
    estado_primer_contacto = models.CharField(
        max_length=20,
        choices=[
            ("NO CONTESTAN", "No Contestan"),
            ("NO EXISTE", "No Existe"),
            ("NO SE ENCUENTRA", "No Se Encuentra"),
            ("NÚMERO EQUIVOCADO", "Número Equivocado"),
            ("REALIZADA", "Realizada"),
            ("NO REALIZADA", "No Realizada"),
        ],
        default="NO REALIZADA"
    )
    fecha_primer_contacto = models.DateField(null=True, blank=True)

    # Encuesta - Envío
    status_envio = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='envio_folios')
    estado_envio = models.CharField(
        max_length=20,
        choices=[
            ("NO CONTESTAN", "No Contestan"),
            ("NO EXISTE", "No Existe"),
            ("NO SE ENCUENTRA", "No Se Encuentra"),
            ("NÚMERO EQUIVOCADO", "Número Equivocado"),
            ("REALIZADA", "Realizada"),
            ("NO REALIZADA", "No Realizada"),
        ],
        default="NO REALIZADA"
    )
    fecha_envio = models.DateField(null=True, blank=True)

    # Intentos separados
    intento_pc_1 = models.DateTimeField(null=True, blank=True)
    intento_pc_2 = models.DateTimeField(null=True, blank=True)
    intento_pc_3 = models.DateTimeField(null=True, blank=True)

    intento_envio_1 = models.DateTimeField(null=True, blank=True)
    intento_envio_2 = models.DateTimeField(null=True, blank=True)
    intento_envio_3 = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.folio:
            base = "SAC-"
            ultimo = Folio.objects.filter(folio__startswith=base).order_by('-id').first()
            if ultimo:
                match = re.search(r'(\d+)$', ultimo.folio)
                numero = int(match.group(0)) + 1 if match else 1
            else:
                numero = 1

            while True:
                nuevo_folio = f"{base}{numero:04d}"
                if not Folio.objects.filter(folio=nuevo_folio).exists():
                    self.folio = nuevo_folio
                    break
                numero += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.folio


class Comentario(models.Model):
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, related_name='comentarios_folio')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.fecha}"


class ComentarioEncuesta(models.Model):
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, related_name='comentarios_encuesta')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Encuesta] {self.usuario.username} - {self.fecha}"
