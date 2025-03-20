from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max


class Folio(models.Model):
    # Campos generados automáticamente
    folio = models.CharField(max_length=50, unique=True, verbose_name="Folio", editable=False)
    asesor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Asesor", editable=False)
    fecha_apertura = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Apertura", editable=False)
    hora_apertura = models.TimeField(auto_now_add=True, verbose_name="Hora de Apertura", editable=False)
    estatus = models.CharField(
        max_length=20,
        choices=[
            ('Abierta', 'Abierta'),
            ('Pendiente', 'Pendiente'),
            ('Cerrada', 'Cerrada')
        ],
        default='Abierta',
        verbose_name="Estatus"
    )
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Cierre", editable=False)
    hora_cierre = models.TimeField(null=True, blank=True, verbose_name="Hora de Cierre", editable=False)

    # Campos de selección
    llamada = models.CharField(
        max_length=20,
        choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')],
        verbose_name="Llamada"
    )
    motivo = models.CharField(
        max_length=50,
        choices=[('Solicitud', 'Solicitud'), ('Queja', 'Queja'), ('Correctivo', 'Correctivo')],
        verbose_name="Motivo"
    )
    medio_recepcion = models.CharField(
        max_length=50,
        choices=[('Llamada', 'Llamada'), ('Correo', 'Correo'), ('Chat', 'Chat')],
        verbose_name="Medio de Recepción"
    )
    medio_contacto = models.CharField(
        max_length=50,
        choices=[('Página web', 'Página web'), ('Atención.cliente', 'Atención.cliente'), ('Referido', 'Referido')],
        verbose_name="Medio de Contacto"
    )
    area = models.CharField(
        max_length=50,
        choices=[('Ventas PDE', 'Ventas PDE'), ('Ventas ACT', 'Ventas ACT'), ('Medical', 'Medical')],
        verbose_name="Área"
    )
    localidad = models.CharField(
        max_length=50,
        choices=[('Matriz', 'Matriz'), ('Servicio', 'Servicio')],
        verbose_name="Localidad"
    )
    industria_sector = models.CharField(
        max_length=50,
        choices=[
            ('Manufactura', 'Manufactura'),
            ('Servicios Profesionales', 'Servicios Profesionales'),
            ('Energía', 'Energía'),
            ('Gobierno', 'Gobierno')
        ],
        verbose_name="Industria/Sector"
    )
    estado = models.CharField(
        max_length=50,
        choices=[
            ('Aguascalientes', 'Aguascalientes'),
            ('Baja California', 'Baja California'),
            # Agregar todos los estados
        ],
        verbose_name="Estado"
    )

    # Campos de texto
    caso = models.TextField(verbose_name="Caso")
    responsable_area = models.CharField(max_length=100, verbose_name="Responsable de Área")
    responsable_solucion = models.CharField(max_length=100, verbose_name="Responsable de Solución")
    contacto = models.CharField(max_length=100, verbose_name="Contacto")
    empresa = models.CharField(max_length=100, verbose_name="Empresa")
    municipio = models.CharField(max_length=100, verbose_name="Municipio")
    cp = models.CharField(max_length=10, verbose_name="Código Postal")
    telefono_local = models.CharField(max_length=20, verbose_name="Teléfono Local")
    celular = models.CharField(max_length=20, verbose_name="Celular")
    email = models.EmailField(verbose_name="Email")
    direccion = models.TextField(verbose_name="Dirección")
    comentarios = models.TextField(blank=True, null=True, verbose_name="Comentarios")

    # 🚀 Campos para el control de encuestas
    status_primer_contacto = models.CharField(
        max_length=20,
        choices=[
            ("NO CONTESTAN", "No Contestan"),
            ("NO EXISTE", "No Existe"),
            ("NO SE ENCUENTRA", "No Se Encuentra"),
            ("NÚMERO EQUIVOCADO", "Número Equivocado"),
            ("REALIZADA", "Realizada"),
            ("NO REALIZADA", "No Realizada"),
        ],
        default="NO REALIZADA",
        verbose_name="Estado Primer Contacto"
    )
    fecha_primer_contacto = models.DateField(null=True, blank=True, verbose_name="Fecha de Primer Contacto")

    status_envio = models.CharField(
        max_length=20,
        choices=[
            ("NO CONTESTAN", "No Contestan"),
            ("NO EXISTE", "No Existe"),
            ("NO SE ENCUENTRA", "No Se Encuentra"),
            ("NÚMERO EQUIVOCADO", "Número Equivocado"),
            ("REALIZADA", "Realizada"),
            ("NO REALIZADA", "No Realizada"),
        ],
        default="NO REALIZADA",
        verbose_name="Estado Envío Cotización"
    )
    fecha_envio = models.DateField(null=True, blank=True, verbose_name="Fecha de Envío de Cotización")

    # Intentos de contacto con registro de fecha y hora
    intento_1 = models.DateTimeField(null=True, blank=True, verbose_name="Primer Intento")
    intento_2 = models.DateTimeField(null=True, blank=True, verbose_name="Segundo Intento")
    intento_3 = models.DateTimeField(null=True, blank=True, verbose_name="Tercer Intento")

    def save(self, *args, **kwargs):
        if not self.folio:
            ultimo_folio = Folio.objects.aggregate(Max('folio'))['folio__max']
            if ultimo_folio:
                try:
                    numero = int(ultimo_folio.split('-')[1]) + 1
                except (ValueError, IndexError):
                    numero = 1
            else:
                numero = 1
            self.folio = f"SAC-{numero:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.folio


class Comentario(models.Model):
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, related_name='comentarios_folio')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    texto = models.TextField(verbose_name="Comentario")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    hora = models.TimeField(auto_now_add=True, verbose_name="Hora")

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.fecha}"
