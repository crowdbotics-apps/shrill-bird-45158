# Generated by Django 3.2.23 on 2024-03-01 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auction', '0002_alter_auction_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auction',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='auction',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='auction',
            name='vehicle',
        ),
    ]
