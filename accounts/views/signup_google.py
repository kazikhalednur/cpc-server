from rest_framework.generics import CreateAPIView

from ..serializers import SignupGoogleSerializer


class SignupGoogleView(CreateAPIView):
    """
    Sign Up with Google view.
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = SignupGoogleSerializer
