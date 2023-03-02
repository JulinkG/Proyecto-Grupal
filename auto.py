import pandas as pd
import numpy as np
from sqlite3 import connect
import matplotlib.pyplot as plt

paises_migraciones_url='https://raw.githubusercontent.com/elgualas/datallake_PG/main/migration%20(1).csv'       
paises_poblacion_url='https://raw.githubusercontent.com/elgualas/datallake_PG/main/population-and-demography.csv'

paises_migraciones= pd.read_csv(paises_migraciones_url)
paises_poblacion = pd.read_csv(paises_poblacion_url)

conn = connect(':memory:') 
paises_migraciones.to_sql('pam',conn,index=False)
paises_poblacion.to_sql('pap',conn,index=False)

paises_migraciones_america=pd.read_sql('SELECT Year,Country,Emigrants,`International migrants`, `Net migration`, `Net migration rate` FROM pam WHERE Country IN ("Argentina","Belice","Bolivia", "Brasil","Canada","Colombia", "Costa Rica", "Cuba", "Chile", "Ecuador", "El Salvador", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru","Puerto Rico", "Republica Dominicana","United States","Uruguay","Venezuela","Antigua y Barbuda","Bahamas","Barbados","Dominica","Granada","Guyana","Jamaica","República Dominicana","San Cristobal y Nieves","San Vicente y las Granadinas","Santa Lucia")',conn)
paises_poblacion_america=pd.read_sql('SELECT `Country name`, Year, Population FROM pap WHERE `Country name` IN ("Argentina","Bolivia","Belice", "Brasil","Canada","Colombia", "Costa Rica", "Cuba", "Chile", "Ecuador", "El Salvador", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru","Puerto Rico", "Republica Dominicana","United States","Uruguay","Venezuela","Antigua y Barbuda","Bahamas","Barbados","Dominica","Granada","Guyana","Jamaica","República Dominicana","San Cristobal y Nieves","San Vicente y las Granadinas","Santa Lucia")',conn)

paises_migraciones_america.to_sql('a',conn,index=False)
paises_poblacion_america.to_sql('c',conn,index=False)

tabla=pd.read_sql('SELECT a.Year,a.Country,a.Emigrants,a.`International migrants`,a.`Net migration`,a.`Net migration rate`,c.Population FROM a a JOIN c c ON(a.Year=c.Year AND a.`Country`=c.`Country name` )',conn)

tabla.dropna(inplace=True)
tabla.reset_index(drop=True, inplace=True)

tabla['relative migration']=0

for i in range(len(tabla)):
    tabla['relative migration'][i]=tabla['Emigrants'][i]/tabla['Population'][i]

print(tabla)