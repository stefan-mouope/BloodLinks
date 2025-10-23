from rest_framework import serializers
from .models import Don



class DonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Don
        fields = '__all__'
