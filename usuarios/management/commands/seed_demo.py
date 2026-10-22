from getpass import getpass
import secrets
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from usuarios.models import (
    Capacitacion,
    Compania,
    Emergencia,
    Inventario,
    Proyecto,
    Rol,
    Usuario,
    Vehiculo,
)


class Command(BaseCommand):
    help = 'Crea datos completamente ficticios para la instancia de demostración.'

    def handle(self, *args, **options):
        email = input('Correo del administrador de demo: ').strip().lower()
        if not email:
            raise CommandError('El correo del administrador es obligatorio.')

        password = getpass('Contraseña nueva para el administrador de demo: ')
        confirmation = getpass('Repite la contraseña: ')
        if len(password) < 12 or password != confirmation:
            raise CommandError('Las contraseñas deben coincidir y tener al menos 12 caracteres.')

        role, _ = Rol.objects.get_or_create(
            nombre='Administrador Demo',
            defaults={'descripcion': 'Permisos de demostración para la instancia aislada.'},
        )
        for field in role._meta.fields:
            if field.name.startswith(('ver_', 'editar_')) and field.get_internal_type() == 'BooleanField':
                setattr(role, field.name, True)
        role.save()

        central, _ = Compania.objects.get_or_create(
            nombre='Compañía Demo Centro',
            defaults={'ubicacion': 'Sector Central (ficticio)'},
        )
        norte, _ = Compania.objects.get_or_create(
            nombre='Compañía Demo Norte',
            defaults={'ubicacion': 'Sector Norte (ficticio)'},
        )

        admin, _ = Usuario.objects.get_or_create(
            email=email,
            defaults={
                'nombre': 'Administración',
                'apellido': 'Demo',
                'rol': role,
                'compania': central,
                'is_active': True,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        admin.nombre = 'Administración'
        admin.apellido = 'Demo'
        admin.rol = role
        admin.compania = central
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password(password)
        admin.save()

        member, _ = Usuario.objects.get_or_create(
            email='brigadista.demo@example.invalid',
            defaults={
                'nombre': 'Valentina',
                'apellido': 'Ejemplo',
                'rol': role,
                'compania': central,
                'is_active': True,
            },
        )
        member.set_password(secrets.token_urlsafe(32))
        member.save()

        vehicle, _ = Vehiculo.objects.get_or_create(
            nombre='B-1 Demo',
            compania=central,
            defaults={
                'patente': 'DEMO-01',
                'descripcion': 'Unidad ficticia para mostrar la ficha del vehículo.',
                'marca': 'Marca Demo',
                'modelo': 'Modelo Demo',
                'anio_fabricacion': 2022,
                'estado': 'Disponible',
                'combustible': 'Diesel',
            },
        )

        today = timezone.localdate()
        alarm_time = timezone.now() - timedelta(hours=3)
        Emergencia.objects.get_or_create(
            tipo='10-0-1',
            direccion='Pasaje de Prueba 123, Sector Demo',
            defaults={
                'fecha_hora_alarma': alarm_time,
                'descripcion': 'Incidente ficticio utilizado exclusivamente para la demostración.',
                'unidades_despachadas': vehicle.nombre,
                'oficial_a_cargo': admin,
                'estado': 'Controlada',
                'creado_por': admin,
                'registro_completado': True,
            },
        )

        Capacitacion.objects.get_or_create(
            nombre='Taller de seguridad operacional (Demo)',
            defaults={
                'tipo_actividad': 'Taller',
                'malla': 'Nivel operativo',
                'descripcion': 'Actividad de capacitación ficticia para mostrar el módulo.',
                'fecha_inicio': timezone.now() + timedelta(days=7),
                'lugar': 'Centro de Entrenamiento Demo',
                'instructor': 'Instructor de Ejemplo',
                'cupos': 20,
                'creado_por': admin,
            },
        )

        Proyecto.objects.get_or_create(
            nombre='Mejora de equipamiento (Demo)',
            defaults={
                'descripcion': 'Proyecto ficticio para ilustrar seguimiento y responsables.',
                'fecha_inicio': today,
                'presupuesto': '2500000.00',
                'responsable': admin,
                'tipo': 'Equipamiento',
                'prioridad': 70,
                'creado_por': admin,
            },
        )

        Inventario.objects.get_or_create(
            nombre='Casco de bombero',
            compania=central,
            ubicacion='Bodega Demo',
            defaults={'estado': 'Bueno', 'agregado_por': admin, 'valor': 180000},
        )
        Inventario.objects.get_or_create(
            nombre='Equipo de respiración autónoma (ERA)',
            compania=norte,
            ubicacion='Unidad B-1 Demo',
            defaults={
                'estado': 'Bueno',
                'asignado_a_vehiculo': vehicle,
                'agregado_por': admin,
                'valor': 1200000,
            },
        )

        self.stdout.write(self.style.SUCCESS('Datos ficticios cargados.'))
        self.stdout.write(f'Administrador de demo: {email}')
