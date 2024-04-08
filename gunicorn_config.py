import os

bind = "0.0.0.0:" + str(os.environ.get('PORT', 5500))
workers = 1    # scalability (only 1 request is available as of now)
timeout = 3600 * 20    # 20h (up to 902,500px (total dimension) or 1920px (sum dimension) of image is available)
