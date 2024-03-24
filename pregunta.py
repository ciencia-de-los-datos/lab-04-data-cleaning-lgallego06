import pandas as pd
import re

def tokenize(text):
    # Divide el texto en palabras
    return re.findall(r'\b\w+\b', text)

def stem(word):
    # Algoritmo de stemming básico
    if word.endswith("s"):
        return word[:-1]
    return word

def tokenize_and_stem(text):
    # Tokeniza el texto y luego aplica stemming a cada palabra
    tokens = tokenize(text)
    return [stem(word) for word in tokens]

def clean_data():
    df = pd.read_csv("solicitudes_credito.csv", sep=";")
    df = df.drop(columns=["Unnamed: 0"]) 
    df = df.drop_duplicates()
    df = df.dropna()
    
    # Convertir a formato de fecha "%d/%m/%Y"
    fecha_formato1 = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors='coerce')
    fecha_formato2 = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors='coerce')
    fechas_combinadas = fecha_formato1.combine_first(fecha_formato2)
    df["fecha_de_beneficio"] = fechas_combinadas
    df = df.dropna(subset=["fecha_de_beneficio"]) 
    
    # Limpiar monto_del_credito
    df['monto_del_credito'] = df['monto_del_credito'].replace('[\$,]', '', regex=True)
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'])
    
    # Strip leading and trailing whitespaces from string columns
    columns_to_strip = ["tipo_de_emprendimiento", "idea_negocio", "sexo", "línea_credito", "barrio"]
    for column in columns_to_strip:
        df[column] = df[column].str.strip()
        
    # Convertir string columns to lowercase
    columns_to_lower = ["tipo_de_emprendimiento", "idea_negocio", "sexo", "línea_credito", "barrio"]
    for column in columns_to_lower:
        df[column] = df[column].str.lower()
    
    # Tokenizar y aplicar stemming a 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito', and 'barrio' columns
    columns_to_process = ["tipo_de_emprendimiento", "idea_negocio", "línea_credito", "barrio"]
    for column in columns_to_process:
        df[column] = df[column].str.replace("-", " ").str.replace("_", " ")
        df[column] = df[column].str.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~¿"))
        df[column] = df[column].apply(tokenize_and_stem)
        df[column] = df[column].apply(lambda x: sorted(set(x))).str.join(' ')
    
    # Reemplace los nombres de los barrios con errores tipográficos
    df['barrio'] = df['barrio'].str.replace("beln", "belen")
    df['barrio'] = df['barrio'].str.replace("antonio nario", "antonio nariño")

    df = df.dropna()
    df = df.drop_duplicates()
    #df.to_excel("solicitudes_credito_limpias.xlsx", index=False)
    return df

    
#clean_data()
#print(clean_data().sexo.value_counts().to_list())
#print(clean_data().tipo_de_emprendimiento.value_counts())
print(clean_data().idea_negocio.value_counts().to_list() == [
        1844,
        1671,
        983,
        955,
        584,
        584,
        273,
        216,
        164,
        160,
        159,
        151,
        142,
        140,
        134,
        127,
        106,
        102,
        93,
        91,
        90,
        85,
        79,
        74,
        68,
        58,
        57,
        55,
        54,
        45,
        42,
        40,
        40,
        40,
        39,
        37,
        36,
        34,
        33,
        32,
        32,
        30,
        29,
        28,
        26,
        23,
        23,
        22,
        22,
        21,
        20,
        19,
        19,
        18,
        14,
        12,
        12,
        11,
        10,
        9,
        9,
        9,
        8,
        7,
        7,
        7,
        6,
        6,
        6,
        5,
        5,
        5,
        4,
        3,
        2,
    ])