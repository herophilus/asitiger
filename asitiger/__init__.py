import logging

# Do not process log messages by default
# Leave it up to the app developer to consume log messages if desired
logging.getLogger(__name__).addHandler(logging.NullHandler())
