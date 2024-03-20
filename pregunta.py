"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd


def clean_data():

    df = pd.read_csv("solicitudes_credito.csv", sep=";")

    #
    # Inserte su código aquí
    #
    # Eliminar filas duplicadas
    df = df.drop_duplicates()

    # Tratar los datos faltantes
    # Por ejemplo, si quieres eliminar las filas con datos faltantes
    df = df.dropna()
    print(df)

    return df
clean_data()