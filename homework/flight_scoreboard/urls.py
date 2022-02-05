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
    url(r'^$', views.home, name='home'),
    url(r'^detail_flight/(?P<flight_id>[0-9]+)/$', views.detail_flight, name='current_flight'),
    url(r'^detail_flight/(?P<flight_id>[0-9]+)/edit/$', views.edit_flight, name='edit_flight'),
    url(r'^delete_flight/(?P<flight_id>[0-9]+)/$', views.delete_flight, name='delete_flight'),
    url(r'^create_flight/$', views.create_flight, name='create_flight'),
    url('^api/', include(router.urls)),
]
