from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def iniciar_driver():
    options = webdriver.ChromeOptions()

    caminho_perfil = r"C:\whatsapp_perfil"

    if not os.path.exists(caminho_perfil):
        os.makedirs(caminho_perfil)

    options.add_argument(f"user-data-dir={caminho_perfil}")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://web.whatsapp.com/")
    time.sleep(25)

    return driver


def abrir_conversa(driver, contato):
    time.sleep(5)

    # pega TODAS caixas editáveis
    caixas = driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')

    if len(caixas) == 0:
        raise Exception("Campo de busca não encontrado")

    busca = caixas[0]

    busca.click()
    time.sleep(1)

    busca.send_keys(Keys.CONTROL + "a")
    busca.send_keys(Keys.DELETE)

    busca.send_keys(contato)
    time.sleep(3)

    try:
        driver.find_element(By.XPATH, f'//span[@title="{contato}"]').click()
    except:
        raise Exception(f"Contato não encontrado: {contato}")

    time.sleep(3)


def enviar_imagem(driver, caminho, legenda):
    time.sleep(2)

    # botão anexo
    driver.find_element(By.XPATH, '//span[@data-icon="clip"]').click()
    time.sleep(2)

    # upload
    inputs = driver.find_elements(By.XPATH, '//input[@type="file"]')

    if len(inputs) == 0:
        raise Exception("Campo de upload não encontrado")

    inputs[0].send_keys(caminho)
    time.sleep(5)

    # pega todas caixas editáveis novamente
    caixas = driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')

    if len(caixas) == 0:
        raise Exception("Campo de legenda não encontrado")

    caixa_legenda = caixas[-1]
    caixa_legenda.click()
    caixa_legenda.send_keys(legenda)

    time.sleep(2)

    # enviar
    driver.find_element(By.XPATH, '//span[@data-icon="send"]').click()
    time.sleep(4)
