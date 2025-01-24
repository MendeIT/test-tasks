from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from database.db import async_engine


jobstores = {
    "default": SQLAlchemyJobStore(engine=async_engine)
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ThreadPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3,
    'name': 'Сбор данных в БД с периодичностью раз в 30 минут'
}

scheduler = AsyncIOScheduler(
    # jobstores=jobstores,
    # executors=executors,
    # job_defaults=job_defaults
)
