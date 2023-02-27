# Generated by Django 4.1.7 on 2023-02-15 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common_objects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commoncategory',
            name='parent',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='common_objects.commoncategory', verbose_name='父类别'),
        ),
    ]
