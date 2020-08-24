# IMPORT THE REQUIRED MODULES
from rest_framework import serializers

# IMPORT PROFILE MODEL 
from .models import Profile

# DEFINE CLASS FOR PROFILE SERIALIZER AT A DEPTH OF 1(TO INCLUDE THE USER IN RESPONSE)
class ProfileSerializer(serializers.ModelSerializer):

	# INCLUDE PROFILE MODEL FIELD USING META CLASS OF SERIALIZERS
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1