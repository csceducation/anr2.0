from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    notes = models.TextField(blank=True, null=True)
    #staff = models.ForeignKey('staffs.Staff',on_delete=models.CASCADE,null=True,blank=True)
    #student = models.ForeignKey('students.Student',on_delete=models.CASCADE,null=True,blank=True)
    

class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Academic Session"""

    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    """Academic Term"""

    name = models.CharField(max_length=20, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Subject"""

    name = models.CharField(max_length=200, unique=True)
    duration = models.CharField(max_length=200,blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
class Book(models.Model):
    """Book"""

    name = models.CharField(max_length=200, unique=True,blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
class Time(models.Model):
    """Timing"""

    time = models.CharField(max_length=200,blank=True)

    class Meta:
        ordering = ["time"]

    def __str__(self):
        return self.time
class Exam(models.Model):
    """Exam"""

    name = models.CharField(max_length=200, unique=True,blank=True)
    exam_mode = models.CharField(max_length=255,choices=[("Online","online"),("Offline","Offline")],default="Offline")
    exam_duration = models.CharField(max_length=200,blank=True)


    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name
