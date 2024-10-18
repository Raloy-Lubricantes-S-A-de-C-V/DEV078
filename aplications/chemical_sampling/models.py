from django.db import models
from django.contrib.auth.models import User

class ModelChemicalSampling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    type_test = models.CharField(max_length=60)
    analyst_request = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    id_template = models.IntegerField()
    templates = models.CharField(max_length=100)
    product_db = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    method = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class ModelTemplates(models.Model):
    id_chemical_samples = models.ForeignKey(ModelChemicalSampling, on_delete=models.CASCADE)
    t_number = models.SmallIntegerField()
    test_name = models.CharField(max_length=60)
    test_time = models.CharField(max_length=20)
    astmd = models.CharField(max_length=100)
    min_val = models.CharField(max_length=64)
    recurrent_val = models.CharField(max_length=64)
    max_val = models.CharField(max_length=64)
    val_result = models.CharField(max_length=64)
    price_unit = models.IntegerField()

    def __str__(self):
        return f'{self.id_chemical_samples} - {self.test_name}'

