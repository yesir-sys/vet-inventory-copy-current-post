from django.db import models

class MassOutgoing(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    medicine = models.CharField(max_length=200)
    quantity = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']