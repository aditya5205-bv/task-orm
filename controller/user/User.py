import sys_path
from sqlalchemy import literal_column, select, insert, and_, or_
from logs.custom_logging import custom_logging
from model.UserData import UserData
from connection.connections import db_connection, redis_connection

class User:
    
    def __init__(self):
        self._user_id = None
        self._username = None
        self.is_user = False
        
    def user_login(self, username, password):
        
        if self.is_user:
            custom_logging.warning("Some user is already logged in")
            return False
        
        try:
            query = select(UserData.user_id, UserData.user_password).where(and_(UserData.username == username 
                    ,UserData.user_password == password))
                
            res = db_connection.execute_query(query)
            
            if res:
                user_id, user_password = res[0]
                
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
            custom_logging.error(f"Login Error: {e}", exc_info=True)
            

    def user_logout(self):
        if not self.is_user:
            custom_logging.warning("No user is logged in")
            return False
        
        else:
            db_connection.disconnect()
            self._user_id = None
            self.is_user = False
            custom_logging.info(f"Logout Successful. Bye {self._username}")
            self._username = None
            return True
        
    def user_signup(self, username, email, password):
        if self.is_user:
            custom_logging.warning("Some user is already logged in")
            return False
        
        try:
            query = select(literal_column('1')).where(or_(UserData.username == username, \
                UserData.user_email == email))
                
            is_duplicate_user = db_connection.execute_query(query)
            
            if is_duplicate_user:
                custom_logging.error("This username or email already exists")
                return False
                
            query = insert(UserData).values(username=username, user_email=email, user_password=password)

            db_connection.execute_query(query)

            custom_logging.info(f"Welcome {username}. Signup successful")

        except Exception as e:
            custom_logging.error(f"Signup Error: {e}", exc_info=True)
            
            
    def get_user_data(self):
        if not self.is_user:
            custom_logging.warning("Log in to see your data")
            return False
        
        try:
            user_data = {}
            cached_data = None
            cols = ["username", "email", "created_at", "updated_at"]
            
            # checking redis cache if this data is available
            REDIS_USER_DATA_KEY = f"{self._username}-{self._user_id}"
            cached_data = redis_connection.get(REDIS_USER_DATA_KEY)
            
            # if not found, getting the data from database
            if not cached_data:  
            
                query = select(UserData.username, UserData.user_email, UserData.created_at,\
                    UserData.updated_at).where(UserData.user_id == self._user_id)
                
                    
                res = db_connection.execute_query(query)
                res = res[0]
                
                if res:
                    if len(res) != len(cols):
                        custom_logging.error("Query results mismatch. Can't zip")
                        return False
                    
                    user_data = dict(zip(cols, res))

                    # setting the query results in redis 
                    redis_connection.set(REDIS_USER_DATA_KEY, user_data)
                
            # if data is found, then return it
            else:
                user_data = cached_data
        
            print(f"{'Username' : <12} : {user_data.get("username")}")
            print(f"{'Email' : <12} : {user_data.get("email")}")
            print(f"{'Created at' : <12} : {user_data.get("created_at")}")
            print(f"{'Updated at' : <12} : {user_data.get("updated_at")}")
                    
                    
        except Exception as e:
            custom_logging.error(f"Getting user data error: {e}", exc_info=True)
        
        finally:
            redis_connection.disconnect()
        