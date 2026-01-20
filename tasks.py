import time
from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def long_running_job(duration: int):
    print(f"⏳ Starting job... sleeping for {duration} seconds.")
    time.sleep(duration)
    print("✅ Job complete!")
    return f"Processed for {duration} seconds."