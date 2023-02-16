from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
from sqlite3 import connect

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "C:\\Users\\gualas\\Desktop\\prueba",
})

driver = webdriver.Chrome(executable_path=r'C:\Users\gualas\Desktop\ChromeDriver\chromedriver.exe',options=chrome_options)
# Acceder a la página nro1
driver.get("https://ourworldindata.org/world-population-growth")

time.sleep(5)
# Cerrar ventana emergente de las cookies
try:
    boton_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[2]/button')))
    boton_cookies.click()
except:
    pass

# Hacer clic en el botón "Download chart"
enlace_descarga = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-track-note="chart-click-download"]')))
enlace_descarga.click()


# Esperar a que aparezca el botón de descarga real
boton_descarga = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/article/div[2]/div[2]/div/div/section[1]/figure/div/div[3]/div/div[4]/div/div[2]/div/button')))
boton_descarga.click()

# Acceder a la página nro2
driver.get("https://ourworldindata.org/migration")

time.sleep(5)
# Cerrar ventana emergente de las cookies
try:
    boton_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[2]/button')))
    boton_cookies.click()
except:
    pass

# Hacer clic en el botón "Download chart"
enlace_descarga = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-track-note="chart-click-download"]')))
enlace_descarga.click()


# Esperar a que aparezca el botón de descarga real                                      
boton_descarga = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/article/div[2]/div/div/div/section/figure[1]/div/div[3]/div/div[4]/div/div[2]/div/button')))
boton_descarga.click()

time.sleep(2)

driver.quit()

paises_migraciones=pd.read_csv(r'C:\Users\gualas\Desktop\prueba\migration.csv')
paises_poblacion=pd.read_csv(r'C:\Users\gualas\Desktop\prueba\population-and-demography.csv')

conn = connect(':memory:') 
paises_migraciones.to_sql('pam',conn,index=False)
paises_poblacion.to_sql('pap',conn,index=False)

paises_migraciones_america = pd.read_sql('SELECT Year,Country,Emigrants,`International migrants`, `Net migration`, `Net migration rate` FROM pam WHERE Country IN ("Argentina","Belice","Bolivia", "Brasil","Canada","Colombia", "Costa Rica", "Cuba", "Chile", "Ecuador", "El Salvador", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru","Puerto Rico", "Republica Dominicana","United States","Uruguay","Venezuela","Antigua y Barbuda","Bahamas","Barbados","Dominica","Granada","Guyana","Jamaica","República Dominicana","San Cristobal y Nieves","San Vicente y las Granadinas","Santa Lucia")', conn)

paises_poblacion_america=pd.read_sql('SELECT `Country name`, Year, Population FROM pap WHERE `Country name` IN ("Argentina","Bolivia","Belice", "Brasil","Canada","Colombia", "Costa Rica", "Cuba", "Chile", "Ecuador", "El Salvador", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru","Puerto Rico", "Republica Dominicana","United States","Uruguay","Venezuela","Antigua y Barbuda","Bahamas","Barbados","Dominica","Granada","Guyana","Jamaica","República Dominicana","San Cristobal y Nieves","San Vicente y las Granadinas","Santa Lucia")',conn)

paises_migraciones_america.to_sql('a',conn,index=False)
paises_poblacion_america.to_sql('c',conn,index=False)

tabla=pd.read_sql('SELECT a.Year,a.Country,a.Emigrants,a.`International migrants`,a.`Net migration`,a.`Net migration rate`,c.Population FROM a a JOIN c c ON(a.Year=c.Year AND a.`Country`=c.`Country name` )',conn)

tabla.dropna(inplace=True)
tabla.reset_index(drop=True, inplace=True)

tabla['relative migration']=tabla['Emigrants']/tabla['Population']

print(tabla)