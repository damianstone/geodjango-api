from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from api import models, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.contrib.auth.hashers import make_password
from decimal import *
import json

# simple json token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# --------------------------------- MANAGE AUTHENTICATION --------------------------------
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = serializers.UserSerializer(self.user).data
        for key, value in serializer.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# --------------------------------- USER MODEL VIEW SET --------------------------------

class UserModelViewSet(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["get"], url_path=r"actions/list-by-distance")
    def list_by_distance(self, request):
        user = request.user
        pnt = user.location
        
        queryset = models.User.objects.all().filter(location__distance_lt=(pnt, D(km=10)))
        user_serializer = serializers.UserSerializer(queryset, many=True)
        return Response({"count": queryset.count(), "distance": "10km", "results": user_serializer.data})
    
    # register user
    def create(self, request):
        data = request.data
        fields_serializer = serializers.UserSerializer(data=request.data)
        fields_serializer.is_valid(raise_exception=True)
            
        lat = fields_serializer.validated_data["lat"]
        lon = fields_serializer.validated_data["lon"]
    
        # update the location point using the new lat and lon
        point = {
            "type": "Point",
            "coordinates": [lat, lon]
        }
        
        user = models.User.objects.create(
            firstname = data['firstname'],
            email=data['email'],
            username=data["email"],
            password=make_password(data['password']),
            lat=fields_serializer.validated_data["lat"],
            lon=fields_serializer.validated_data["lon"], 
            location = GEOSGeometry(json.dumps(point), srid=4326)
        )
        
        user_serializer = serializers.UserSerializer(user, many=False)
        return Response(user_serializer.data)
        
    # update user
    def update(self, request, pk=None, *args, **kwargs):
        user = models.User.objects.get(id=pk)
        
        # receives lat and lon
        fields_serializer = serializers.UserSerializer(data=request.data, partial=True)
        fields_serializer.is_valid(raise_exception=True)

        
        lat = fields_serializer.validated_data["lat"]
        lon = fields_serializer.validated_data["lon"]
        
        # update the location point using the new lat and lon
        point = {
            "type": "Point",
            "coordinates": [lat, lon]
        }
        
        user.lat = fields_serializer.validated_data["lat"]
        user.lon = fields_serializer.validated_data["lon"]
        user.location = GEOSGeometry(json.dumps(point), srid=4326)
        user.save()
        
        user_serializer = serializers.UserSerializer(user, many=False)
        return Response(user_serializer.data)
        

# -------------- SIMPLE ENDPOINT TO POST LOCATIONS AND RETURN NEAREST LOCATION AROUND --------------------------------

class getLocationsWithinDistance(ModelViewSet):

    def create(self, request):
        serializer = serializers.LocationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.data
                print('DATA -> ', data)

               # from documentation distance queries (distance lookups)
               # this is the center point
                pnt = GEOSGeometry('POINT({} {})'.format(
                    data['long'], data['lat']), srid=4326)

                locations = models.Location.objects.all()

                print(len(locations))
                print('POINT({} {})'.format(
                    data['long'], data['lat']))

                # point is because in the model the property is named point
                qs = models.Location.objects.all().filter(point__distance_lt=(pnt, D(km=10)))


                return Response({"results": str(qs), "count": qs.count()})
            except Exception as e:
                print(e)

        return Response({"fucking": "error"})
