from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, primary_key=True)
    password_hash = models.CharField(max_length=100)

    def __str__(self):
        return self.email + '-' + self.name


class Organisation(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=6)
    type = models.CharField(max_length=20)
    about = models.CharField(max_length=200)

    def __str__(self):
        return self.email + '_' + self.latitude + '_' + self.longitude

class AccidentLocation(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    orgs = models.CharField(max_length=1000)

    def __str__(self):
        return self.latitude + '_' + self.longitude





