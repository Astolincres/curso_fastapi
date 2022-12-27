from schemas.user import User
from models.user import UsersDB
from schemas.user import Credential, UserData
from services.main import AppCRUD

class UserCRUD(AppCRUD):

    def get_user(self, id: int) -> User:
        user = self.db.query(UsersDB).filter(UsersDB.id == id).first()
        if user:
            return user
        return None

    def get_user_by_username(self, username: str) -> User:
        user = self.db.query(UsersDB).where(UsersDB.username == username, UsersDB.is_active == True, UsersDB.deleted == None).first()
        if user:
            return user
        return None    

    def get_all_users(self) -> User:
        all_users = self.db.query(UsersDB).all()
        if all_users:
            return all_users
        return None

    def create_user(self, user: UserData) -> User:
        user = UsersDB(
                    username = user.username,
                    password = user.password,
                    first_name = user.first_name,
                    last_name = user.last_name,
                    email = user.email,
                    rfc = user.rfc,
                    curp = user.curp
                )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, item: User, user: UsersDB) -> User:
        user.username = item.username,
        user.password = item.password,
        user.first_name = item.first_name,
        user.last_name = item.last_name,
        user.email = item.email,
        user.rfc = item.rfc,
        user.curp = item.curp
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user: UsersDB) -> User:
        self.db.delete(user)
        self.db.commit()
        return user
