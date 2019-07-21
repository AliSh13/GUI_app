from secrets import choice
import string
def create_password_(len_pass):
    text = ''.join([choice(string.ascii_uppercase + string.digits +
        string.ascii_lowercase) for _ in range(len_pass)])
    return text



def creat_pass_all_char(len_pass):
    text = ''.join([choice(string.ascii_uppercase + string.digits +
        string.ascii_lowercase + '!@#$%^&*(?></)') for _ in range(len_pass)])
    return text
