from time import sleep
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.print_page_options import PrintOptions

from unionPDF import union_b64_to_pdf

idProg = '63154'
catalog = Path(Path.home(),'RabProg')
if not (Path.exists(catalog) and Path.is_dir(catalog)):
    Path.mkdir(catalog)
outFile = Path(catalog,f'ID{idProg}.pdf')  
url = "https://rpd.rosnou.ru//RPDPrint/printrp?id=" + idProg


driver = webdriver.Chrome()

driver.get(url)

sleep(10)

# нажатие на кнопку ок
elemOk = driver.find_element(By.NAME, "btnOk1")
elemOk.click()

# параметры страницы -   без фона
PO = PrintOptions()
PO.background = False

flagEnd = False
namberPage = 1

updf = union_b64_to_pdf(outFile)

while not flagEnd:
    sleep(3)
    pagePDF = driver.print_page(PO)
    namberPage += 1
    elemNext = driver.find_element(By.NAME, "next")
    flagEnd = not elemNext.is_enabled()
    updf(pagePDF,flagEnd)
    elemNext.click()

driver.close()