"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""

import pandas as pd
import nltk


def clean_data():

    df = pd.read_csv("solicitudes_credito.csv", sep=";")
    df = df.dropna()
    df = df.drop(columns=["Unnamed: 0"]) 
    df = df.drop_duplicates()
    # Convertir a formato de fecha "%d/%m/%Y"
    fecha_formato1 = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors='coerce')

    # Convertir a formato de fecha "%Y/%m/%d"
    fecha_formato2 = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors='coerce')

    # Combinar resultados
    fechas_combinadas = fecha_formato1.combine_first(fecha_formato2)

    # Reemplazar la columna "fecha_de_beneficio" con las fechas normalizadas
    df["fecha_de_beneficio"] = fechas_combinadas

    # Eliminar filas con fechas nulas
    df = df.dropna(subset=["fecha_de_beneficio"]) 
    
    df['monto_del_credito'] = df['monto_del_credito'].replace('[\$,]', '', regex=True)

    # Convertir la columna "monto_del_credito" a valores numéricos
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'])
    
    # Strip leading and trailing whitespaces from string columns
    columns_to_strip = ["tipo_de_emprendimiento", "idea_negocio", "sexo", "línea_credito", "barrio"]
    for column in columns_to_strip:
        df[column] = df[column].str.strip()
        
    # Convert string columns to lowercase
    columns_to_lower = ["tipo_de_emprendimiento", "idea_negocio", "sexo", "línea_credito", "barrio"]
    for column in columns_to_lower:
        df[column] = df[column].str.lower()
    
    # Tokenize and stem 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito', and 'barrio' columns
    columns_to_process = ["tipo_de_emprendimiento", "idea_negocio", "línea_credito", "barrio"]
    for column in columns_to_process:
        # Replace dashes and underscores with spaces
        df[column] = df[column].str.replace("-", " ").str.replace("_", " ")
        df[column] = df[column].str.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~¿"))
        # Tokenize
        df[column] = df[column].str.split()
        # Stemming
        stemmer = nltk.PorterStemmer()
        df[column] = df[column].apply(lambda x: [stemmer.stem(word) for word in x])
        # Remove duplicates, sort, and join
        df[column] = df[column].apply(lambda x: sorted(set(x))).str.join(' ')
    df['barrio'] = df['barrio'].str.replace("beln", "belen")
    df['barrio'] = df['barrio'].str.replace("antonio nario", "antonio nariño")
    df = df.dropna()
    df = df.drop_duplicates()
    #print(df)
    return df
#clean_data()
#print(clean_data().sexo.value_counts().to_list())
#print(clean_data().tipo_de_emprendimiento.value_counts())
#print(clean_data().idea_negocio.value_counts())
#pd.set_option('display.max_rows', None)
#print(clean_data().barrio.value_counts().to_list())
#print(clean_data().estrato.value_counts())

