import random
import string


class Config(object):
    """
    Configuration Class
    """
    SECRET_KEY = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32)),
    DEBUG = True
