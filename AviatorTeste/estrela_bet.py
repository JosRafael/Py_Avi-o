import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Carrega as credenciais do arquivo credentials.json
with open('credentials.json', 'r') as file:
    credentials = json.load(file)

login = credentials["login"]
senha = credentials["senha"]

# Configurar o driver Selenium
driver = webdriver.Chrome()
driver.get("https://estrelabet.com/pb/gameplay/aviator/real-game")

# Esperar pelo botão de aceitar cookies
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div[2]/app-cookie-policy/div/div/div/span/button'))
)

# Aceitar cookies
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/app-root/div[2]/app-cookie-policy/div/div/div/span/button').click()
time.sleep(2)

# Clicar no botão "Entre"
element = driver.find_element(By.XPATH, '/html/body/modal[2]/div/div/div/div/app-loginform/div/div[4]/div/div')
element.click()

# Preencher os campos de login e senha
driver.find_element(By.XPATH, '/html/body/modal[2]/div/div/div/div/app-loginform/div/div[4]/div/div/div[3]/form/div[1]/div/input').send_keys(login)
driver.find_element(By.XPATH, '/html/body/modal[2]/div/div/div/div/app-loginform/div/div[4]/div/div/div[3]/form/div[2]/div/input').send_keys(senha)

# Clicar no botão de login
driver.find_element(By.XPATH, '/html/body/modal[2]/div/div/div/div/app-loginform/div/div[4]/div/div/div[3]/form/div[4]/button[1]').click()

while len(driver.find_elements(By.XPATH, '/html/body/app-root/div[1]/div[1]/app-gamingwindow/div/div/div/div[2]/div/div/div/div[2]/iframe')) == 0:
    time.sleep(2)

iframe1 = driver.find_element(By.XPATH, '/html/body/app-root/div[1]/div[1]/app-gamingwindow/div/div/div/div[2]/div/div/div/div[2]/iframe')

driver.switch_to.frame(iframe1)

while len(driver.find_elements(By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div')) == 0:
    time.sleep(2)

json_file_name = 'resultados.json'

def escrever_resultados_json(dados):
    with open(json_file_name, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False)

# Obtém os resultados iniciais
resultado = driver.find_element(By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div')
ultimos_resultados = resultado.text.split()
ultimo_resultado_impresso = None
resultados_impressos = set()

while True:
    # Verifica se o elemento está presente
    if len(driver.find_elements(By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div')) == 0:
        time.sleep(2)
        continue  # Se não estiver presente, espera e tenta novamente

    # Lê o texto atual do elemento de resultados
    resultado_atual = driver.find_element(By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div').text.split()

    # Verifica se o resultado atual já foi impresso
    if resultado_atual != ultimos_resultados:
        print(resultado_atual)
        ultimos_resultados = resultado_atual  # Atualiza os últimos resultados
        # Escreve os resultados no arquivo .json
        escrever_resultados_json({"Ultimos Numeros": resultado_atual})

    time.sleep(1)
