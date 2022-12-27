from schemas.user import UserData
from utils.app_exceptions import AppException
from daos.user_dao import UserCRUD
from services.main import AppService
from utils.service_result import ServiceResult
from utils.auth import hash_password
from utils.service_result import handle_result

class UserService(AppService):

    def get_user(self, id: int) -> ServiceResult:
        user = UserCRUD(self.db).get_user(id)
        
        if not user:
            return ServiceResult(AppException.GetUser({"Message": f"No se ha encontrado ningun usuario con el id: {id}"}))
        
        return ServiceResult(user)

    def get_user_by_username(self, username: str) -> ServiceResult:

        user = UserCRUD(self.db).get_user_by_username(username)

        if not user:
            return ServiceResult(AppException.GetUser({"Message": f"No se ha encontrado ningun usuario con el id: {username}"}))

        return ServiceResult(user)

    def get_all(self) -> ServiceResult:

        users = UserCRUD(self.db).get_all_users()

        if not users:
            return ServiceResult(AppException.GetAllUser({"Message": f"No se ha encontrado ningun objeto"}))

        return ServiceResult(users)

    def create_user(self, user: UserData) -> ServiceResult:

        user.password = hash_password(user.password)

        verify_username = UserCRUD(self.db).get_user_by_username(user.username)
        
        if(verify_username):
            return ServiceResult(AppException.CreateUser({"Message": f"Ya existe un usuario con el username: {user.username}"}))

        user = UserCRUD(self.db).create_user(user)
        
        if not user:
            return ServiceResult(AppException.CreateUser({"Message": f"No se ha podido crear el User"}))
        
        return ServiceResult(user)

    def update_user(self, id: int, user_request: UserData) -> ServiceResult:

        user_request.password = hash_password(user_request.password)

        if(user_db.username is not user_request.username):

            verify_username = UserCRUD(self.db).get_user_by_username(user_request.username)
        
            if(verify_username):
                return ServiceResult(AppException.CreateUser({"Message": f"Ya existe un usuario con el username: {user_request.username}"}))

        user_db = UserCRUD(self.db).get_user(id)

        if not user_db:
            return ServiceResult(AppException.GetUser({"Message": f"No se ha encontrado ningun User con el id"}))
        
        user = UserCRUD(self.db).update_user(user_request, user_db)

        if not user: 
            return ServiceResult(AppException.UpdateUser({"Message": f"No se ha encontrado ningun User con el id"}))

        return ServiceResult(user)

    def delete_user(self, id: int) -> ServiceResult:
        user = UserCRUD(self.db).get_user(id)

        if not user:
            return ServiceResult(AppException.GetUser({"Message": f"No se ha encontrado ningun User con el id"}))

        user = UserCRUD(self.db).delete_user(user)

        if not user:
            return ServiceResult(AppException.DeleteUser({"Message": f"No se ha encontrado ningun User con el id"}))

        return ServiceResult(user)