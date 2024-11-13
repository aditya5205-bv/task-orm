import re
from model.user.User import User
from logs.custom_logging import custom_logging

class TaskController:
    
    def __init__(self, user: User):
        self._user = user
        
    def login(self, username, password):
        self._user.user_login(username, password)
        
    def logout(self):
        self._user.user_logout()
    
    def signup(self, username, email, password):
        
        email_pattern = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)"
                                r"*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]"
                                r"*[a-z0-9])?")
        email_verification = re.match(email_pattern, email)
                    
        if email_verification:
            self._user.user_signup(username, email, password)
            
        else: 
            custom_logging.error("Invalid email")
            
    def get_data(self):
        self._user.get_user_data()