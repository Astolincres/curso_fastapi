from models.token import TokenDB
from schemas.token import Token
from services.main import AppCRUD

from utils.enums import typeHistorial
from daos.historical_dao import Historical
from models.token import Historical_TokenDB

class TokenCRUD(AppCRUD):

    def get_token(self, id: int) -> TokenDB:
        token = self.db.query(TokenDB).filter(TokenDB.id == id).first()
        if token:
            return token
        return None

    def get_all_token(self) -> TokenDB:
        all_tokens = self.db.query(TokenDB).all()
        if all_tokens:
            return all_tokens
        return None

    def create_token(self,  user_id: int,  token: Token) -> TokenDB:
        token = TokenDB(user_id = user_id, token = token)
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        Historical(self.db).historical(token, Historical_TokenDB, typeHistorial.ADD.value, user_id)
        return token

    def update_token(self, item: Token, token: TokenDB) -> TokenDB:
        token.description = item.description
        token.public = item.public
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        Historical(self.db).historical(token, Historical_TokenDB, typeHistorial.UPDATE.value, token.user_id)
        return token
    
    def delete_token(self, token: TokenDB) -> TokenDB:
        self.db.delete(token)
        self.db.commit()
        Historical(self.db).historical(token, Historical_TokenDB, typeHistorial.DEL.value, token.user_id)
        return token

    def get_token_by_token(self, token:str) -> TokenDB:
        token_response = self.db.query(TokenDB).filter(TokenDB.token == token).first()
        if token_response:
            return token_response
        return None