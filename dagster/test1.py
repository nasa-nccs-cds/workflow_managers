from dagster import lambda_solid, pipeline, execute_pipeline
from dagster.core.execution.results import PipelineExecutionResult, SolidExecutionResult
import xarray as xa
import codecs, pickle, time


@lambda_solid
def get_dataset() -> str:
    uri = "https://dataserver.nccs.nasa.gov//thredds/dodsC/bypass/CREATE-IP/reanalysis/MERRA2/mon/atmos/tas.ncml"
    dset: xa.Dataset = xa.open_dataset( uri )
    return codecs.encode(pickle.dumps(dset), "base64").decode()
#    return pickle.dumps(dset)


@lambda_solid
def get_variable( dset: str ) -> str:
#    dataset = pickle.loads(dset)
    dataset = pickle.loads(codecs.decode( dset.encode(), "base64"))
    variable =  dataset.variables['tas']
    varData = variable[:,:,:]
    return codecs.encode(pickle.dumps(varData), "base64").decode()


@pipeline
def actual_dag_pipeline():
    get_variable( get_dataset() )


def run_dagster_pipeline():
    result: PipelineExecutionResult  = execute_pipeline(actual_dag_pipeline)
    exec_result: SolidExecutionResult = result.result_for_solid("get_variable")
    var_str = exec_result.output_values['result']
    return pickle.loads(codecs.decode( var_str.encode(), "base64") )

def run_bare_pipeline() -> xa.Variable:
    uri = "https://dataserver.nccs.nasa.gov//thredds/dodsC/bypass/CREATE-IP/reanalysis/MERRA2/mon/atmos/tas.ncml"
    dset: xa.Dataset = xa.open_dataset( uri )
    variable: xa.Variable = dset.variables['tas']
    return variable[:,:,:]

if __name__ == '__main__':
    t0 = time.time()
    variable = run_dagster_pipeline()
#    variable = run_bare_pipeline()
    print( "RESULT SHAPE = " + str(variable.shape)  + ", Exec time = " + str( time.time() - t0 ) + " seconds" )