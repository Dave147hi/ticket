import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from .models import Folio, Comentario, ComentarioEncuesta
from .forms import FolioForm, FolioEditForm, PrimerContactoForm, EnvioEncuestaForm

# ================================
# DASHBOARD Y GESTIÓN DE FOLIOS
# ================================

@login_required
def dashboard(request):
    area = request.GET.get('area')
    fecha = request.GET.get('fecha')
    folio_numero = request.GET.get('folio_numero')

    folios = Folio.objects.all()
    if area:
        folios = folios.filter(area=area)
    if fecha:
        folios = folios.filter(fecha_apertura__date=fecha)
    if folio_numero:
        folios = folios.filter(id=folio_numero)

    folios_by_area = list(Folio.objects.values('area').annotate(count=Count('id')))
    folios_by_status = list(Folio.objects.values('estatus').annotate(count=Count('id')))
    unique_areas = Folio.objects.values_list('area', flat=True).distinct()

    context = {
        'folios': folios,
        'folios_by_area_json': json.dumps(folios_by_area),
        'folios_by_status_json': json.dumps(folios_by_status),
        'unique_areas': unique_areas,
    }
    return render(request, 'folios/dashboard.html', context)

@login_required
def crear_folio(request):
    if request.method == 'POST':
        form = FolioForm(request.POST)
        if form.is_valid():
            folio_obj = form.save(commit=False)
            folio_obj.asesor = request.user
            folio_obj.save()
            return redirect('dashboard')
    else:
        form = FolioForm()
    return render(request, 'folios/crear_folio.html', {'form': form})

@login_required
def editar_folio(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id)
    if request.method == 'POST':
        folio_form = FolioEditForm(request.POST, instance=folio)
        nuevo_comentario = request.POST.get("nuevo_comentario", "").strip()
        if folio_form.is_valid():
            folio = folio_form.save(commit=False)
            if folio.estatus == 'Cerrada' and not folio.fecha_cierre:
                folio.fecha_cierre = timezone.now()
                folio.hora_cierre = timezone.now().time()
            folio.save()
            if nuevo_comentario:
                Comentario.objects.create(folio=folio, usuario=request.user, texto=nuevo_comentario)
            return redirect('editar_folio', folio_id=folio.id)
    else:
        folio_form = FolioEditForm(instance=folio)

    comentarios = folio.comentarios_folio.all().order_by('-fecha', '-hora')
    return render(request, 'folios/editar_folio.html', {
        'folio': folio,
        'folio_form': folio_form,
        'comentarios': comentarios
    })

@login_required
def ver_folio(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id)
    comentarios = folio.comentarios_folio.all().order_by('-fecha', '-hora')
    return render(request, 'folios/ver_folio.html', {
        'folio': folio,
        'comentarios': comentarios
    })

# ================================
# CONTROL DE ENCUESTAS
# ================================

@login_required
def control_encuestas(request):
    folios = Folio.objects.all()
    unique_areas = Folio.objects.values_list('area', flat=True).distinct()
    return render(request, 'folios/control_encuestas.html', {
        'folios': folios,
        'unique_areas': unique_areas,
    })

@login_required
def encuesta_vista(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id)
    comentarios = ComentarioEncuesta.objects.filter(folio=folio).order_by('-fecha')

    if request.method == 'POST':
        texto = request.POST.get('nuevo_comentario', '').strip()
        if texto:
            ComentarioEncuesta.objects.create(folio=folio, usuario=request.user, texto=texto)

        intento = request.POST.get('intento')
        tipo = request.POST.get('tipo')
        now = timezone.now()

        if tipo == 'primer_contacto':
            if not folio.intento_pc_1:
                folio.intento_pc_1 = now
            elif not folio.intento_pc_2:
                folio.intento_pc_2 = now
            elif not folio.intento_pc_3:
                folio.intento_pc_3 = now
        elif tipo == 'envio':
            if not folio.intento_envio_1:
                folio.intento_envio_1 = now
            elif not folio.intento_envio_2:
                folio.intento_envio_2 = now
            elif not folio.intento_envio_3:
                folio.intento_envio_3 = now

        estado_primer = request.POST.get('estado_primer_contacto')
        estado_envio = request.POST.get('estado_envio')
        if estado_primer:
            folio.estado_primer_contacto = estado_primer
        if estado_envio:
            folio.estado_envio = estado_envio

        folio.save()
        return redirect('encuesta_vista', folio_id=folio.id)

    # Para los selects
    estado_opciones = Folio._meta.get_field('estado_primer_contacto').choices

    return render(request, 'folios/encuesta_vista.html', {
        'folio': folio,
        'comentarios': comentarios,
        'estado_opciones': estado_opciones,
    })

@login_required
def ver_folio_encuesta(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id)
    comentarios = folio.comentarios_folio.all().order_by('-fecha', '-hora')
    return render(request, 'folios/ver_folio_encuesta.html', {
        'folio': folio,
        'comentarios': comentarios
    })

@login_required
def primer_contacto(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id)
    if request.method == 'POST':
        form = PrimerContactoForm(request.POST, instance=folio)
        if form.is_valid():
            folio = form.save(commit=False)
            if not folio.asesor:
                folio.asesor = request.user
            folio.fecha_primer_contacto = timezone.now()

            now = timezone.now()
            if not folio.intento_pc_1:
                folio.intento_pc_1 = now
            elif not folio.intento_pc_2:
                folio.intento_pc_2 = now
            elif not folio.intento_pc_3:
                folio.intento_pc_3 = now

            folio.save()
            return redirect('ver_folio_encuesta', folio_id=folio.id)
    else:
        form = PrimerContactoForm(instance=folio)

    return render(request, 'folios/primer_contacto.html', {'folio': folio, 'form': form})

@login_required
def envio_encuesta(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id)
    if request.method == 'POST':
        form = EnvioEncuestaForm(request.POST, instance=folio)
        if form.is_valid():
            folio = form.save(commit=False)
            folio.fecha_envio = timezone.now()

            now = timezone.now()
            if not folio.intento_envio_1:
                folio.intento_envio_1 = now
            elif not folio.intento_envio_2:
                folio.intento_envio_2 = now
            elif not folio.intento_envio_3:
                folio.intento_envio_3 = now

            folio.save()
            return redirect('ver_folio_encuesta', folio_id=folio.id)
    else:
        form = EnvioEncuestaForm(instance=folio)

    return render(request, 'folios/envio_encuesta.html', {'folio': folio, 'form': form})
