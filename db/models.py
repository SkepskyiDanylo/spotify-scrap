from django.db import models


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    song_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}, {self.email}, {self.song_type}"


class Track(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    popularity = models.IntegerField()
    place = models.IntegerField()
    link = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
