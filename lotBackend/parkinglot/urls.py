from django.conf.urls import url, include
from parkinglot import views

app_name = 'api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/customers/$', views.customers, name='customers'),
    url(r'^api/customers/(?P<pk>[0-9]*)$', views.customers_detail),
    url(r'^api/reservations/$', views.reservations, name='reservations'),
    url('^api/parkingSlots/$', views.parkingSlots, name='parkingSlots'),
    url('^api/parkingLots/$', views.parkingLots, name='parkinglots'),
    url('^api/parkingStatus/.*$', views.parkingStatus, name='parkingStatus'),
    url('^api/createParkingLot/$', views.createParkingLot, name='createParkingLot'),
]
