import pandas as pd
import psycopg2
import streamlit as st



# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


conn = init_connection()


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)

        rows_and_headers_object = {'rows': cur.fetchall()}

        # Extract the column names
        col_names = []
        for elt in cur.description:
            col_names.append(elt[0])
        rows_and_headers_object['headers'] = col_names

        return rows_and_headers_object


def load_tables(table_name_array):
    df_array = []
    for table_name in table_name_array:
        result = run_query(f"""SELECT * FROM {table_name};""")

        df = pd.DataFrame(result['rows'], columns=result['headers'])
        print('result object type: %s, object: %s, converted to dataframe: %s', type(result), result, df)

        df_array.append(df)

    return df_array
