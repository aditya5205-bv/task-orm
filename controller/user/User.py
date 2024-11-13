import sys_path
from sqlalchemy import literal_column, select, insert, and_, or_
from sqlalchemy.orm import Session
from logs.custom_logging import custom_logging
from model.UserData import UserData

class User():
    
    def __init__(self, session: Session):
        self._session = session
        self._user_id = None
        self._username = None
        self.is_user = False
        
        # super().__init__(db_config)

        
    def user_login(self, username, password):
        
        if self.is_user:
            custom_logging.warning("Some user is already logged in")
            return False
        
        try:
            stmt = select(UserData.user_id, UserData.user_password).where(and_(UserData.username == username 
                    ,UserData.user_password == password))
            
            if not self._session:
                custom_logging.info("Session is not initialized")
                return False
                
            res = self._session.execute(stmt)

            if res:
                user_id, user_password = res.fetchone()
                
                if user_password == password:
                    self.is_user = True
                    self._user_id = user_id
                    self._username = username
                    custom_logging.info(f"Login Successful. Welcome {self._username}")
                else:
                    custom_logging.error("Wrong username or password")
                    return False
                    
            else:
                custom_logging.error("Wrong username or password")
                return False
            
        
        except Exception as e:
            custom_logging.error(f"Login Error: {e}")
            trace_back = e.__traceback__
            custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
            #       f"Traceback to last instruction {trace_back.tb_frame}")

    def user_logout(self):
        if not self.is_user:
            custom_logging.warning("No user is logged in")
            return False
        
        else:
            temp_username = self._username
            self._user_id = None
            self._username = None
            self.is_user = False
            custom_logging.info(f"Logout Successful. Bye {temp_username}")
            return True
        
    
    def user_signup(self, username, email, password):
        if self.is_user:
            custom_logging.warning("Some user is already logged in")
            return False
        
        try:
            stmt = select(literal_column('1')).where(or_(UserData.username == username, UserData.user_email == email))
            
            if not self._session:
                custom_logging.info("Session is not initialized")
                return False
                
            is_duplicate_user = self._session.scalars(stmt)
            
            if is_duplicate_user:
                custom_logging.error("This username or email already exists")
                return False
                
            stmt = insert(UserData).values(username=username, user_email=email, user_password=password)

            self._session.execute(stmt)
            self._session.commit()

            custom_logging.info(f"Welcome {username}. Signup successful")
            

        except Exception as e:
            custom_logging.error(f"Login Error: {e}")
            trace_back = e.__traceback__
            custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
            #       f"Traceback to last instruction {trace_back.tb_frame}")