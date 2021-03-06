import json
from django.http import JsonResponse
from fireMap.models import Cuartel
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from fireMap.models import Incendio
from users.models import UserProfile
from django.contrib.gis.geos import Point
from django.utils import timezone


@require_POST
@csrf_exempt
def status_cuartel(request):
    """
    Funcion para determinar el background de la app mobile en funcion del nivel
    de alarma de un cuartel.
    Hay 3 posibles niveles de alarma:
        - Bajo: No hay ningun incendio activo en la jurisdiccion, ni en
                jurisdicciones vecinas. Se representa con el color verde.
        - Medio: No hay incendios activos en la jurisdiccion, pero si en alguno
                de los cuarteles limitrofes. Se representa con el color amarillo.
        - Alto: Hay un incendio activo en la jurisdiccion que afecta al cuartel.
                Se representa con el color rojo.
    Toma un token y devuelve un color.
    """
    received_json = json.loads(request.body)
    token = received_json.get('token')
    user = get_object_or_404(Token, key=token).user
    user = UserProfile.objects.get(user=user)
    cuartel = user.cuartel
    if (
        cuartel.fuego_activo is True
    ) and (
        Incendio.objects.filter(cuarteles_afectados=cuartel).exists()
    ):
        color = '#fc3b2d'
    else:
        if Cuartel.objects.filter(
            fuego_activo=True,
            cuarteles_limitrofes=cuartel,
        ):
            color = '#f0a418'
        else:
            color = '#8fd9a8'
    return JsonResponse({'color': color})


@require_POST
@csrf_exempt
def confirmar_incendio(request):
    """
    Esta vista crea en la base de datos una instancia 'Incendio' con la
    informacion proveniente de la app mobile.
    Toma: token, coordenadas, falso_positivo, radio, riesgo_interfase, activo.
    Devuelve: JsonResponse
    """
    received_json = json.loads(request.body)
    token = received_json.get('token')
    user = get_object_or_404(Token, key=token).user
    user = UserProfile.objects.get(user=user)
    coord = Point(
        received_json.get('coordenadas')['longitude'],
        received_json.get('coordenadas')['latitude']
    )
    # cuartel = user.cuartel
    cuartel = Cuartel.objects.get(jurisdiccion__contains=coord)
    if received_json.get('falso_positivo') is True:
        return JsonResponse(
            {
                'Response':
                'El incendio denunciado es un falso_positivo'
            }
        )
    else:
        params = {
            'coordenadas': Point(
                received_json.get('coordenadas')['longitude'],
                received_json.get('coordenadas')['latitude']
            ),
            'radio': received_json.get('radio'),
            'riesgo_interfase': received_json.get('riesgo_interfase'),
            'activo': True
        }
    incendio = Incendio(**params)
    incendio.save()
    incendio.cuarteles_afectados.set([cuartel])

    cuartel.fuego_activo = True
    cuartel.save()

    return JsonResponse(
        {
            'Response':
            'El incendio ha sido confirmado y agregado a la base de datos'
        }
    )


@require_POST
@csrf_exempt
def informar_incendio(request):
    """
    Esta vista crea en la base de datos una instancia 'Incendio' con la
    informacion proveniente de la app mobile.
    Recibe: token, coordenadas, falso_positivo, radio, riesgo_interfase, activo,
    caracteristica, bomberos_afectados, unid?unid_pesadas_afectadas,
    unid_livianas_afectadas
    Devuelve: JsonResponse
    """
    received_json = json.loads(request.body)
    token = received_json.get('token')
    user = get_object_or_404(Token, key=token).user
    user = UserProfile.objects.get(user=user)
    # cuartel = user.cuartel ----> En esta opcion el cuartel se determina por el usuario que carga desde el celular.
    coord = Point(
        received_json.get('coordenadas')['longitude'],
        received_json.get('coordenadas')['latitude']
    )
    cuartel = Cuartel.objects.get(jurisdiccion__contains=coord)
    params = {
        'coordenadas': coord,
        'radio': received_json.get('radio'),
        'fecha_hora_inicio': timezone.now(),
        'riesgo_interfase': received_json.get('riesgo_interfase'),
        'estado': received_json.get('estado'),
        'caracteristica': received_json.get('caracteristica'),
        'bomberos_afectados': received_json.get('bomberos_afectados'),
        'unid_pesadas_afectadas': received_json.get('unid_pesadas_afectadas'),
        'unid_livianas_afectadas': received_json.get(
            'unid_livianas_afectadas'
        ),
        'activo': True
    }
    incendio = Incendio(**params)
    incendio.save()
    incendio.cuarteles_afectados.set([cuartel])

    cuartel.fuego_activo = True
    cuartel.save()

    return JsonResponse(
        {
            'Response':
            'El incendio ha sido confirmado y agregado a la base de datos'
        }
    )
