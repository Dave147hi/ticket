import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from .models import Folio, Comentario, User
from .forms import FolioEditForm, FolioForm

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
            folio_obj.save()  # Se genera el folio automáticamente
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
                comentario = Comentario(texto=nuevo_comentario, folio=folio, usuario=request.user)
                comentario.save()

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
    # Filtrar folios que NO estén en estado "REALIZADA" por defecto
    folios = Folio.objects.exclude(status_primer_contacto="REALIZADA")
    unique_areas = Folio.objects.values_list('area', flat=True).distinct()
    asesores = User.objects.filter(is_active=True)  # Lista de asesores activos

    return render(request, 'folios/control_encuestas.html', {
        'folios': folios,
        'unique_areas': unique_areas,
        'asesores': asesores,
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
        status = request.POST.get('status_primer_contacto')
        folio.status_primer_contacto = status
        folio.fecha_primer_contacto = timezone.now()

        # REGISTRO DE INTENTOS DE CONTACTO
        now = timezone.now()
        if not folio.intento_1:
            folio.intento_1 = now
        elif not folio.intento_2:
            folio.intento_2 = now
        elif not folio.intento_3:
            folio.intento_3 = now

        folio.save()
        return redirect('ver_folio_encuesta', folio_id=folio.id)

    return render(request, 'folios/primer_contacto.html', {'folio': folio})

@login_required
def envio_encuesta(request, folio_id):
    folio = get_object_or_404(Folio, id=folio_id)

    if request.method == 'POST':
        folio.status_envio = request.POST.get('status_envio')
        folio.fecha_envio = timezone.now()
        folio.save()
        return redirect('ver_folio_encuesta', folio_id=folio.id)

    return render(request, 'folios/envio_encuesta.html', {'folio': folio})

# ================================
# ASIGNACIÓN DE ASESORES (AJAX)
# ================================

@login_required
def asignar_asesor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        folio_id = data.get('folio_id')
        tipo = data.get('tipo')  # 'primer_contacto' o 'envio'
        asesor_id = data.get('asesor_id')

        folio = get_object_or_404(Folio, id=folio_id)
        asesor = User.objects.get(id=asesor_id) if asesor_id else None

        if tipo == 'primer_contacto':
            folio.asesor_primer_contacto = asesor
        elif tipo == 'envio':
            folio.asesor_envio = asesor

        folio.save()

        return JsonResponse({'success': True, 'folio_id': folio.id, 'asesor': asesor.username if asesor else "Sin asignar"})

    return JsonResponse({'success': False}, status=400)
