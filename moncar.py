# -*- coding: utf-8 -*-
"""MonCar.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WeLSf_ESLiU8qAnqve-d3IXcSHMh2iMe
"""

!pip install sweetviz
!pip install streamlit
!pip install streamlit_folium

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import datetime
import streamlit as st
import sweetviz as sv

from streamlit_folium import folium_static



def get_data(path):
  df = pd.read_csv(path)
  return df

def split_name(df):
  new = df["name"].str.split(" ", n=1, expand=True)
  df["car_brand_name"] = new[0]
  df["car_name"] = new[1]
  df.drop(columns=["name"], inplace=True)

  return df

def car_age(df):
  df['car_age'] = (datetime.datetime.now().year) - (df['year'])
  return df

def remove_duplicates (df):
  df = df.drop_duplicates()
  return df

def data_overview(df):
  if st.checkbox('Mostre o dataset'):
    st.write(df.head(50))

  st.sidebar.title('Projeto MonCar')
  st.sidebar.write('MonCar é uma empresa que trabalha com a compra e venda de veículos usados. '
'O Cientista de dados da empresa deverá ajudar a encontrar as melhores '
'oportunidades de negócio.')
  st.sidebar.write("Para mais informações sobre o projeto, acesse: "
"[GitHub](https://github.com/rsoliveirac/house-rocket-project)")
  return None

new_km = df[['km_driven', 'year']].groupby('year').median().reset_index()
h2 = pd.merge(df, new_km, on = 'year', how = 'inner')
h2 = h2.rename(columns={'km_driven_y': 'km_driven_median'})

for i in range(len(h2)):
  if(h2.loc[i,'year'] >= 2017) & (h2.loc[i,'km_driven_x'] <= h2.loc[i, 'km_driven_median']):
    h2.loc[i, 'state'] = 'semi_used'

  else:
    h2.loc[i, 'state'] = 'used'

h2

def metricas (df):
  st.markdown("<h1 style='text-align: center; color: black;'> Análise Descritiva</h1>", unsafe_allow_html=True)
  atri_num = df.select_dtypes(include = ['int64', 'float64'])

  pd.set_option('display.float_format', lambda x: '%.3f' % x)

  #medidas de tendencia central
  df_mean = pd.DataFrame(atri_num.apply(np.mean)).T
  df_median = pd.DataFrame(atri_num.apply(np.median)).T

  #medidas de dispersão
  df_std = pd.DataFrame(atri_num.apply(np.std)).T
  df_min = pd.DataFrame(atri_num.apply(np.min)).T
  df_max = pd.DataFrame(atri_num.apply(np.max)).T

  #concatenando
  df1 = pd.concat( [df_mean, df_median, df_std, df_min, df_max ] ).T.reset_index()

  #alterando o nome das colunas
  df1.columns = [ 'atributos','media', 'mediana', 'std', 'min', 'max']
  st.dataframe(df1, width = 1000)
  return df

my_report = sv.analyze(h2)
my_report.show_html()

# Load the data into a DataFrame
df2 = h2.copy()

#Hipoteses

def hipoteses(df):

  #H1 - Carros com até 5 anos são 40% mais caros

  # Split the data into two groups based on car age
  young_cars = df2[df2['car_age'] <= 5]
  old_cars = df2[df2['car_age'] > 5]

  # Calculate the average selling price for each group
  young_cars_price = young_cars['selling_price'].mean()
  old_cars_price = old_cars['selling_price'].mean()

  # Calculate the difference in average selling price
  price_difference = young_cars_price - old_cars_price

  # Calculate the percentage difference in average selling price
  price_difference_percentage = (price_difference / old_cars_price) * 100

  # Print the results
  print(f'A média de carros com até 5 anos é: {young_cars_price:.2f}')
  print(f'A média de carros com mais de 5 anos é: {old_cars_price:.2f}')
  print(f'A diferença de preço é: {price_difference:.2f}')
  print(f'A diferença em porcentagem é: {price_difference_percentage:.2f}')

  # Create a bar chart to visualize the results
  plt.bar(['Carros com até 5 anos', 'Carros com mais de 5 anos'], [young_cars_price, old_cars_price])
  plt.title('Comparação de preços de carros por idade')
  plt.xlabel('Idade do carro')
  plt.ylabel('Preço médio')
  plt.show()

  #H2 - O tipo de dono aumenta a kilometragem
  # Extract the unique owner types from the 'owner' column
  owner_types = df2['owner'].unique()

  # Initialize a dictionary to store the average mileage for each owner type
  mileage_by_owner_type = {}

  # Iterate through each owner type
  for owner_type in owner_types:
      # Filter the data to include only cars with the current owner type
      filtered_data = df2[df2['owner'] == owner_type]

      # Calculate the average mileage for the filtered data
      average_mileage = filtered_data['km_driven'].mean()

      # Store the average mileage for the current owner type in the dictionary
      mileage_by_owner_type[owner_type] = average_mileage

  # Sort the dictionary by average mileage in ascending order
  sorted_mileage_by_owner_type = dict(sorted(mileage_by_owner_type.items(), key=lambda item: item[1]))

  # Print the sorted average mileage for each owner type
  for owner_type, mileage in sorted_mileage_by_owner_type.items():
      print(f'Média de quilometragem para proprietários {owner_type}: {mileage:.2f}')

  # Create a bar chart to visualize the sorted average mileage
  plt.bar(sorted_mileage_by_owner_type.keys(), sorted_mileage_by_owner_type.values())
  plt.title('Comparação de quilometragem por tipo de proprietário')
  plt.xlabel('Tipo de proprietário')
  plt.ylabel('Média de quilometragem')
  plt.show()

  #H3 - O tipo de combustivel aumenta a kilometragem

  # Calculate the average mileage for each fuel type
  fuel_types = df2['fuel'].unique()
  mileage_by_fuel_type = {}
  for fuel_type in fuel_types:
      mileage_by_fuel_type[fuel_type] = df2[df2['fuel'] == fuel_type]['km_driven'].mean()

  # Sort the dictionary by average mileage in ascending order
  sorted_mileage_by_fuel_type = dict(sorted(mileage_by_fuel_type.items(), key=lambda item: item[1]))

  # Print the sorted average mileage for each fuel type
  for fuel_type, mileage in sorted_mileage_by_fuel_type.items():
      print(f'Média de quilometragem para combustível {fuel_type}: {mileage:.2f}')

  # Create a bar chart to visualize the sorted average mileage
  plt.bar(sorted_mileage_by_fuel_type.keys(), sorted_mileage_by_fuel_type.values())
  plt.title('Comparação de quilometragem por tipo de combustível')
  plt.xlabel('Tipo de combustível')
  plt.ylabel('Média de quilometragem')
  plt.show()

  #H4 - Carros eletricos são 40% mais caros que os outros

  # Get the selling price data for electric cars
  electric_selling_price = df2[df2['fuel'] == 'Electric']['selling_price']

  # Get the selling price data for other cars
  petrol_selling_price = df2[df2['fuel'] == 'Petrol']['selling_price']

  # Calculate the difference in average selling price between electric cars and other cars
  price_difference = petrol_selling_price.mean() - electric_selling_price.mean()


  # Calculate the percentage difference in average selling price between electric cars and other cars
  price_difference_percentage = (price_difference / petrol_selling_price.mean()) * 100

  # Print the results
  print('A diferença de preço média entre carros gasolina e carros elétricos é:', price_difference)
  print('A diferença de preço média entre carros gasolina e carros elétricos em porcentagem é:', price_difference_percentage, '%')

  # Create a bar chart to visualize the results
  plt.bar(['Carros elétricos', 'Gasolina'], [electric_selling_price.mean(), petrol_selling_price.mean()])
  plt.title('Comparação de preços de carros por tipo de combustível')
  plt.xlabel('Tipo de combustível')
  plt.ylabel('Preço médio')
  plt.show()

  return None

def questoes_negocio (df):
  st.markdown("<h1 style='text-align: center; color: black;'> Questões de Negócio</h1>", unsafe_allow_html=True)
  st.subheader('1. Quais são os carros que a MonCar deveria comprar para revender?')

  # Define criteria for buying cars for resale

  df2['cars_to_buy'] = 'NA'

  for i in range(len(df2)):
      if (df2.loc[i,'car_age'] <= 10) & (df2.loc[i, 'selling_price'] < 473912.542):
          df2.loc[i, 'cars_to_buy'] = 'Yes'
      else:
          df2.loc[i, 'cars_to_buy'] = 'No'

  # Print information about the cars to buy
  print("**Cars to buy for resale:**")
  plt.hist(x = df2['cars_to_buy']);

  #Valor de revenda dos carros com 20% de lucro
  df3 = df2.copy()
  df3['sale'] = '0'

  for i in range(len(df2)):
      if (df3.loc[i, 'cars_to_buy'] == 'Yes'):
          df3.loc[i, 'sale'] = df3.loc[i, 'selling_price'] * 0.2 + df3.loc[i, 'selling_price']

  # Agora, 'sale' é numérica e você pode calcular o lucro corretamente
  df3['sale'] = df3['sale'].astype(int)
  df3['profit'] = df3['sale'] - df3['selling_price']

  #Agora você pode calcular o total do lucro
  total_profit = df3['sale'].sum()

  #print(df3)
  st.text("O lucro gerado neste projeto é de R$ {}".format(total_profit))
  return None

def tabela (df):
  st.markdown("<h1 style='text-align: center; color: black;'> Resumo sobre as Hipóteses </h1>", unsafe_allow_html=True)
  hipoteses = pd.DataFrame({
  '.': ['Verdadeira', 'Verdadeira', 'Verdadeira', 'Falsa']}, index=['H1', 'H2', 'H3', 'H4'])
  hipoteses = hipoteses.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
  hipoteses.set_properties(**{'text-align': 'center'}).hide_index()
  st.table(hipoteses)
  return None

if __name__ == "__main__":
  path = '/content/MonCar Cars.csv'
  df = get_data(path)
  split_name(df)
  car_age(df)
  remove_duplicates (df)
  data_overview(df)
  metricas(df)
  questoes_negocio(df)
  tabela(df)