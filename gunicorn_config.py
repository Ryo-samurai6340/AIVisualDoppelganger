import os
bind = "0.0.0.0:" + str(os.environ.get('PORT', 5500))
workers = 1
timeout = 10800
