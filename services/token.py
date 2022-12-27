from datetime import timedelta
from schemas.token import Token
from daos.token_dao import TokenCRUD
from daos.user_dao import UserCRUD
from utils.app_exceptions import AppException
from services.main import AppService
from schemas.user import Credential as User
from utils.service_result import ServiceResult
from utils.auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_DAYS

class TokenService(AppService):

    def create_token(self, user: User) -> ServiceResult:

        exist = UserCRUD(self.db).get_user_by_username(user.username)

        if not exist:
            return ServiceResult(AppException.GetToken({"Message": "Incorrect username or password"}))

        is_logged = verify_password(user.password, exist.password)

        if not is_logged:
            return ServiceResult(AppException.TokenInvalidCredentials({"Message": "Incorrect username or password"}))
        
        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

        token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        token = TokenCRUD(self.db).create_token(exist.id, token)
        
        if not token:
            return ServiceResult(AppException.CreateToken({"Message": "Incorrect username or password"}))

        token = Token(access_token=token.token, token_type="Bearer")

        return ServiceResult(token)