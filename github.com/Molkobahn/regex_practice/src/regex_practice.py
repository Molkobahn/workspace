import re


    
def extract_email(text):
    email = re.findall(r"([a-zA-Z0-9\.]+@[a-zA-Z]+\.(com|edu|org))", text)
    return [match[0] for match in email]
    

