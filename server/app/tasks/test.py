from app.config import celery_app


@celery_app.task
def test_task_worker():
    print("test task work")
