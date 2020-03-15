import datetime

from django.shortcuts import render
from parkinglot.models import ParkingSlot, Customer, ParkingSlotReservation, ParkingLot
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import *

@api_view(['GET'])
def index(request):
    return render(request, 'index.html')

def createSlotsForLot( lotSerializer ):
    numSlots = lotSerializer.data[ 'number_of_slots' ]
    slotList = []
    parkingLotObj = ParkingLot.objects.all()[ 0 ]
    for slotNumber in range( 1, numSlots+1 ):
        slotList.append( ParkingSlot( parkingLot=parkingLotObj, slotNumber=slotNumber ) )
    ParkingSlot.objects.bulk_create( slotList )

@api_view(['GET', 'POST'])
def createParkingLot(request):
    if request.method == 'POST':
        if not list(ParkingLot.objects.all()):
            serializer = ParkingLotSerializer( data=request.data )
            if serializer.is_valid():
                serializer.save()
                responseDict = { "status": "Parking Lot has been created with following config" }
                responseDict.update( serializer.data )
                response = Response( responseDict, status=status.HTTP_201_CREATED )

                # Create Slots
                createSlotsForLot( serializer )
            else:
                response = Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

            return response
        else:
            lotData = ParkingLot.objects.all()[ 0 ]
            content = { "status" : "Parking Lot already exists",
                        "name": lotData.name }
            return Response(content, status=status.HTTP_400_BAD_REQUEST )

    elif request.method == 'GET':
        if not list(ParkingLot.objects.all()):
            content = { "No Parking-Lot created" }
            return Response(content, status=status.HTTP_200_OK)
        else:
            # Assuming there will be only one Parking-Lot
            parkingLot = ParkingLot.objects.all()[ 0 ]
            lotSerializer = ParkingLotSerializer( parkingLot )
            content = lotSerializer.data
            return Response( content, status=status.HTTP_200_OK )
    
@api_view(['GET', 'POST'])
def customers( request ):
    """
    List customers, or create a new customer.
    """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        customers = Customer.objects.get_queryset().order_by('customer_name')
        page = request.GET.get('page', 1)
        paginator = Paginator(customers, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = CustomerSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/customers/?page=' + str(nextPage), 'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = CustomerSerializer( data=request.data )
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_201_CREATED )
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET', 'DELETE'])
def customers_detail( request, pk ):
    """
    Retrieve, update or delete a customer by id/pk.
    """
    try:
        customer = Customer.objects.get( pk=pk )
    except Customer.DoesNotExist:
        return Response( "Customer with contact-number: {} does not exist".format( pk ),
                         status=status.HTTP_404_NOT_FOUND )

    if request.method == 'GET':
        serializer = CustomerSerializer( customer )
        return Response( serializer.data )

    elif request.method == 'DELETE':
        reservations = ParkingSlotReservation.objects.filter(customer=customer)
        for res in reservations:
            slot_number = res.parking_slot_number
            slotHr = res.start_timestamp.hour
            duration = res.duration_in_hrs
            slot = ParkingSlot.objects.get(slotNumber=slot_number)
            slotBaseStr = 'slot_avail_hr_{:02d}'
            for tmpHr in range( slotHr, slotHr + duration ):
                timeSlotStr = slotBaseStr.format( tmpHr )
                setattr( slot, timeSlotStr, True )
                slot.save()
        customer.delete()
        return Response( status=status.HTTP_204_NO_CONTENT )


@api_view(['GET', 'POST'])
def reservations(request):
    """
    List parking slot reservations, or create a new reservation
    """
    if not list(ParkingLot.objects.all() ):
        return Response( { "Status" : "ParkingLot doesn't exist, please create one" },
                            status=status.HTTP_400_BAD_REQUEST )
        
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        reservations = ParkingSlotReservation.objects.get_queryset().order_by('vehicleRegNo')
        page = request.GET.get('page', 1)
        paginator = Paginator(reservations, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ParkingSlotReservationSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/reservations/?page=' + str(nextPage), 'prevlink': '/api/reservations/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = ParkingSlotReservationSerializer( data=request.data )
        if serializer.is_valid():
            
            # checking that the booking is made for the current day only                                                                               
            bookingDate = int ( request.data["booking_date"].split('-')[2] )
            todayDate = datetime.datetime.now().date().day
            if ( bookingDate != todayDate ):
                content = { 'Bookings can be made only for today' }
                return Response( content, status=status.HTTP_400_BAD_REQUEST )

            requestSlotHr = int( request.data["start_timestamp"].split(':')[0] )
            slotBaseStr = 'slot_avail_hr_{:02d}'
            slotStr = slotBaseStr.format( requestSlotHr )
            duration = int( request.data["duration_in_hrs"] )
            slotAvailable = False

            # check to discard redundant bookings:
            booking_customer_contact = request.data["customer"]
            booking_vehicleRegNo = request.data["vehicleRegNo"]
            bookingExists = False
            bookingTimeHr = int( request.data["start_timestamp"].split(':')[0] )
            for reservation in list (ParkingSlotReservation.objects.filter(vehicleRegNo=booking_vehicleRegNo) ):
                if ( reservation.start_timestamp.hour == bookingTimeHr and reservation.duration_in_hrs == int (request.data["duration_in_hrs"]) ):
                    bookingExists = True
                    break;
            if bookingExists:
                content = { 'Booking already exists' }
                return Response( content, status=status.HTTP_400_BAD_REQUEST )

            # checking that the booking doesn't extend to the next day
            if ( ( requestSlotHr + duration ) > 24 ):
                content = { "the booking period cannot extend to the next day" }
                return Response(content, status=status.HTTP_200_OK)
            
            for slot in ParkingSlot.objects.all():
                slotAvailable = True
                cost_per_hour = 40
                for tmpHr in range( requestSlotHr, requestSlotHr + duration ):
                    # Making sure that the slot under question is available for the whole time duration of booking
                    timeSlotStr = slotBaseStr.format( tmpHr )
                    tmpFieldVal = getattr( slot, timeSlotStr )
                    if not tmpFieldVal:
                        slotAvailable = False
                        break;

                if slotAvailable:
                    # Update ParkingSlot model
                    for tmpHr in range( requestSlotHr, requestSlotHr + duration ):
                        timeSlotStr = slotBaseStr.format( tmpHr )
                        setattr( slot, timeSlotStr, False )
                        slot.save()
                    # end of for tmpHr

                    # Add Reservation to ParkingSlotReservation model
                    request.data["parking_slot_number"] = slot.slotNumber
                    request.data["amount_to_be_paid"] = cost_per_hour * duration
                    serializer = ParkingSlotReservationSerializer( data=request.data )
                    if serializer.is_valid():
                        serializer.save()
                        return Response( serializer.data, status=status.HTTP_201_CREATED)
                # end of if slotAvailable
            # end of for slot

            if not slotAvailable:
                content = {'All the slots have been booked, please try after some time'}
                return Response(content, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        content = {'invalid input'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def parkingSlots( request ):
    """
    List Parking-Slots in a Parking-Lot, or create a new Parking-Slot
    """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        parkingSlots = ParkingSlot.objects.get_queryset().order_by( 'slotNumber' )
        page = request.GET.get('page', 1)
        paginator = Paginator(parkingSlots, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ParkingSlotSerializer(data, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response(
                {
                'data': serializer.data ,
                'count': paginator.count,
                'numpages' : paginator.num_pages,
                'nextlink': '/api/parkingSlots/?page={}'.format( str( nextPage ) ),
                'prevlink': '/api/parkingSlots/?page={}'.format( str(previousPage) )
                }
            )

    elif request.method == 'POST':
        # Data Validation
        if( len( request.data ) > 1 or
            len( request.data ) == 1 and not request.data.get( "parkingLot" ) ):
            return Response( { "Status" : "POST only accepts parkingLot name" }, status=status.HTTP_400_BAD_REQUEST )
        
        if ( len( request.data ) == 0 ):
            return Response( { "Status" : "POST method requires parkingLot name" }, status=status.HTTP_400_BAD_REQUEST )
        lotName = request.data[ 'parkingLot' ]
        try:
            parkingLotObj = ParkingLot.objects.get( name=lotName )
        except ParkingLot.DoesNotExist:
            return Response( { "Status" : "ParkingLot with a name: '{}' does not exist".format( lotName ) },
                             status=status.HTTP_400_BAD_REQUEST )

        numSlots = parkingLotObj.number_of_slots
        numSlots += 1
        data = request.data
        data.update( { "slotNumber" : numSlots } )
        serializer = ParkingSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Update ParkingLot table with number_of_slots
            setattr( parkingLotObj, "number_of_slots", numSlots )
            parkingLotObj.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def parkingLots(request):
    """
    List Parking-Lots
    """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        parkingLots = ParkingLot.objects.get_queryset().order_by('name')
        page = request.GET.get('page', 1)
        paginator = Paginator(parkingLots, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ParkingLotSerializer(data, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response(
                {
                'data': serializer.data ,
                'count': paginator.count,
                'numpages' : paginator.num_pages,
                'nextlink': '/api/parkingLots/?page={}'.format( str( nextPage ) ),
                'prevlink': '/api/parkingLots/?page=' + str(previousPage)
                }
            )
    elif request.method == 'POST':
        parkingLotList = list( ParkingLot.objects.all() )
        if not parkingLotList:
            serializer = ParkingLotSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = { "The Parking Lot model has already been created" }
            return Response( content, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           

@api_view(['GET', 'POST'])  
def parkingStatus( request ):

    if not list(ParkingLot.objects.all() ):
        return Response( { "Status" : "ParkingLot doesn't exist, please create one" },
                            status=status.HTTP_400_BAD_REQUEST )
    if request.method == 'POST':
        # Data Validation
        if( not( "start_time" in request.data and
                 "duration" in request.data and
                 len( request.data ) == 2 ) ):
            return Response( { "Status" : "ParkingStatus only accepts start_time (in hr:min:sec) and duration (in hours) parameters" },
                            status=status.HTTP_400_BAD_REQUEST )

        fromTime = request.data.get( 'start_time' )
        tmpDuration = request.data.get( 'duration' )
        timeHr = int( fromTime.split( ':' )[ 0 ] ) 
        duration = int( tmpDuration )
    elif request.method == 'GET':
        timeHr = datetime.datetime.now().hour
        duration = 1

    if timeHr + duration >= 24:
        return Response( "Provided duration crosses the day-boundary. Not Allowed",
                         status=status.HTTP_400_BAD_REQUEST )

    slotStatus = { "fromTime" : timeHr, "toTime" : timeHr+duration }
    slotBaseStr = "slot_avail_hr_{:02d}"
    for slot in ParkingSlot.objects.all():
        slotAvailable = True
        for tmpTime in range( timeHr, timeHr + duration ):
            fieldVal = getattr( slot, slotBaseStr.format( tmpTime ) )
            if not fieldVal:
                slotAvailable = False
                break;

        slotName = "slot_number_{}".format( slot.slotNumber )
        slotStatus[ slotName ] = "Available" if slotAvailable else "Not Available"

    return Response( slotStatus )
