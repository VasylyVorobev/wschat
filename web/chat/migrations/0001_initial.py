# Generated by Django 3.2.3 on 2021-08-08 18:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('received_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('is_system', models.BooleanField(default=False)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_at', '-received_at'),
            },
        ),
        migrations.CreateModel(
            name='RoomGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.BooleanField(default=1, verbose_name='Open or close')),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, max_length=254)),
                ('url', models.URLField(max_length=400)),
                ('content_type', models.CharField(choices=[('img', 'image'), ('sound', 'sound'), ('file', 'file')], max_length=100)),
                ('file_id', models.PositiveIntegerField(verbose_name='File id in Customer Host')),
            ],
        ),
        migrations.CreateModel(
            name='UsersRoomGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_room_set', to='chat.roomgroup')),
            ],
        ),
    ]
