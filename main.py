from time import sleep
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.print_page_options import PrintOptions

from unionpdf import union_b64_to_pdf

id_prog = '63154'
catalog = Path(Path.home(),'RabProg')
if not (Path.exists(catalog) and Path.is_dir(catalog)):
    Path.mkdir(catalog)
out_file = Path(catalog,f'ID{id_prog}.pdf')  
url = "https://rpd.rosnou.ru//RPDPrint/printrp?id=" + id_prog


driver = webdriver.Chrome()

driver.get(url)

sleep(10)

# нажатие на кнопку ок
elem_ok = driver.find_element(By.NAME, "btnOk1")
elem_ok.click()

# параметры страницы -   без фона
PO = PrintOptions()
PO.background = False

flag_end = False

updf = union_b64_to_pdf(out_file)

while not flag_end:
    sleep(3)
    page_pdf = driver.print_page(PO)
    elem_next = driver.find_element(By.NAME, "next")
    flag_end = not elem_next.is_enabled()
    updf(page_pdf,flag_end)
    elem_next.click()

driver.close()