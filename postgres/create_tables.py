import psycopg2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--addr", type=str, help="Address for deploymnets db!", required=True)

args = parser.parse_args()

dbname = 'postgres'
user = 'postgres'
password = 'super_dooper_secret'
host = args.addr

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

cur = conn.cursor()

create_table_models = """
CREATE TABLE models (
    model_id VARCHAR,
    user_id VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    description VARCHAR,
    score NUMERIC,
    model_name VARCHAR,
    score_count INTEGER,
    dataset_user VARCHAR,
    notebook_type VARCHAR,
    target_column VARCHAR
);
"""

create_table_notebooks = """
CREATE TABLE notebooks (
    user_id VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    notebook_id VARCHAR,
    last_accessed TIMESTAMP WITHOUT TIME ZONE,
    description VARCHAR,
    port VARCHAR,
    notebook_type VARCHAR,
    dataset_name VARCHAR,
    dataset_user VARCHAR
);
"""

cur.execute(create_table_models)
cur.execute(create_table_notebooks)

conn.commit()

cur.close()
conn.close()
