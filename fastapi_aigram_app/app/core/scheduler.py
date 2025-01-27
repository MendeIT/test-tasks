from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from database.db import sync_engine


jobstores = {
    "default": SQLAlchemyJobStore(engine=sync_engine)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3,
    'name': 'Сбор данных в БД с периодичностью раз в 30 минут'
}

scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    job_defaults=job_defaults
)
