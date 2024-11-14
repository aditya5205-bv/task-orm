import re

def email_verification(email: str):
    email_pattern = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)"
                            r"*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]"
                            r"*[a-z0-9])?")
    
    email_verification = re.match(email_pattern, email)
    
    if email_verification: return True
    else: return False