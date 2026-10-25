from getpass import getpass
import secrets
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from usuarios.models import (
    Capacitacion,
    CajaChica,
    Compania,
    Emergencia,
    Inventario,
    Mantenimiento,
    Proyecto,
    Rol,
    Usuario,
    Vehiculo,
)


class Command(BaseCommand):
    help = 'Crea datos completamente ficticios para la instancia de demostración.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad', type=int, default=20,
            help='Cantidad de registros variados a crear por cada módulo (1 a 500).',
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        if not 1 <= cantidad <= 500:
            raise CommandError('--cantidad debe estar entre 1 y 500.')

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
        member_role, _ = Rol.objects.get_or_create(
            nombre='Brigadista Demo',
            defaults={'descripcion': 'Rol básico para cuentas ficticias de brigadistas.'},
        )

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
                'rol': member_role,
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

        # Lote adicional, determinista e idempotente para poblar los módulos de demo.
        nombres = ['Camila', 'Matías', 'Antonia', 'Benjamín', 'Florencia', 'Tomás', 'Isidora', 'Vicente']
        apellidos = ['Rojas', 'Muñoz', 'Soto', 'Díaz', 'Pérez', 'González', 'Silva', 'Torres']
        companias = [central, norte]
        estados_vehiculo = ['Disponible', 'En Servicio', 'En Taller', 'Fuera de Servicio']
        tipos_emergencia = [value for value, _ in Emergencia.TIPO_EMERGENCIA_CHOICES]
        nombres_inventario = [value for value, _ in Inventario.ITEM_CHOICES]
        for i in range(1, cantidad + 1):
            compania = companias[i % len(companias)]
            brigadista, _ = Usuario.objects.get_or_create(
                email=f'brigadista{i:03d}.demo@example.invalid',
                defaults={
                    'nombre': nombres[(i - 1) % len(nombres)],
                    'apellido': apellidos[(i * 3) % len(apellidos)],
                    'rol': member_role,
                    'compania': compania,
                    'is_active': True,
                },
            )
            if brigadista.has_usable_password() is False:
                brigadista.set_password(secrets.token_urlsafe(32))
                brigadista.save(update_fields=['password'])

            vehiculo, _ = Vehiculo.objects.get_or_create(
                nombre=f'Demo {i:03d}', compania=compania,
                defaults={
                    'patente': f'DM-{i:05d}',
                    'descripcion': f'Unidad ficticia de demostración {i}.',
                    'marca': ['Volvo', 'Mercedes-Benz', 'MAN', 'Iveco'][i % 4],
                    'modelo': ['Rescate', 'Bomba', 'Aljibe', 'Forestales'][i % 4],
                    'anio_fabricacion': 2018 + i % 8,
                    'estado': estados_vehiculo[i % len(estados_vehiculo)],
                    'combustible': ['Diesel', 'Gasolina', 'Otro'][i % 3],
                },
            )
            Emergencia.objects.get_or_create(
                direccion=f'Dirección ficticia Demo {i:03d}',
                defaults={
                    'tipo': tipos_emergencia[i % len(tipos_emergencia)],
                    'fecha_hora_alarma': timezone.now() - timedelta(days=i, hours=i % 24),
                    'descripcion': f'Evento de prueba ficticio número {i}; sin relación con una emergencia real.',
                    'unidades_despachadas': vehiculo.nombre,
                    'oficial_a_cargo': brigadista,
                    'estado': ['Controlada', 'Finalizada', 'Activa'][i % 3],
                    'creado_por': admin,
                    'registro_completado': True,
                },
            )
            Capacitacion.objects.get_or_create(
                nombre=f'Capacitación Demo {i:03d}',
                defaults={
                    'tipo_actividad': ['Curso', 'Taller', 'Charla', 'Reunión'][i % 4],
                    'malla': ['Nivel postulante', 'Nivel inicial', 'Nivel operativo', 'Otros'][i % 4],
                    'descripcion': f'Actividad ficticia de demostración número {i}.',
                    'fecha_inicio': timezone.now() + timedelta(days=i),
                    'lugar': f'Recinto Demo {1 + i % 5}',
                    'instructor': f'Instructor Demo {1 + i % 8}',
                    'cupos': 10 + (i % 31),
                    'creado_por': admin,
                },
            )
            Proyecto.objects.get_or_create(
                nombre=f'Proyecto Demo {i:03d}',
                defaults={
                    'descripcion': f'Proyecto ficticio número {i} para la demostración.',
                    'fecha_inicio': today - timedelta(days=i),
                    'presupuesto': f'{500000 + i * 125000}.00',
                    'responsable': brigadista,
                    'tipo': ['Infraestructura', 'Equipamiento', 'Capacitación', 'Otro'][i % 4],
                    'prioridad': 1 + (i * 13) % 100,
                    'creado_por': admin,
                },
            )
            Inventario.objects.get_or_create(
                nombre=nombres_inventario[i % len(nombres_inventario)],
                compania=compania,
                ubicacion=f'Bodega Demo {1 + i % 6} / lote {i:03d}',
                defaults={
                    'estado': ['Bueno', 'Regular', 'Malo', 'En Reparación'][i % 4],
                    'asignado_a_vehiculo': vehiculo if i % 2 == 0 else None,
                    'agregado_por': admin,
                    'valor': 50000 + i * 25000,
                },
            )
            Mantenimiento.objects.get_or_create(
                vehiculo=vehiculo.nombre,
                fecha=today - timedelta(days=i),
                defaults={
                    'descripcion': f'Mantenimiento ficticio de demostración {i}.',
                    'costo': f'{25000 + i * 7000}.00',
                    'responsable': admin,
                    'compania_caja': compania,
                    'tipo': ['Preventivo', 'Correctivo'][i % 2],
                },
            )
            CajaChica.objects.get_or_create(
                compania=compania,
                descripcion=f'Movimiento Demo {i:03d}',
                defaults={
                    'tipo': ['Ingreso', 'Egreso'][i % 2],
                    'tipo_cuenta': ['caja_propia', 'cuenta_bancaria'][i % 2],
                    'monto': f'{10000 + i * 5000}.00',
                    'responsable': admin,
                },
            )

        self.stdout.write(self.style.SUCCESS(f'Datos ficticios cargados: lote de hasta {cantidad} registros por módulo.'))
        self.stdout.write(f'Administrador de demo: {email}')
