from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    zone = models.CharField(max_length=255)
    district_name = models.CharField(max_length=255, unique=True)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.district_name

class Club(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name='clubs')

    def __str__(self):
        return self.name

class RotaryYear(models.Model):
    year = models.CharField(max_length=4, unique=True)
    rotary_full_year = models.CharField(max_length=255)  # New field
    is_closed = models.BooleanField(default=False)
    notice = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.year

class RotaryYearFile(models.Model):
    rotary_year = models.ForeignKey(RotaryYear, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='admin_files/')

    def __str__(self):
        return f'{self.rotary_year.year} - {self.file.name}'

class ClubReport(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    rotary_year = models.ForeignKey(RotaryYear, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='club_reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.club.name} - {self.rotary_year.year}'

class ClubBudget(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    rotary_year = models.ForeignKey(RotaryYear, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.club.name} - {self.rotary_year.year} - ${self.amount}'
