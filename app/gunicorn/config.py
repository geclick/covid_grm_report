import multiprocessing

bind = "0.0.0.0:8443"
workers = multiprocessing.cpu_count() * 2 + 1
# Access log - records incoming HTTP requests
accesslog = "/app/gunicorn/log/access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/app/gunicorn/log/error.log"
# Whether to send Django output to the error log
capture_output = True
# How verbose the Gunicorn error logs should be
loglevel = "info"
timeout = 300
