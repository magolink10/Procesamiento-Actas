#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os

class Modulo1:

        
    def comprobarActa(self,selector,junta):
        #Con esta funcion determina en numero de acta 
        acta=''
        for a in selector:
            if ('>'+junta in a):
                acta=a.split('"')[1]      
        return acta
    
    def comprobarArchivo(self,acta,contenido):
        #COn esta funcion se verifica si un acta ya fue descargada
        encontrado=False
        if(acta+'.txt' in contenido):
            encontrado= True
        #return os.path.exists('ActasInfo/Info/'+acta+'.txt')
        return encontrado
    
    def descargar2019(self,acta,driver):
        #Funcion para descargar actas de Resultados2019
        i=0
        time.sleep(1)
        driver.execute_script("DoLogin()")
        time.sleep(2)
        driver.execute_script("document.getElementById('actaLink').click();")
        while(True):
            try:
                driver.find_element(By.ID,"btnDescargar").click()
                break
            except:
                time.sleep(1)
                try:
                    driver.switch_to.default_content()
                    n=driver.find_element(By.XPATH,"//*[@id='cboxLoadedContent']/iframe")
                    driver.switch_to.frame(n)
                except:
                    time.sleep(0.3)
                    pass
        f = open('ActasInfo/Info/'+acta+'.txt', "w")

        cabecera=(driver.find_element(By.XPATH,'//*[@id="datosActa"]/table[1]').get_attribute('innerText').split('\n'))
        for a in cabecera:
            div=a.split('\t')
            for u in range(0,len(div),2):

                f.write(div[u]+':'+div[u+1]+"\n")
        cabecera=(driver.find_element(By.XPATH,'//*[@id="tablaSufragantes"]').get_attribute('innerText').split('\n'))
        for a in cabecera:

            div=a.split('\t')
            for u in range(0,len(div),2):

                f.write(div[u]+':'+div[u+1]+"\n")

        votos=(driver.find_element(By.XPATH,'//*[@id="tablaCandi"]').get_attribute('innerText').split('\n'))
        for a in votos:
            f.write(a.split('\t')[2]+':'+a.split('\t')[3]+"\n")

        f.close()
        
        driver.switch_to.default_content()
        driver.find_element(By.ID,'cboxClose').click()

    def descargar2021(self,acta,driver,dignidad):
            #Funcion para descargar actas de Resultados 2021 y Resultados20212v
            i=0
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL+Keys.HOME)

            while (True):
                try:
                    driver.find_element(By.ID,"A2").click()
                    break
                except:
                    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL+Keys.HOME)   
                    try:
                        driver.find_element(By.ID,"btnConsultar").click()
                    except:
                        pass

            while (True):
                try:
                    driver.find_element(By.ID,"btnDescargarActa").click()

                    break
                except:
                    i+=1
                    if(i==100):
                        while (True):
                            try:
                                driver.find_element(By.XPATH,'//*[@id="pupupHeader"]/button').click()
                                break
                            except:

                                pass
                        return
                    time.sleep(0.5)

            f = open('ActasInfo/Info/'+acta+'.txt', "w")
            cabecera=(driver.find_element(By.XPATH,'//*[@id="datosActaJurisdiccion"]/div[3]').get_attribute('innerText').split('\n'))
            for a in range (0,len(cabecera),2):
                f.write(cabecera[a]+':'+cabecera[a+1]+"\n")

            votos=(driver.find_element(By.XPATH,'//*[@id="tablaCandi"]').get_attribute('innerText').split('\n'))
            for a in votos:
                if(dignidad=="seleccionarDignidadPopup(1);"):
                    f.write(a.split('\t')[1]+':'+a.split('\t')[2]+"\n")
                else:
                    f.write(a.split('\t')[0]+':'+a.split('\t')[1]+"\n")

            f.close()

            while (True):
                try:
                    driver.find_element(By.XPATH,'//*[@id="pupupHeader"]/button').click()
                    break
                except:
                    pass
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL+Keys.HOME)        
        
        
    def iniciar2019(self,driver,tipoEleccion,provincia,_URL,rutaEstado):
        #inicio de página web de Resultados 2019
        contenido=[]
        encontrado=False
        valorProvincia=provincia
        total=[]
        #Se comprueba el estado actual de descarga
        try:
            fic=open(rutaEstado)
            total=fic.read().split('\n')
            fic.close()
            actualCan=total[0]
            actualCir=total[1]
            actualParr=total[2]
            actualZon=total[3]
            actual=total[4]
            print (total)
        except:
            actualCan=''
            actualCir=''
            actualParr=''
            actualZon=''
            actual=''

        contenido = os.listdir('ActasInfo/Info/')
        #Se recarga la página hasta que se encuentre disponible
        while (True):
            try:

                driver.find_element(By.ID,tipoEleccion).click()
                print('Inicio')
                break
            except:
                time.sleep(3)
                driver.get(_URL)
        #Seleccion de elementos cuando existe una ciscunscripción
        time.sleep(1)
        select_fr = Select(driver.find_element(By.ID,"comboPro"))
        select_fr.select_by_value(valorProvincia)
        time.sleep(1)
        select_can = Select(driver.find_element(By.ID,"comboCanton"))
        canton=driver.find_element(By.ID,"comboCanton").get_attribute('innerText').split('\n')
        inicio=0
        time.sleep(1)
        for c in canton:

            if ('Todos' not in c):
                if(encontrado==False and actualCan!=''):
                    if(actualCan==c):
                        pass
                    else:
                        continue

                select_can = Select(driver.find_element(By.ID,"comboCanton"))
                select_can.select_by_index(canton.index(c))
                time.sleep(1)
                element = driver.find_element(By.ID,"comboCirc")
                if(element.is_enabled()):
                    select_circuncripcion = Select(element)
                    circuncripcion=element.get_attribute('innerText').split('\n')
                    for ci in circuncripcion:

                        if ('Todas' not in ci):
                            select_circuncripcion = Select(driver.find_element(By.ID,"comboCirc"))
                            select_circuncripcion.select_by_index(circuncripcion.index(ci))
                            time.sleep(1)


                            select_parroquia = Select(driver.find_element(By.ID,"comboParro"))
                            parroquia=driver.find_element(By.ID,"comboParro").get_attribute('innerText').split('\n')
                            for p in parroquia:
                                if(encontrado==False and actualParr!=''):
                                    if(actualParr==p):
                                        pass
                                    else:
                                        continue
                                if ('Todas' not in p):
                                    select_parroquia = Select(driver.find_element(By.ID,"comboParro"))
                                    select_parroquia.select_by_index(parroquia.index(p))
                                    time.sleep(1)
                                    select_zona = Select(driver.find_element(By.ID,"comboZona"))
                                    zona=driver.find_element(By.ID,"comboZona").get_attribute('innerText').split('\n')
                                    for z in zona:
                                        if(encontrado==False and actualZon!=''):
                                            if(actualZon==z):
                                                pass
                                            else:
                                                continue
                                        if ('Todas' not in z):

                                            select_zona = Select(driver.find_element(By.ID,"comboZona"))
                                            select_zona.select_by_index(zona.index(z))
                                            time.sleep(1)
                                            select_junta = Select(driver.find_element(By.ID,"comboJunta"))
                                            junta=driver.find_element(By.ID,"comboJunta")
                                            selector=junta.get_attribute('innerHTML').split("</option>")

                                            junta=junta.get_attribute('innerText').split('\n')
                                            for j in junta:

                                                if ('Todas' not in j):
                                                    acta=self.comprobarActa(selector,j)

                                                    if(encontrado==False and actual!=''):
                                                        if(actual==j):
                                                            #print('e')
                                                            encontrado=True
                                                            #pass
                                                        else:
                                                            continue

                                                    f = open(rutaEstado, "w")
                                                    f.write(c+"\n")
                                                    f.write(ci+"\n")
                                                    f.write(p+"\n")
                                                    f.write(z+"\n")
                                                    f.write(j+"\n")         
                                                    f.close()                                               

                                                    if(self.comprobarArchivo(acta,contenido)==False):
                                                        print (c,p,z,j,acta)
                                                        select_junta = Select(driver.find_element(By.ID,"comboJunta"))
                                                        select_junta.select_by_index(junta.index(j))
                                                        self.descargar2019(acta,driver)
                                                        inicio+=1
                                                        actual=j
                                                        actualCan=c
                                                        actualCir=ci
                                                        actualParr=p
                                                        actualZon=z
                                                        encontrado=True


                                                    if(inicio==50):
                                                        encontrado=False
                                                        driver.quit()
                                                        return
                #Seleccion de elementos cuando no existe una ciscunscripción
                else:                                    
                    select_parroquia = Select(driver.find_element(By.ID,"comboParro"))
                    parroquia=driver.find_element(By.ID,"comboParro").get_attribute('innerText').split('\n')
                    for p in parroquia:
                        if(encontrado==False and actualParr!=''):
                            if(actualParr==p):
                                pass
                            else:
                                continue
                        if ('Todas' not in p):
                            select_parroquia = Select(driver.find_element(By.ID,"comboParro"))
                            select_parroquia.select_by_index(parroquia.index(p))
                            time.sleep(1)
                            select_zona = Select(driver.find_element(By.ID,"comboZona"))
                            zona=driver.find_element(By.ID,"comboZona").get_attribute('innerText').split('\n')
                            for z in zona:
                                if(encontrado==False and actualZon!=''):
                                    if(actualZon==z):
                                        pass
                                    else:
                                        continue
                                if ('Todas' not in z):

                                    select_zona = Select(driver.find_element(By.ID,"comboZona"))
                                    select_zona.select_by_index(zona.index(z))
                                    time.sleep(1)
                                    select_junta = Select(driver.find_element(By.ID,"comboJunta"))
                                    junta=driver.find_element(By.ID,"comboJunta")
                                    selector=junta.get_attribute('innerHTML').split("</option>")

                                    junta=junta.get_attribute('innerText').split('\n')
                                    for j in junta:

                                        if ('Todas' not in j):
                                            acta=self.comprobarActa(selector,j)

                                            if(encontrado==False and actual!=''):
                                                if(actual==j):
                                                    #print('e')
                                                    encontrado=True
                                                    #pass
                                                else:
                                                    continue

                                            f = open(rutaEstado, "w")
                                            f.write(c+"\n")
                                            f.write("n/a\n")
                                            f.write(p+"\n")
                                            f.write(z+"\n")
                                            f.write(j+"\n")         
                                            f.close()                                               

                                            if(self.comprobarArchivo(acta,contenido)==False):
                                                print (c,p,z,j,acta)
                                                select_junta = Select(driver.find_element(By.ID,"comboJunta"))
                                                select_junta.select_by_index(junta.index(j))
                                                self.descargar2019(acta,driver)
                                                inicio+=1
                                                actual=j
                                                actualCan=c
                                                actualCir=''
                                                actualParr=p
                                                actualZon=z
                                                encontrado=True


                                            if(inicio==50):
                                                encontrado=False
                                                driver.quit()
                                                return
        encontrado=False
        driver.quit()                                        
        return
    
    def iniciar2021(self,driver,tipoEleccion,valorProvincia,_URL,rutaEtado):
        #inicio de página web de Resultados 2021 y Resultados 20212v
        rutaEstado=rutaEtado
        contenido=[]
        #Se comprueba el estado actual de descarga
        try:
            fic=open(rutaEstado)
            total=fic.read().split('\n')
            fic.close()
            actualCir=total[0]
            actualCan=total[1]
            actualParr=total[2]
            actualZon=total[3]
            actual=total[4]
            print (total)
        except:
            actualCan=''
            actualCir=''
            actualParr=''
            actualZon=''
            actual=''

        encontrado=False

        contenido = os.listdir('ActasInfo/Info/')    
        #Se recarga la página hasta que se encuentre disponible
        while (True):
            try:
                driver.execute_script(tipoEleccion)
                print('Inicio')
                break
            except:
                time.sleep(3)
                driver.get(_URL)
        #Seleccion de elementos 
        time.sleep(1)
        select_fr = Select(driver.find_element(By.ID,"ddlProvincia"))
        select_fr.select_by_value(valorProvincia)
        time.sleep(0.5)
        select_cir = Select(driver.find_element(By.ID,"ddlCircunscripcion"))
        circuncripcion=driver.find_element(By.ID,"ddlCircunscripcion").get_attribute('innerText').split('\n')
        inicio=0
        time.sleep(0.5)
        for ci in circuncripcion:

            if ('TODOS' not in ci):
                if(encontrado==False and actualCir!=''):
                    if(actualCir==ci):
                        pass
                    else:
                        continue
                select_cir.select_by_index(circuncripcion.index(ci))
                time.sleep(1)
                select_canton = Select(driver.find_element(By.ID,"ddlCanton"))
                canton=driver.find_element(By.ID,"ddlCanton").get_attribute('innerText').split('\n')
                for c in canton:
                    if(encontrado==False and actualCan!=''):
                        if(actualCan==c):
                            pass
                        else:
                            continue
                    if ('TODOS' not in c): 
                        select_canton.select_by_index(canton.index(c))
                        time.sleep(1)
                        select_parroquia = Select(driver.find_element(By.ID,"ddlParroquia"))
                        parroquia=driver.find_element(By.ID,"ddlParroquia").get_attribute('innerText').split('\n')
                        for p in parroquia:
                            if(encontrado==False and actualParr!=''):
                                if(actualParr==p):
                                    pass
                                else:
                                    continue
                            if ('TODOS' not in p):
                                select_parroquia.select_by_index(parroquia.index(p))
                                time.sleep(1)
                                select_zona = Select(driver.find_element(By.ID,"ddlZona"))
                                zona=driver.find_element(By.ID,"ddlZona").get_attribute('innerText').split('\n')
                                for z in zona:
                                    if(encontrado==False and actualZon!=''):
                                        if(actualZon==z):
                                            pass
                                        else:
                                            continue
                                    if ('TODOS' not in z):
                                        select_zona.select_by_index(zona.index(z))
                                        time.sleep(2)
                                        select_junta = Select(driver.find_element(By.ID,"ddlJunta"))
                                        junta=driver.find_element(By.ID,"ddlJunta")
                                        selector=junta.get_attribute('innerHTML').split("</option>")
                                        junta=junta.get_attribute('innerText').split('\n')
                                        for j in junta:

                                            if ('TODOS' not in j):
                                                acta=self.comprobarActa(selector,j)
                                                if(encontrado==False and actual!=''):
                                                    if(actual==j):
                                                        encontrado=True
                                                        #pass
                                                    else:
                                                        continue
                                                f = open(rutaEstado, "w")
                                                f.write(ci+"\n")
                                                f.write(c+"\n")
                                                f.write(p+"\n")
                                                f.write(z+"\n")
                                                f.write(j+"\n")         
                                                f.close()                                                   
                                                if(self.comprobarArchivo(acta,contenido)==False):
                                                    print (ci,c,p,z,j,acta)
                                                    select_junta.select_by_index(junta.index(j))
                                                    self.descargar2021(acta,driver,tipoEleccion)
                                                    inicio+=1
                                                    actual=acta
                                                    actualCir=ci
                                                    actualCan=c
                                                    actualParr=p
                                                    actualZon=z
                                                    encontrado=True

                                                if(inicio==50):
                                                    encontrado=False
                                                    driver.quit()
                                                    return
        encontrado=False
        driver.quit()                                        
        return


# In[ ]:


modulo1 = Modulo1('1')
for a in range (0,50):
    try:
        # Valores básicos
        _URL = 'https://app01-n1.cne.gob.ec/resultados2019/'
        tipoEleccion='ASPxButton2'
        valorProvincia='7'
        
        #Otros parametros
        chrome_options = webdriver.ChromeOptions()
        #creación del driver
        driver = webdriver.Chrome()
        #seleccionar ruta de descarga
        download_dir="C:\\Users\\Admin\\Desktop\\Tesis\\ActasInfo\\Acta\\"
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)
        #cargar driver
        driver.get(_URL)
        eleccion=_URL.split('/')[3]
        tipo=tipoEleccion.split('Button')[1]
        rutaEstado='ActasInfo/estado/'+eleccion+'-'+tipo+'-'+valorProvincia+'.txt'
        
        #inicio
        modulo1.iniciar2019(driver,tipoEleccion,valorProvincia,_URL,rutaEstado)
        
        driver.quit()
    except Exception as e:
        print (e)
        driver.quit()

    
print ('Fin')


# In[2]:


modulo1 = Modulo1('1')
for a in range (0,20):
    try:
        # Valores básicos
        _URL = "https://app01-n1.cne.gob.ec/resultados2021/"
        valorProvincia="4"
        tipoEleccion="seleccionarDignidadPopup(1);"
        
        #Otros parametros
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome()
        download_dir="C:\\Users\\Admin\\Desktop\\Tesis\\ActasInfo\\Acta\\"
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)
        driver.get(_URL) 
        eleccion=_URL.split('/')[3]
        tipo=tipoEleccion.split('(')[1].split(')')[0]
        rutaEstado='ActasInfo/estado/'+eleccion+'-'+tipo+'-'+valorProvincia+'.txt'
        
        #inicio 
        modulo1.iniciar2021(driver,tipoEleccion,valorProvincia,_URL,rutaEstado)
    except Exception as e:
        print (e)
        driver.quit()

print ('Fin')

