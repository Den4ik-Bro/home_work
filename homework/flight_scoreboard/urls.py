from django.conf.urls import url
from . import views


app_name = 'flight_scoreboard'


urlpatterns = [
    url(r'^$', views.FlightListView.as_view(), name='flight_list'),
    url(r'^detail_flight/(?P<pk>[0-9]+)/$', views.DetailFlightView.as_view(), name='current_flight'),
    url(r'^detail_flight/(?P<pk>[0-9]+)/edit/$', views.UpdateFlightView.as_view(), name='edit_flight'),
    url(r'^delete_flight/(?P<pk>[0-9]+)/$', views.DeleteFlightsView.as_view(), name='delete_flight'),
    url(r'^create_flight/$', views.CreateFlightView.as_view(), name='create_flight'),
    url(r'^api/flights_list/$', views.GetAllFlight.as_view(), name='flight_list_api'),
]
