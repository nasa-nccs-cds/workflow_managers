from celery.result import AsyncResult
from IL_dtq_celery.tests.test_proj.tasks import add, mul, input, xsum
from celery import group, chain, chord

c1 = ( input.s(1) | add.s(4) | mul.s(8) )
c2 = ( input.s(2) | add.s(1) | mul.s(3) )
c3 = ( group( c1, c2 )| xsum.s() )

async_result: AsyncResult = c3.delay()
result = async_result.get()
print( result )