from celery.result import AsyncResult
from IL_dtq_celery.tests.test_proj.tasks import add

async_result: AsyncResult = add.delay(2, 2)
result = async_result.get()
print( result )