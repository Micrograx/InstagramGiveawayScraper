# Defining easy to break constants for future fixing
from selenium import webdriver

# ---------------   COMMENT GATHERING ---------------

# Button for loading more comments XPath:
BTN_MORE_COMMENTS = '//*[@id="react-root"]/section/main/div/ul/li/div/button'

# Each comment class name:
CLASS_COMMENT = "C4VMK"

# Each comment username class name:
CLASS_COMMENT_USERNAME = "_6lAjh"


# ---------------   LIKES GATHERING   ---------------

# Link to likes XPath:
BTN_ALL_LIKES = '//*[@id="react-root"]/section/main/div/div/article/div[3]/section[2]/div/div/a'

# Each Like XPath to count them:
XPATH_SINLGE_COMMENT = '//*[@id="react-root"]/section/main/div[1]/div'

# ---------------   EXCEPTION CODES   ---------------

EXCEPTION_NO_ELEMENT = webdriver.remote.errorhandler.NoSuchElementException