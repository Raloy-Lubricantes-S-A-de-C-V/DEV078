from django.db import models
from django.contrib.auth.models import User

class ModelChemicalSampling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    type_test = models.CharField(max_length=60)
    analyst_request = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    id_template = models.IntegerField(null=True, blank=True)
    templates = models.CharField(max_length=100, null=True, blank=True)
    product_db = models.CharField(max_length=30, null=True, blank=True)
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
    min_val = models.CharField(max_length=64, null=True, blank=True)
    recurrent_val = models.CharField(max_length=64, null=True, blank=True)
    max_val = models.CharField(max_length=64, null=True, blank=True)
    val_result = models.CharField(max_length=64, null=True, blank=True)
    price_unit = models.FloatField()

    def __str__(self):
        return f'{self.id_chemical_samples} - {self.test_name}'

