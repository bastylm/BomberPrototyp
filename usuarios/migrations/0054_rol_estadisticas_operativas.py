from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0053_chatbot_reglas'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='ver_estadisticas_operativas',
            field=models.BooleanField(default=False, verbose_name='Estadísticas Operativas'),
        ),
    ]
