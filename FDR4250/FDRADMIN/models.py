from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

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
    year = models.CharField(max_length=255, unique=True)
    rotary_full_year = models.CharField(max_length=255)
    notice = models.TextField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.year

class RotaryYearFile(models.Model):
    file = models.FileField(upload_to='rotary_year_files/', validators=[validate_file_extension])
    rotary_year = models.ForeignKey(RotaryYear, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.rotary_year.year} - {self.file.name}'

class ClubReport(models.Model):
    file = models.FileField(upload_to='club_reports/', validators=[validate_file_extension])
    rotary_year = models.ForeignKey(RotaryYear, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    is_authorized = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)
    decline_date = models.DateTimeField(null=True, blank=True)

    def approve(self):
        self.is_authorized = True
        self.is_declined = False
        self.approval_date = timezone.now()
        self.save()

    def decline(self):
        self.is_authorized = False
        self.is_declined = True
        self.decline_date = timezone.now()
        self.save()

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
