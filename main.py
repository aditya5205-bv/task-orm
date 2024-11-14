import time
from controller.user.User import User
from logs.custom_logging import custom_logging
from settings import DB_CONFIG, REDIS_CONN
from connection.Connection import Connection
from connection.RedisConnection import RedisConnection
import re

if __name__ == "__main__":

    try:
        conn = Connection()
        conn.initialize(DB_CONFIG)
    
        with conn.get_session() as session:
            
            user = User()
            redis_conn = RedisConnection(REDIS_CONN)
            redis_conn.initialize()
            
            user.initialize_db(session)
            
            while True:

                prompt = "- My data \n- Logout" if user.is_user == True else "- Login \n- Signup"
                input_text = (f"Enter Your Task \n{prompt}  \n- Exit \n")
                
                todo_input = input(input_text)
                todo_input = "".join(todo_input.split()).lower()
                
                
                if todo_input == 'exit':
                    custom_logging.info('Exitting ......')
                    break
                
                elif todo_input == 'logout':
                    user.user_logout()
                    break   

                elif todo_input == 'login':
                    username = input('Username: ')
                    password = input('Password: ')
                    
                    if username and password:
                        user.user_login(username,password)
                    else:
                        custom_logging.warning("Invalid username or password")
                        
                elif todo_input == 'signup':
                    username = input('Username: ')
                    email = input('Email: ')
                    password = input('Password: ')
                    
                    email_pattern = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)"
                                r"*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]"
                                r"*[a-z0-9])?")
                    email_verification = re.match(email_pattern, email)
                                
                    if username and password and email:
                        if email_verification:
                            user.user_signup(username, email, password)
                        else: 
                            custom_logging.error("Invalid email")
                    else:
                        custom_logging.error("Invalid input. Try again.")
                        
                elif todo_input == 'mydata':
                    
                    redis = redis_conn.get_redis()
                    user.initialize_redis(redis)
                    
                    user.get_user_data()
                
                else:
                    custom_logging.error(f"Invalid task: {todo_input}")
                
                time.sleep(1)
                    
    except KeyboardInterrupt as e:
        custom_logging.info('Exitting ......')
        
    except Exception as e:
        custom_logging.error(f"Oops Something went wrong! {e}")
        trace_back = e.__traceback__
        custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
        # print(e.__traceback__.tb_lineno)
        
    finally:
        if user.is_user: user.user_logout()
        conn.disconnect()