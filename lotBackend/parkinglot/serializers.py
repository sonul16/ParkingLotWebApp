from rest_framework import serializers
from .models import Customer, ParkingSlotReservation, ParkingSlot, ParkingLot


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_name', 'email', 'contact_number', 'address')


class ParkingSlotReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlotReservation
        fields = ('pk', 'customer', 'vehicleRegNo', 'start_timestamp',
                  'duration_in_hrs', 'booking_date', 'parking_slot_number', 'amount_to_be_paid')


class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = ('pk', 'parkingLot', 'slotNumber', 'slot_avail_hr_00',
                  'slot_avail_hr_01', 'slot_avail_hr_02', 'slot_avail_hr_03',
                  'slot_avail_hr_04', 'slot_avail_hr_05', 'slot_avail_hr_06',
                  'slot_avail_hr_07', 'slot_avail_hr_08', 'slot_avail_hr_09',
                  'slot_avail_hr_10', 'slot_avail_hr_11', 'slot_avail_hr_12',
                  'slot_avail_hr_13', 'slot_avail_hr_14', 'slot_avail_hr_15',
                  'slot_avail_hr_16', 'slot_avail_hr_17', 'slot_avail_hr_18',
                  'slot_avail_hr_19', 'slot_avail_hr_20', 'slot_avail_hr_21',
                  'slot_avail_hr_22', 'slot_avail_hr_23')


class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = ('name', 'number_of_slots',
                  'address', 'operating_company_name')
