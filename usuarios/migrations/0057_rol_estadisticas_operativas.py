from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0056_guia_agregar_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='ver_estadisticas_operativas',
            field=models.BooleanField(default=False, verbose_name='Estadísticas Operativas'),
        ),
    ]
