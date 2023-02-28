from celery import shared_task

import db_api


@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='fund:increase_funds')
def input_cash_task(self, user_id: int, cash: int):
    user = db_api.input_cash(user_id, cash)
    return user


@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='fund:increase_funds')
def output_cash_task(self, user_id: int, cash: int):
    user = db_api.output_cash(user_id, cash)
    return user
