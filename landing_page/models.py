from django.db import models

# Create your models here.

class Message(models.Model):
    email = models.EmailField(max_length=100)
    sender = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sent_datetime = models.DateTimeField('time and date sent')


    def __str__(self):
        return self.subject
