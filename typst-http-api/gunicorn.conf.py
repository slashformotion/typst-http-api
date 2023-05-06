import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
loglevel = "debug"
# valid levels are
# - 'debug'
# - 'info'
# - 'warning'
# - 'error'
# - 'critical'

bind = "0.0.0.0:8000"
