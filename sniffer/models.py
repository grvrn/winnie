from django.db import models

# Create your models here.
class Packet(models.Model):
    srcip = models.GenericIPAddressField(null=True, blank=True)
    sport = models.IntegerField(null=True, blank=True)
    dstip = models.GenericIPAddressField(null=True, blank=True)
    dsport = models.IntegerField(null=True, blank=True)
    proto = models.CharField(max_length=16, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.srcip} -> {self.dstip} ({self.proto})"
