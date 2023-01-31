try: 
    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator    from datetime import datetime
    print('all modules are printed')
except Exception as e:
    print('error {}'.format(e))

def first_function_execute():
    print('hellow world')
    return 'hello world'

with DAG(
    dag_id='first_Dag',
    schedule_interval='@daily',
    default_args={'owner':'airflow',
    'retries':1,
    'retry_delay':timedelta(minutes=5),
    'start_Date':datetime(2023,1,1)},
    catchup=False
) as f:
    
    first_function_execute = PythonOperator(
        task_id = 'first_function_execute',
        python_callable = 'first_function_execute'
    )

