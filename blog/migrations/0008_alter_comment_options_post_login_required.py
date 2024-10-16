# Generated by Django 5.0.7 on 2024-09-27 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_date']},
        ),
        migrations.AddField(
            model_name='post',
            name='login_required',
            field=models.BooleanField(default=False),
        ),
    ]
