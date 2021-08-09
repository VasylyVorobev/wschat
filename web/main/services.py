from .models import UserClient


class MainService:

    @staticmethod
    def get_user_client(user_id: int):
        try:
            return UserClient.objects.get(user_id=user_id)
        except UserClient.DoesNotExist:
            return None

    @staticmethod
    def is_user_client_exist(user_id: int) -> bool:
        return UserClient.objects.filter(user_id=user_id).exists()
