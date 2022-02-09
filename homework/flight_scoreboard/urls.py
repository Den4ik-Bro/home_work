from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('flights', viewset=views.FlightsApiViewSet, base_name='flights')
router.register('citys', viewset=views.CityApiViewSet, base_name='citys')
router.register('statuses', viewset=views.StatusApiViewSet, base_name='statuses')
router.register('type_airplanes', viewset=views.TypeAirPlaneApiViewSet, base_name='type_airplanes')

app_name = 'flight_scoreboard'


urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^detail_flight/(?P<pk>[0-9]+)/$', views.DetailFlightView.as_view(), name='current_flight'),
    url(r'^detail_flight/(?P<pk>[0-9]+)/edit/$', views.UpdateFlightView.as_view(), name='edit_flight'),
    url(r'^delete_flight/(?P<pk>[0-9]+)/$', views.DeleteFlightsView.as_view(), name='delete_flight'),
    url(r'^create_flight/$', views.CreateFlightView.as_view(), name='create_flight'),
    url('^api/', include(router.urls)),
]
