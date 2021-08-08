from .models import UserClient


class MainService:

    @staticmethod
    def get_user_client(user_id):
        try:
            return UserClient.objects.get(user_id=user_id)
        except UserClient.DoesNotExist:
            return None
