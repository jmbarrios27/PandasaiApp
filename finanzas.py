import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from tkinter import *
import base64
import matplotlib.pyplot as plt
import matplotlib
import io
from io import StringIO
import boto3
import base64
matplotlib.use('tkagg')


# Utilizando la llave de OpneAI para comenzar a consultar la data
OPENAI_API_KEY = ""
llm = OpenAI(api_token=OPENAI_API_KEY)
pandas_ai = PandasAI(llm,save_charts=True,save_charts_path='..')


# Descargar DataFrame
def download_csv(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dataframe.csv">Descargar Archivo en formato .CSV</a>'
    return href


def presupuesto_finanzas():
    aws_access_key_id = ''
    aws_secret_access_key = ''
    aws_region = 'us-east-1'

    s3_file_path = 'Streamlit/presupuesto_finanzas.csv'
    s3_bucket = 'tlrd-pages'

      # Create a session with boto3
    session = boto3.Session(
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      region_name=aws_region
    )

    s3 = session.client('s3')
  
    # Read the CSV file from S3 into a pandas dataframe
    s3_object = s3.get_object(Bucket=s3_bucket, Key=s3_file_path)
    s3_data = s3_object['Body'].read().decode('utf-8')
    titanic = pd.read_csv(StringIO(s3_data))

    st.dataframe(titanic)
    st.subheader('Presupuesto de Finanzas')
    st.warning(body='Cuidado esta pagina esta reservada para la conexión a S3 de Streamlit')
    user_promt = st.text_area(label='Hazle tus preguntas a estos datos y la IA te contestara')
    control = False
    if st.button("Generar"):
        if user_promt:
            with st.spinner("Generando respuesta:"):
                    prompt_result = pandas_ai.run(data_frame=titanic, prompt=f'{user_promt}')
                    st.write(prompt_result)
                    control = True
        else:
            st.warning("Por favor, ingrese un prompt.")
    
    # Flujo de Control para habilitar el botón de Descarga del DataFrame creado, sólo si el resultado de 
    if control == True:
        type_result = str(type(prompt_result))
        print('tipo de resultado',type_result)
        if type_result == "<class 'pandas.core.frame.DataFrame'>":
            print('Hola mundo')
            st.markdown(download_csv(dataframe=prompt_result), unsafe_allow_html=True)
       

    
    
