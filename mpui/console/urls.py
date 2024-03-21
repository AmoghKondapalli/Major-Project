from django.urls import path
from . import views

urlpatterns= [
    path('home',views.home,name='home'),
    path('',views.home,name='home'),
    path('pcap',views.pcap, name = 'pcap'),
    path('downthreat',views.downthreat,name = 'downthreat'),
    path('upload',views.upload,name='upload')
]