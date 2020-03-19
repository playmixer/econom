from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class CreatUserView(APIView):
    def post(self, request):
        data = request.data
        serialized = UserSerializer(data=data)
        if serialized.is_valid():
            User.objects.create_user(
                data['email'],
                data['username'],
                data['password']
            )
            return Response({"registration": serialized.data}, 201)
        else:
            return Response({"error": serialized._errors}, 400)
