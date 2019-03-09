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
import pandas as pd
import numpy as np
import lxml.html
import matplotlib.pyplot as plt
from io import StringIO




# Configura o driver com o caminho de instalação do selenium
driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\SeleniumWrapper\chromedriver.exe')

link = 'http://www.ogol.com.br/edition_matches.php?id_edicao=122072&page='

f = open('base.txt', 'w')
for k in range(1,9):
    
    # Abre site
    driver.get(link + repr(k))
    
    # Aguarda o elemento
    for i in range(60):
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//*[@id="container"]/div[3]/a').click()        
        except Exception:
            pass
        try:
            wait = WebDriverWait(driver, 1)
            elemento = wait.until(EC.element_to_be_clickable((By.ID, 'team_games')))
            break
        except Exception:
            pass
        
    time.sleep(1)
    
    element = driver.find_element_by_xpath('//*[@id="team_games"]/table')
    texto = element.text
    
    texto = texto.split('FASE')[1]
    texto = texto.replace('h2h ', '')
    texto = texto.replace(' FG', '')
    
    data1 = ''
    for i in range(50):
        try:
            linha = texto.split('\n')[i]
            linha = linha.replace(' ', ';')
            for j in range(10):
                if linha.find('R' + repr(j)) > 1:
                   fora = linha.find('R' + repr(j))
                   a = linha[17:fora - 1].split('-')[0]
                   b = a.count(';')
                   if b > 1:
                       a = a.replace(';', ' ', 1)
                   a = a.split(';')[0]
            
            data = linha.split(';')[0]
            hora = linha.split(';')[1]
            casa = a    
            if linha[-1] == ';':
                linha = linha[0:len(linha)-1]        
            c = linha.split('-')[2].count(';')
            d = linha.split('-')[3].count(';')
            if c > 3:
                placar = linha.split(';')[4]
            else:
                placar = linha.split(';')[3]    
            if d > 2:
                d = linha.split('-')[3]
                foraCasa = d.split(';')[1] + ' ' + d.split(';')[2]
                fase = d.split(';')[3]
            else:
                d = linha.split('-')[3]
                foraCasa = d.split(';')[1]
                fase = d.split(';')[2]          
            data1 = data1 + data + ';' + hora + ';' + casa + ';' + placar + ';' + foraCasa + ';' + fase + '\n'
        except Exception:
            pass
    f.write(data1 + '\n')

f.close()