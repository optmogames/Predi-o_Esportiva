# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 10:54:28 2018

@author: carlo
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import sqlite3


def insertDB(query):    
    conn = sqlite3.connect('D:/Projeto/tcc/TCC2.db')           
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

# Configura o driver com o caminho de instalação do selenium
driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\SeleniumWrapper\chromedriver.exe')

link = 'http://www.ogol.com.br/edition.php?id_edicao=122072'

    
# Abre site
driver.get(link)

for i in range(60):
    time.sleep(1)
    try:
        driver.find_element_by_xpath('//*[@id="container"]/div[3]/a').click()        
    except Exception:
        pass
    try:
        wait = WebDriverWait(driver, 1)
        elemento = wait.until(EC.element_to_be_clickable((By.ID, 'page_submenu')))
        break
    except Exception:
        pass 

select_box = driver.find_element_by_name("id_edicao")
options = [x for x in select_box.find_elements_by_tag_name("option")]
ano = []
ano1=[]


for element in options:
    ano.append(element.get_attribute("value"))
    
for i in range(2018, 1989, -1):
    ano1.append(repr(i))

    

link = 'http://www.ogol.com.br/edition.php?id_edicao='
for i in range(len(ano)):
    
    texto = ''
        
    # Aguarda o elemento
    for j in range(60):
        time.sleep(1)       
        try:
            texto = driver.page_source
            if texto.find('todos jogos disputados">') > 1:                    
                break
        except Exception:
            pass
        if j == 30:
            driver.refresh()
                    
    time.sleep(1)
    
    
        
    texto = driver.page_source
    texto = texto.split('</div></div></div><div id="page_submenu" style="background-color:rgb')[1]
    
    
    
    clube = ''
    jogosDisp = ''
    vitorias = ''
    empates = ''
    derrotas = ''
    golsMarcados = ''
    golsSofridos = ''
    
    
    
    
    
    for k in range(1, 21):
        try:
            clube = texto.split('href="/equipa.php?id=')[k]
            clube = clube.split('>')[1]
            clube = clube.split('<')[0]
        except Exception:
            pass
        
        try:
            jogosDisp = texto.split('todos jogos disputados">')[k]
            jogosDisp = jogosDisp.split('<')[0]
        except Exception:
            pass
        
        try:
            vitorias = texto.split('todas as vitórias">')[k]
            vitorias = vitorias.split('<')[0]
        except Exception:
            pass
        
        try:
            empates = texto.split('todos os empates">')[k]
            empates = empates.split('<')[0]
        except Exception:
            pass
        
        try:
            derrotas = texto.split('todas as derrotas">')[k]
            derrotas = derrotas.split('<')[0]
        except Exception:
            pass
        
        try:
            golsMarcados = texto.split('jogos com gols marcados">')[k]
            golsMarcados = golsMarcados.split('<')[0]
        except Exception:
            pass
        
        try:
            golsSofridos = texto.split('jogos com gols sofridos">')[k]
            golsSofridos = golsSofridos.split('<')[0]
        except Exception:
            pass
        
    
        
        
        # insere no banco
        insertDB("""INSERT INTO classificacao(clube, jogosDisp, vitorias, empates, derrotas, golsMarcados, golsSofridos, ano)
                VALUES ('"""+ clube + """','""" + jogosDisp + """','""" + vitorias + """','""" + empates + """','""" 
                        + derrotas + """','""" + golsMarcados + """','""" + golsSofridos + """','"""+ ano1[i] + """')""")
        
    # troca ano
    driver.get(link + ano[i + 1])
    if ano == '1990':
        break
    
