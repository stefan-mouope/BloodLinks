from django.urls import path
from .views import BanqueDeSangListView, BanqueDeSangDetailView

urlpatterns = [
    path('banques/', BanqueDeSangListView.as_view(), name='banque-list'),
    path('banques/<int:pk>/', BanqueDeSangDetailView.as_view(), name='banque-detail'),
]
