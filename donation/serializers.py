from rest_framework import serializers
from .models import Don, FaireDon

class FaireDonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaireDon
        fields = '__all__'


class DonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Don
        fields = '__all__'
