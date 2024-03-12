# Generated by Django 3.2.23 on 2024-03-08 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0003_vehicle_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleimage',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vehicle.vehicle'),
        ),
        migrations.AlterField(
            model_name='vehiclevideo',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='vehicle.vehicle'),
        ),
    ]