from accounts.serializers import UserSerializer


def jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'resuest': request}).data
    }
