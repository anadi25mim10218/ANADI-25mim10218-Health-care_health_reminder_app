from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from django.conf import settings
import datetime
# Create your models here.

class ProfileManager(models.Manager):
    def create(self,validated_data,user):
        profile = Profile(
            user = user,
            is_doctor = validated_data['is_doctor'],
            is_patient = validated_data['is_patient'],
            is_staffmember = validated_data['is_staffmember'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            dob = validated_data['dob'],
            photo = validated_data['photo'],
        )
        profile.save()
        return user

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)
    is_staffmember = models.BooleanField(default=False)
    firstName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=30, blank=True)
    dob = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='uploads', blank=True)
    address = models.CharField(max_length=1000, blank=True)
    address_city = models.CharField(max_length=30, blank=True)
    address_state = models.CharField(max_length=30, blank=True)
    address_pincode = models.CharField(max_length=6, blank=True)
    date_firstVisit = models.DateField(auto_now_add=True, blank=True)
    date_lastVisit = models.DateField(auto_now=True, blank=True)
    contact1 = models.CharField(max_length=30, blank=True)
    contact2 = models.CharField(max_length=30, blank=True)
    emailId1 = models.CharField(max_length=100, blank=True)
    emailId2 = models.CharField(max_length=100, blank=True)
    
    # objects = ProfileManager()

    def __str__(self):
        return str(self.user.username)
    # is_relative = models.BooleanField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class DoctorManager(models.Manager):
    def __init__(self):
        super(DoctorManager, self).__init__()
        self.is_doctor = True
    def create(self,**kwargs):
        user=kwargs['user']
        profile= Profile(
            user = user,
            is_doctor = self.is_doctor,
        )
        profile.save()
        dr = Doctor(**kwargs)
        dr.save()
        return dr
    
class PatientManager(models.Manager):
    def __init__(self):
        super(PatientManager, self).__init__()
        self.is_patient=True

    def create(self,**kwargs):
        user = kwargs['user']
        profile = Profile(
            user=user,
            is_patient = self.is_patient,
        )
        profile.save()
        pt = Patient(**kwargs)
        pt.save()
        return pt

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=False)
    department = models.CharField(max_length=30)
    designation = models.CharField(max_length=30)
    hospital = models.CharField(max_length=30)
    # objects = DoctorManager()
    def __str__(self):
        return (self.user.username)


class Patient(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name='self')
    relative1 = models.ForeignKey(User, models.CASCADE, related_name='relative1')
    relative2 = models.ForeignKey(User, models.CASCADE, related_name='relative2')
    relative3 = models.ForeignKey(User, models.CASCADE, related_name='relative3')
    date_firstVisit = models.DateField(auto_now_add=True)
    date_lastVisit = models.DateField(auto_now=True)

    def __str__(self):
        return (self.user.username)


class Staff(models.Model):
    user = models.OneToOneField(User, models.CASCADE, blank=True, null=True)
    department = models.CharField(max_length=30)
    designation = models.CharField(max_length=30)
    hospital = models.CharField(max_length=30)
    
    def __str__(self):
        return (self.user.username)


class Exercise(models.Model):
    exerciseId = models.AutoField(primary_key=True)
    doctorId = models.ForeignKey(Doctor, models.CASCADE, blank=True, null=True)
    exercise_code = models.CharField(max_length=8, blank=True, null=True)
    exercise_name = models.CharField(max_length=30, blank=True, null=True)
    instructions = models.CharField(max_length=1000, blank=True, null=True)
    level = models.IntegerField(default=1)

    def __str__(self):
        return str(self.exerciseId)

    def save(self, *args, **kwargs):
        super(Exercise, self).save(*args, **kwargs)


class Treatment(models.Model):
    treatmentId = models.AutoField(primary_key=True)
    doctorId = models.ForeignKey(Doctor, models.CASCADE, blank=True, null=True)
    patientId = models.ForeignKey(
        Patient, models.CASCADE, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    medicines = models.CharField(max_length=100)
    exercises = models.ManyToManyField(Exercise, blank=True )
    staff1 = models.ForeignKey(Staff, models.CASCADE, blank=True, null=True, related_name='staff1')
    staff2 = models.ForeignKey(Staff, models.CASCADE, blank=True, null=True, related_name='staff2')
    # relative1 = models.ForeignKey('Relative', on_delete=models.CASCADE, related_name='relative1')
    # relative2 = models.ForeignKey('Relative', on_delete=models.CASCADE, related_name='relative2')

    def __str__(self):
        return str(self.treatmentId)

    class Meta:
        ordering = ['start_date']


# class Relative(models.Model):
#     user = models.ForeignKey(User, models.CASCADE, blank=True, null=True, related_name='self_userid')
#     relativeId = models.ForeignKey(User, models.CASCADE, blank=True, null=True, related_name='relative_userid')
    
#     def __str__(self):
#         return self.user


class Record(models.Model):
    recordId = models.AutoField(primary_key=True)
    treatmentId = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    confirmationFromRelative1 = models.BooleanField(default=False)
    markAsDone = models.BooleanField(default=False)

    def __str__(self):
        return str(self.recordId)

class Notification(models.Model):
    nId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, models.CASCADE, related_name='relativeName')
    treatmentId = models.ForeignKey(Treatment, models.CASCADE)
    patientId = models.ForeignKey(Patient, models.CASCADE)
    dateNotified = models.DateField(auto_now_add=True) 

    def __str__(self):
        return str(self.nId)