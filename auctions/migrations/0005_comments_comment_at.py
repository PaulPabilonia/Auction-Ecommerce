# Generated by Django 3.2.8 on 2021-11-20 08:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20211112_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
