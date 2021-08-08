# Generated by Django 3.2.3 on 2021-08-08 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersroomgroup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_room_set', to='main.userclient'),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='message',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_file', to='chat.message'),
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_set', to='main.userclient'),
        ),
        migrations.AddField(
            model_name='message',
            name='room_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.roomgroup'),
        ),
        migrations.AlterUniqueTogether(
            name='usersroomgroup',
            unique_together={('user', 'room_group')},
        ),
    ]