import requests
from django.db import models

class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album_cover = models.ImageField(upload_to='album_covers/', null=True, blank=True)
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)

    def __str__(self):
        return self.name




