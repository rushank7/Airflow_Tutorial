try: 
    from datetime import timedelta
    from datetime import datetime
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    print('all modules are printed')
except Exception as e:
    print('error {}'.format(e))

def first_function_execute(**context):
    print('first_function_execute')
    context['ti'].xcom_push(key='mykey',value="first_function_execute says hello") ## get the key value and push the data/function

## 2nd function

def second_function_execute(**context):
    instance = context.get("ti").xcom_pull(key="mykey")  ## get the key value and pull the data/function
    print("i am in second_fucntion_execute got value :{} from function 1".format(instance))

with DAG(
    dag_id='first_dag',
    schedule_interval='@daily',
    default_args={'owner':'airflow',
    'retries':1,
    'retry_delay':timedelta(minutes=5),
    'start_date':datetime(2023,1,1)},
    catchup=False
) as f:
    
    first_function_execute = PythonOperator(
        task_id = "first_function_execute",
        python_callable = first_function_execute,
        provide_context = True,
        op_kwargs={"name":"rushankpatil"})

    second_function_execute = PythonOperator(
        task_id = "second_function_execute",
        python_callable = second_function_execute,
        provide_context = True)

first_function_execute>>second_function_execute

## docker container ls - shows all running container
##  docker image prune - deletes all unnnecessary images