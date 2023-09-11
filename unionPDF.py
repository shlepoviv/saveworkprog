from io import BytesIO
from pathlib import Path
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from base64 import b64decode

# функциональное программирование

#байт64 в пдф
def b64toPdf(b64):

    # Decode the Base64 string, making sure that it contains only valid characters
    b = b64decode(b64, validate=True)

    if b[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature') 
    reader = PdfReader(BytesIO(b))
    return reader
    

def unionb64toPDF(fileName):
    """ 
    Возвращает метод mergeb64toPDF который объеденяет
    передаваемые станицы ПДФ в формате байт64 и записывает
    в файл при передаче признака конца 
    """

    merger = PdfWriter()
    #Создаем замыкание
    def mergeb64toPDF(b64, writeFlag = False):
        merger.append(b64toPdf(b64))
        if writeFlag:
            merger.write(fileName)
            merger.close()
        
    return mergeb64toPDF

# функциональное программирование
# Реализация классом
class Unionb64toPDF():
    def __init__(self,fileName = "file.pdf") -> None:
        self.merger = PdfWriter()
        self.fileName = fileName
 
    def append(self,b64):
        self.merger.append(b64toPdf(b64))
            
    def close(self):
        self.merger.write(self.fileName)
        self.merger.close() 

         

if __name__ == '__main__' :
    pathfPDF = Path("test", "test.pdf")
    pathtest64 = Path("test", "testStringb64.txt")

    uPDF = unionb64toPDF(pathfPDF)    
    f= open(pathtest64)
    uPDF(f.read(),True)
    fPDF = PdfReader(pathfPDF)
    page = fPDF.pages[0]
    print(page.extract_text())

    uPDF = Unionb64toPDF(pathfPDF)    
    f= open(pathtest64)
    uPDF.append(f.read())
    uPDF.close()
    fPDF = PdfReader(pathfPDF)
    page = fPDF.pages[0]
    print(page.extract_text())


