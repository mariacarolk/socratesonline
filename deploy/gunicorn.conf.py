# CONFIGURAÇÃO GUNICORN - SOCRATES ONLINE
# Arquivo: /home/socrates/socrates_online/deploy/gunicorn.conf.py

import multiprocessing
import os

# Server socket
bind = "127.0.0.1:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Process naming
proc_name = "socrates_online"

# User and group
user = "socrates"
group = "socrates"

# Server mechanics
daemon = False
pidfile = "/home/socrates/socrates_online/logs/gunicorn.pid"
tmp_upload_dir = None

# Logging
errorlog = "/home/socrates/socrates_online/logs/gunicorn_error.log"
accesslog = "/home/socrates/socrates_online/logs/gunicorn_access.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# SSL (if needed for direct HTTPS)
# keyfile = "/path/to/ssl.key"
# certfile = "/path/to/ssl.crt"

# Environment
raw_env = [
    'FLASK_ENV=production',
    'FLASK_APP=app.py',
]

# Application
pythonpath = '/home/socrates/socrates_online'
chdir = '/home/socrates/socrates_online'

# Performance
preload_app = True
sendfile = True

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Worker behavior
worker_tmp_dir = "/dev/shm"

# Hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting Socrates Online server...")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading Socrates Online server...")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Socrates Online server is ready. Listening on: %s", server.address)

def worker_int(worker):
    """Called just after a worker has been killed by a signal."""
    worker.log.info("Worker %s killed", worker.pid)

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info("Worker %s forked", worker.pid)

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker %s spawned", worker.pid)

def post_worker_init(worker):
    """Called just after a worker has initialized the application."""
    worker.log.info("Worker %s initialized", worker.pid)

def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    worker.log.info("Worker %s aborted", worker.pid) 