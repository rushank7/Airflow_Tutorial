# Airflow_Tutorial
learnign Airflow with docker


Airflow
Apache Airflow is a platform to programmatically schedule and mointor workflows as DAGs. With Airflow, we have command line utilities as well as a user interface to visualise pipelines, monitor progress and troubleshoot issues.

Here's the general architecture:



source
Airflow
Apache Airflow is a platform to programmatically schedule and mointor workflows as DAGs. With Airflow, we have command line utilities as well as a user interface to visualise pipelines, monitor progress and troubleshoot issues.

Here's the general architecture:



source

Web Server - GUI to inspect, trigger and debug behaviour of DAGS. Available at http://localhost:8080.

The home page of the web server shows us a list of DAGs. The DAGs properties can be seen here (where the source file resides, tags, descriptions, and so on). The DAGs can also easily be paused here, which will then ignore any schedules you may have set. You can see the names of the DAGs, the schedule that they run on (in CRON format), the owner of the DAG, recent tasks, a timestamp of the last run of the DAG, summary of previous DAGs run, and so on.

You can also view the DAG as a graph, after going to the DAG detail page. We can also view the code behind the DAG here as well.

Scheduler - Responsible for scheduling jobs.

This constantly monitors DAGs and taks and running any that are scheduled to run and have had their dependencies met.

Worker - Executes the tasks given by scheduler.

MetaData Database - Backend to Airflow. Used by scheduler and executor and webserver to store data.

This contains all the metadata related to the execution history of each task and DAG as well as airflow configuration. I believe the default in SQLite, but can easily be configured to PostgreSQL or some other database system. The database is created when we initialise using airflow-init. Information in this database includes task history.

redis - Forwards messages from scheduler to worker

flower- Flower app for monitoring the environment. Available at http://localhost:5555.

airflow-inti - Initialises service

If we're running Airflow in Docker, we use something called CeleryExecutor

What is an Executor and what is CeleryExecutor?
Once we define a DAG, the following needs to happen in order for a single set of tasks within that DAG to execute and complete from start to finish:

The Metadata Database keeps a record of all tasks within the DAG, along with their status (e.g. failed, running, scheduled).

The Scheduler reads from the Metadata Database to check the status of each tasks and decide what needs done.

The Executor works with the Scheduler to determine what resources will complete those tasks as they're queued. In other words, it runs tasks taht the Scheduler determines are ready to run. The SequentialExecutor is the default. This can only run one task at a time, and is not meant for production. It's really just for testing simple DAGs. However, it's the only one that is currently compatible with SQLite. We're using PostgreSQL, and we want to run more complex DAGs, wo we're going with CeleryExecutor which is built for horizontal scaling, or distributed computing. This works with pools of independent workders across which it can delegate tasks.

Additional Terminology
Operators - Each task implements an operator. These are what actually execute scripts, commands, and so on. These include PythonOperator, BashOperator and PostgresOperator. These are assigned to each task/node in a DAG.
Running Airflow with Docker
There's a few steps required to get Airflow working with Docker:

Install Docker Community Edition on your local machine.
Configure Docker instance to use 4GB of memory.
Install Dockder Compose.
We then fetch docker-compose.yaml which uses the latest airflow image. To do so, run:

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.3/docker-compose.yaml'

Within this file, there are several definitions:

airflow-scheduler - This monitors all tasks & DAGs.
airflow-webserver - Available at http://localhost:8080
airflow-worker - This executes the tasks given by scheduler
airflow-init - Initialises services
flower - Monitors oru environment
postgres - The database
redis - broker and forwards messages from scheduler to worker
With these services, we are able to run Airflow with CeleryExecutor.

Some of these services are mounted, meaning their contents are synced between our local machine and the container:

/dags - DAG files go here
/logs - Logs from task execution & scheduler
/plugins - Custom plugins go here
Some workflow components:

DAG - Specifies the dependencies between a set of tasks with explicit execution order
Tasks - A definied unit of work. These define what to do (e.g. running analysis)
DAG Run - Individual execution of a DAG
Task Instance - Individual run of a single Task. Each task has a state (failed, success, etc). Ideally, they run from:
none > scheduled > queued > running > success
