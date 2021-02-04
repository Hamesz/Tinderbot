# this deals with classifying a person
import logging
from tinderbot.control import classify_users
logger = logging.getLogger("tinderbot.Logger")
logger.setLevel(logging.DEBUG)

def main(no_users=10,):
    try:
        classify_users(no_users)
    except KeyboardInterrupt:
        pass



if __name__ == "__main__":
    main()