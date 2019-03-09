# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 10:54:28 2018

@author: carlo
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pyautogui
import sqlite3



def insertDB(query):
    
    conn = sqlite3.connect('D:/Projeto/tcc/TCC2.db')           
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

# Configura o driver com o caminho de instalação do selenium
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False) 

driver = webdriver.Firefox(profile, executable_path=r'C:\Program Files (x86)\SeleniumWrapper\geckodriver.exe')







link = 'http://www.ogol.com.br/edition_matches.php?id_edicao=122072&page='


ano = 2018
    
# pega tabela de todos os anos
while(ano >= 1971):
    for k in range(1,8):
        
        # Abre site
        driver.get(link + repr(k))
        
        texto = ''
        
        # Aguarda o elemento
        for i in range(60):
            time.sleep(1)
            try:
                driver.find_element_by_xpath('//*[@id="container"]/div[3]/a').click()        
            except Exception:
                pass
            try:
                texto = driver.page_source
                if texto.find('</td><td style="width:38px;"></td><td style="width:38px;"></td><td style="width:38px;">') > 1:                    
                    break
            except Exception:
                pass
            if i == 30:
                driver.refresh()
                        
        time.sleep(1)
        
        
        texto = driver.page_source
        
        # = texto.split('</div></td></tr><tr')[1]
            
        data1 = ''
        data = ''
        hora = ''
        casa = ''
        placar = ''
        foraCasa = ''
        fase = ''
        #divide = '</td><td style="width:38px;"></td><td style="width:38px;"></td><td style="width:38px;">'
        for i in range(1, 51):
            try:
                data = texto.split('class="date">')[i]
                data = data.split('<')[0]
            except Exception:
                pass
            
            # tem duas formas de trazer o nome dos times, com ou sem bold
            try:
                casa = texto.split('text home"><a href="/equipa.php?id=')[i]
                casa = casa.split('>')[1]
                casa = casa.split('<')[0]
                if len(casa) == 0:
                    casa = texto.split('text home"><a href="/equipa.php?id=')[i]
                    casa = casa.split('<b>')[1]
                    casa = casa.split('<')[0]
            except Exception:                
                pass
            
                
            
            try:
                placar = texto.split('result"><a href="/jogo.php?id=')[i]
                placar = placar.split('>')[1]
                placar = placar.split('<')[0]
            except Exception:
                pass
            
            # tem duas formas de trazer o nome dos times, com ou sem bold
            try:
                foraCasa = texto.split('text away"><a href="/equipa.php?id=')[i]
                foraCasa = foraCasa.split('>')[1]
                foraCasa = foraCasa.split('<')[0]
                if len(foraCasa) == 0:
                    foraCasa = texto.split('text away"><a href="/equipa.php?id=')[i]
                    foraCasa = foraCasa.split('<b>')[1]
                    foraCasa = foraCasa.split('<')[0]
            except Exception:                
                pass
            
            
            try:
                fase = texto.split('class="phase">')[i]
                fase = fase.split('<')[0]
            except Exception:
                pass
        
            #print(data, casa, placar, foraCasa, fase)
            
            insertDB("""INSERT INTO calendario(data, casa, placar, foracasa, fase)
                    VALUES ('"""+ data + """','""" + casa + """','"""
                            + placar + """','""" + foraCasa + """','""" + fase + """')""")
            
    
    # trova ano    
    ano = ano -1
    
    driver.find_element_by_xpath('//*[@id="id_edicao_chosen"]').click()    
    pyautogui.press('down')
    pyautogui.press('enter')
    for i in range(10):
        time.sleep(1)
        a = driver.page_source
        if a.find('Classificação') > 1:
            break
    
    b = driver.current_url
    link = 'http://www.ogol.com.br/edition_matches.php?id_edicao=' + b.split('=')[1] + '&page='
    #limpa os cookies
    driver.delete_all_cookies()
    
    
    
  