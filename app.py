import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from tkinter import *
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')
from titanic import titanic
from tpm import tpm
from finanzas import presupuesto_finanzas
from proyectos import proyectos_estrategicos
from datetime import datetime

# Configuración principal de la pagína
st.set_page_config(
    page_title="TeleGPT-PandasAI",
    page_icon="🧊",
    layout="wide",)

# Utilizando la llave de OpneAI para comenzar a consultar la data
OPENAI_API_KEY = "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"
llm = OpenAI(api_token=OPENAI_API_KEY)
pandas_ai = PandasAI(llm, save_charts=True,save_charts_path='..')


# Header principal de la aplicación.
st.title('PREGUNTALE A TUS DATOS 🤖🧠')

#st.image('ai.png')

# Botón de descarga
def download_csv(dataframe):
    CSV = dataframe.to_csv(index=False)
    B64 = base64.b64encode(CSV.encode()).decode()
    href = f'<a href="data:file/csv;base64,{B64}" download="dataframe.csv">Descargar CSV</a>'
    return href



# Using object notation
add_selectbox = st.sidebar.selectbox(
    "Datos a Manipular",
    ("Archivo Local", "AWS-S3  | Titanic",
     "AWS-S3 | Transacciones Financieras",
     "SQL Server | TPM",
     "Oracle | Estatus Proyectos")
)



# Respuestas de Datos 
def text_gtp():
    # Widget de Añadir archivo.
    uploaded_file = st.file_uploader("Escoge tu Archivo Excel (.xslx)  o  CSV (.csv)", accept_multiple_files=False)
    #user_promt = st.text_input(label='Pidele algo a ChatGPT que haga por ti')
    current_hour = datetime.now()

    # Variable de Control para que no se siga ejecutando todo el programa hasta que se suba algun archivo
    control = False

    if uploaded_file is not None:
        try:
            uploaded_dataframe = pd.read_excel(uploaded_file, engine='openpyxl')
            control = True
        except UnicodeDecodeError:
            st.write('Archivo con formato incorrecto')
        except OSError:
            pass
    
    elif uploaded_file is not None:
        try:
            uploaded_file = pd.read_csv(uploaded_file, sep=';')
        except UnicodeDecodeError:
            st.write('Archivo con formato incorrecto.')

    else:
        st.warning('Inserte su archivo dando click al botón "Browse files" (Excel, CSV, TXT)')

    # Variable de Contro para que no se ejecute hasta que se colo
    if control == True:
        st.write(uploaded_dataframe)
        user_promt = st.text_area(label='Hazle tus preguntas a estos datos y la IA te contestara')

        if st.button("Generar"):
           if user_promt:
               with st.spinner("Generando respuesta:"):
                    prompt_result = pandas_ai.run(data_frame=uploaded_dataframe, prompt=f'{user_promt}')
                    
                        
                    # Escribir el resultado de la búsqueda en lenguaje natural.

                    st.write(prompt_result)
                    st.write('Última Búsqueda: ',current_hour)
           else:
               st.warning("Por favor, ingrese un prompt.")


# Correr el
if __name__ == '__main__':
    # Controlar la venta
    if add_selectbox == 'Archivo Local': 
        text_gtp()

    elif add_selectbox == 'AWS-S3  | Titanic':
        titanic()
    elif add_selectbox == 'SQL Server | TPM':
        tpm()
    elif add_selectbox == 'AWS-S3 | Transacciones Financieras':
        presupuesto_finanzas()
    else:
        proyectos_estrategicos()
