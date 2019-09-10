from __future__ import print_function

import xarray as xa
import codecs, pickle, time
from builtins import range
from pprint import pprint
import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='ILTest-xarray-parallel',
    default_args=args,
    schedule_interval=None,
)

def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'

op_print_context = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)

def get_dataset(ds, **kwargs) -> xa.Dataset:
    pathList = "/Users/tpmaxwel/Dropbox/Tom/Data/MERRA/DAILY/2005/JAN/*.nc"
    dset: xa.Dataset = xa.open_mfdataset( pathList, data_vars=["t"], parallel=True )
    return dset

op_get_dataset = PythonOperator(
    task_id='get_dataset',
    provide_context=True,
    python_callable=get_dataset,
    dag=dag,
)

def get_variable(ds, **kwargs) -> xa.Variable:
    dataset = kwargs['task_instance'].xcom_pull(task_ids='get_dataset')
    variable: xa.Variable =  dataset.variables["t"]
    varData = variable[:,:,:]
    print( f"VARIABLE SHAPE= {variable.shape}")
    return varData

op_get_variable = PythonOperator(
    task_id='get_variable',
    provide_context=True,
    python_callable=get_variable,
    dag=dag,
)

op_print_context >> op_get_dataset >> op_get_variable




