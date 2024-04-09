import os

bind = "0.0.0.0:" + str(os.environ.get('PORT', 5500))
workers = 1    # concurrency (1 request for replication available at the same time)
timeout = 3600 * 200    # 20h (up to 1920px (total dimension) of image is available)
