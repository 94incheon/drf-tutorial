from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user_app.api.serializers import RegistrationSerializer


@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
