import time
from controller.user.User import User
from logs.custom_logging import custom_logging
from connection.connections import db_connection
from helper.email_verification import email_verification 

if __name__ == "__main__":

    try:  
        user = User()

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
                
                if username and password and email:
                    if email_verification(email):
                        user.user_signup(username, email, password)
                    else: 
                        custom_logging.error("Invalid email")
                else:
                    custom_logging.error("Invalid input. Try again.")
                    
            elif todo_input == 'mydata':
                user.get_user_data()
                
            else:
                custom_logging.error(f"Invalid task: {todo_input}")
            
            time.sleep(1)
                    
    except KeyboardInterrupt as e:
        custom_logging.info('Exitting ......')
        
    except Exception as e:
        custom_logging.error(f"Oops Something went wrong! {e}", exc_info=True)
        
    finally:
        if user.is_user : user.user_logout()
        db_connection.disconnect()
        
        