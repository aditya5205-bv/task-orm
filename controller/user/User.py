import sys_path
from sqlalchemy import literal_column, select, insert, and_, or_
from sqlalchemy.orm import Session
from logs.custom_logging import custom_logging
from model.UserData import UserData
from redis import Redis
from model.redis_cache.RedisCache import RedisCache

class User:
    
    def __init__(self):
        self._session = None
        self._user_id = None
        self._username = None
        self.is_user = False
        self._redis_conn = None
        # super().__init__(db_config)
        
    def initialize_db(self, session: Session):
        self._session = session
        
    def initialize_redis(self, redis_conn: Redis):
        self._redis_conn = redis_conn
        
    def user_login(self, username, password):
        
        if self.is_user:
            custom_logging.warning("Some user is already logged in")
            return False
        
        try:
            stmt = select(UserData.user_id, UserData.user_password).where(and_(UserData.username == username 
                    ,UserData.user_password == password))
            
            if self._session is None:
                custom_logging.info("Session is not initialized")
                return False
                
            res = self._session.execute(stmt)
            res = res.fetchone()
            
            if res:
                user_id, user_password = res
                
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
            stmt = select(literal_column('1')).where(or_(UserData.username == username, \
                UserData.user_email == email))
            
            if self._session is None:
                custom_logging.info("Session is not initialized")
                return False
                
            is_duplicate_user = self._session.scalars(stmt).all()
            
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
            
            
            
    def get_user_data(self):
        if not self.is_user:
            custom_logging.warning("Log in to see your data")
            return False
        
        try:
            user_data = {}
            cols = ["username", "email", "created_at", "updated_at"]
            
            # checking redis cache if this data is available
            if self._redis_conn is None:
                custom_logging.error("Redis not initialized")
                return False
            
            redis = RedisCache(self._redis_conn)
            
            REDIS_USER_DATA_KEY = f"{self._username}-{self._user_id}"
            cached_data = redis.get(REDIS_USER_DATA_KEY)
        
            # if not found, getting the data from database
            if not cached_data:
            
                stmt = select(UserData.username, UserData.user_email, UserData.created_at,\
                    UserData.updated_at).where(UserData.user_id == self._user_id)
                
                if not self._session:
                    custom_logging.info("Session is not initialized")
                    return False
                    
                res = self._session.execute(stmt)
                res = res.fetchone()

                if res:
                    if len(res) != len(cols):
                        custom_logging.error("Query results mismatch. Can't zip")
                        return False
                    
                    user_data = dict(zip(cols, res))

                    # setting the query results in redis 
                    redis.set(REDIS_USER_DATA_KEY, user_data)
                
            # if data is found, then return it
            else:
                user_data = cached_data
        
            print(f"{'Username' : <12} : {user_data.get("username")}")
            print(f"{'Email' : <12} : {user_data.get("email")}")
            print(f"{'Created at' : <12} : {user_data.get("created_at")}")
            print(f"{'Updated at' : <12} : {user_data.get("updated_at")}")
                    
                    
        except Exception as e:
            custom_logging.error(f"Login Error: {e}")
            trace_back = e.__traceback__
            custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
            #       f"Traceback to last instruction {trace_back.tb_frame}")
        
        