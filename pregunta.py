"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""

import pandas as pd
import nltk

def clean_text(text):
    text = text.strip().lower().replace("-", " ").replace("_", " ")
    text = text.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~¿"))
    return text

def apply_stemming(text):
    stemmer = nltk.PorterStemmer()
    words = [stemmer.stem(word) for word in text.split()]
    return ' '.join(sorted(set(words)))

def clean_data():

    df = pd.read_csv("solicitudes_credito.csv", sep=";")
    df = df.dropna()
    df = df.drop(columns=["Unnamed: 0"]) 
    df = df.drop_duplicates()
    df["sexo"] = df["sexo"].str.strip()
    df["sexo"] = df["sexo"].str.lower()
    # Convertir a formato de fecha "%d/%m/%Y"
    fecha_formato1 = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors='coerce')
    # Convertir a formato de fecha "%Y/%m/%d"
    fecha_formato2 = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors='coerce')
    # Combinar resultados
    fechas_combinadas = fecha_formato1.combine_first(fecha_formato2)
    # Reemplazar la columna "fecha_de_beneficio" con las fechas normalizadas
    df["fecha_de_beneficio"] = fechas_combinadas
    # Eliminar filas con fechas nulas
    # df = df.dropna(subset=["fecha_de_beneficio"])
    df['monto_del_credito'] = df['monto_del_credito'].replace('[\$,]', '', regex=True)
    # Convertir la columna "monto_del_credito" a valores numéricos
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'])
    # Convertir la columna al tipo de datos str antes de aplicar la limpieza
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].astype(str)
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].apply(clean_text)
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].apply(apply_stemming)

    df["idea_negocio"] = df["idea_negocio"].astype(str)
    df["idea_negocio"] = df["idea_negocio"].apply(clean_text)
    df["idea_negocio"] = df["idea_negocio"].apply(apply_stemming)

    df["línea_credito"] = df["línea_credito"].astype(str)
    df["línea_credito"] = df["línea_credito"].apply(clean_text)
    df["línea_credito"] = df["línea_credito"].apply(apply_stemming)

    df["barrio"] = df["barrio"].astype(str)
    df["barrio"] = df["barrio"].apply(clean_text)
    df["barrio"] = df["barrio"].apply(apply_stemming)
    
    df = df.dropna()
    df = df.drop_duplicates()
    print(df)
    return df
#clean_data()
#print(clean_data().tipo_de_emprendimiento.value_counts())