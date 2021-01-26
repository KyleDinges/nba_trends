FROM puckel/docker-airflow:1.10.9

COPY airflow/dags/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

COPY r.txt /r.txt
RUN pip install -r /r.txt