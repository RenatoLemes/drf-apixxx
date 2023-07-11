from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    """
    List all profiles
    No Create View (post method), as profile creation handled by django signals
    """
    def get(self, request):
        profiles = Profile.objects.all() #Create profile
        serializer = ProfileSerializer(profiles, many=True) #Serializer them
        return Response(serializer.data) #send serializer data to response


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer #gives a proper form to update the user
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)