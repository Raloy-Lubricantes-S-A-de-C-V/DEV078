from django.db import models

class UsersModel(models.Model):
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length = 100, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
