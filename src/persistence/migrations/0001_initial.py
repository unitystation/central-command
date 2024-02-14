# Generated by Django 3.2.22 on 2023-11-11 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import persistence.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fork_compatibility', models.CharField(default='Unitystation', help_text='What fork is this character compatible with? This is a simple string, like "Unitystation" or "tg".', max_length=25)),
                ('character_sheet_version', models.CharField(help_text='What character sheet version is this character compatible with? This should be semantically versioned, like "1.0.0" or "0.1.0".', max_length=10, validators=[persistence.validators.validate_semantic_version])),
                ('data', models.JSONField(help_text='Unstructured character data in JSON format.', verbose_name='Character data')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
