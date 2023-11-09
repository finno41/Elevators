from django.db import models
import uuid
from datetime import datetime
# Create your models here.


class Elevator(models.Model):
    number = models.IntegerField(primary_key=True, editable=False)
    current_floor = models.IntegerField(default=0)


class Settings(models.Model):
    number_of_floors = models.IntegerField()
    number_of_elevators = models.IntegerField()


class ElevatorJourney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    elevator = models.ForeignKey(
        Elevator, on_delete=models.CASCADE, blank=False, null=False)
    floor_from = models.IntegerField()
    floor_to = models.IntegerField()
    created_on = models.DateTimeField(default=datetime.now())
