
### Airflow Installation
```
$ python3 -m venv airflow
$ source airflow/bin/activate
$ pip install "apache-airflow[mysql]"
$ pip install pydap
DOWNLOAD: https://files.pythonhosted.org/packages/64/2e/abc0bce095ab5a3b8374f052ace2509a031fd7633b23917e557487067225/netCDF4-1.5.2.tar.gz
$ pip install ~/Downloads/netCDF4-1.5.2.tar.gz 
```

### Setup Environment
```
export AIRFLOW_HOME=<install_dir>/workflow_managers/airflow/home
export AIRFLOW_GPL_UNIDECODE=true
```

### MySql Setup
```
## START SHELL:
> mysql -u <username> -p

## SET UP DATABASE AND USER:
mysql> CREATE USER airflow@localhost IDENTIFIED BY ‘workflow’;
mysql> GRANT ALL ON *.* TO 'airflow'@'localhost' WITH GRANT OPTION;
mysql> CREATE DATABASE airflow;
```

### Airflow Startup
```
> airflow initdb
> airflow webserver -p 8080
> airflow scheduler