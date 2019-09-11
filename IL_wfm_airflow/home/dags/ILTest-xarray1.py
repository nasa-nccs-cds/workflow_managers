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
    dag_id='ILTest-xarray1',
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
    uri = "https://dataserver.nccs.nasa.gov//thredds/dodsC/bypass/CREATE-IP/reanalysis/MERRA2/mon/atmos/tas.ncml"
    dset: xa.Dataset = xa.open_dataset( uri )
#    return codecs.encode(pickle.dumps(dset), "base64").decode()
    return dset

op_get_dataset = PythonOperator(
    task_id='get_dataset',
    provide_context=True,
    python_callable=get_dataset,
    dag=dag,
)

def get_variable(ds, **kwargs) -> xa.Variable:
    dataset = kwargs['task_instance'].xcom_pull(task_ids='get_dataset')
    variable: xa.Variable =  dataset.variables['tas']
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



