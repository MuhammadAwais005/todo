from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    srno = models.IntegerField()  # Not AutoField! Just IntegerField

    def __str__(self):
        return f"{self.user.username} - {self.title}"
