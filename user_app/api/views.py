from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from user_app.api.serializers import RegistrationSerializer


@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        serializer.is_valid(raise_exception=True)
        account = serializer.save()

        data['response'] = 'Registration Successful!'
        data['username'] = account.username
        data['email'] = account.email

        token = Token.objects.get(user=account)
        data['token'] = token.key

        return Response(data, status=status.HTTP_201_CREATED)
