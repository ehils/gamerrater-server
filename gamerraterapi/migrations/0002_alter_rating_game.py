# Generated by Django 4.0.4 on 2022-05-12 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamerraterapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='gamerraterapi.game'),
        ),
    ]