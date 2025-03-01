from src.app.user.model.user_data import UserData
from src.app.user.repository.user_data import UserDataRepository
from src.app.user.service.user_data import UserDataService

user_data_repository = UserDataRepository(UserData)
user_data_service = UserDataService(user_data_repository)
