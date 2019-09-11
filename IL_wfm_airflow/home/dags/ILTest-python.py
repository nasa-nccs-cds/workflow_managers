from __future__ import print_function

import xarray as xa
import codecs, pickle, time
from builtins import range
from pprint import pprint
import airflow, traceback
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils import timezone
from argparse import Namespace

args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='ILTest-python',
    default_args=args,
    schedule_interval=None,
)

def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    traceback.print_stack()
    return 'Whatever you return gets printed in the logs'

op_print_context = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)

def get_dataset(ds, **kwargs) -> str:
    return "get_dataset: result"

op_get_dataset = PythonOperator(
    task_id='get_dataset',
    provide_context=True,
    python_callable=get_dataset,
    dag=dag,
)

def get_variable(ds, **kwargs) -> str:
    return "get_dataset: result"

op_get_variable = PythonOperator(
    task_id='get_variable',
    provide_context=True,
    python_callable=get_variable,
    dag=dag,
)

op_print_context >> op_get_dataset >> op_get_variable


if __name__ == '__main__':
    from airflow.bin.cli import run, get_dag
    from unittest.mock import patch

    run_args = dict(
        task_id='get_variable',
        dag_id='ILTest-python',
        interactive=False,
        cfg_path = "",
        execution_date=timezone.parse('2018-04-27T08:39:51.298439+00:00')
    )


    run( Namespace(**run_args) )




