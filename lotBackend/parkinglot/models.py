
from django.db import models
import uuid
import datetime
from django.core.validators import RegexValidator

# Create your models here.


class ParkingLot(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    number_of_slots = models.PositiveIntegerField()
    address = models.CharField(max_length=500)
    operating_company_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ParkingSlot(models.Model):
    parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    slotNumber = models.PositiveIntegerField()
    slot_avail_hr_00 = models.BooleanField(default=True)
    slot_avail_hr_01 = models.BooleanField(default=True)
    slot_avail_hr_02 = models.BooleanField(default=True)
    slot_avail_hr_03 = models.BooleanField(default=True)
    slot_avail_hr_04 = models.BooleanField(default=True)
    slot_avail_hr_05 = models.BooleanField(default=True)
    slot_avail_hr_06 = models.BooleanField(default=True)
    slot_avail_hr_07 = models.BooleanField(default=True)
    slot_avail_hr_08 = models.BooleanField(default=True)
    slot_avail_hr_09 = models.BooleanField(default=True)
    slot_avail_hr_10 = models.BooleanField(default=True)
    slot_avail_hr_11 = models.BooleanField(default=True)
    slot_avail_hr_12 = models.BooleanField(default=True)
    slot_avail_hr_13 = models.BooleanField(default=True)
    slot_avail_hr_14 = models.BooleanField(default=True)
    slot_avail_hr_15 = models.BooleanField(default=True)
    slot_avail_hr_16 = models.BooleanField(default=True)
    slot_avail_hr_17 = models.BooleanField(default=True)
    slot_avail_hr_18 = models.BooleanField(default=True)
    slot_avail_hr_19 = models.BooleanField(default=True)
    slot_avail_hr_20 = models.BooleanField(default=True)
    slot_avail_hr_21 = models.BooleanField(default=True)
    slot_avail_hr_22 = models.BooleanField(default=True)
    slot_avail_hr_23 = models.BooleanField(default=True)


class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone_regex = RegexValidator(
        regex=r'^[6-9]\d{9}$', message="Phone number must be entered in the format: '[6-9]239464379'. 10 digits required")
    contact_number = models.CharField(
        validators=[phone_regex], max_length=12, primary_key=True, unique=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.customer_name


class ParkingSlotReservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicleRegNo = models.CharField(max_length=10)
    start_timestamp = models.TimeField()
    duration_in_hrs = models.PositiveIntegerField(default=0)
    booking_date = models.DateField(default=datetime.date.today)
    parking_slot_number = models.PositiveIntegerField(default=0)
    amount_to_be_paid = models.PositiveIntegerField(default=0)
