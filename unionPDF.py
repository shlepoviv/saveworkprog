from io import BytesIO
from pathlib import Path
from base64 import b64decode
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter


# функциональное программирование

# байт64 в пдф
def b64_to_pdf(b64):

    # Decode the Base64 string, making sure that it contains only valid characters
    byte_dec = b64decode(b64, validate=True)

    if byte_dec[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')
    reader = PdfReader(BytesIO(byte_dec))
    return reader


def union_b64_to_pdf(file_name):
    """ 
    Возвращает метод mergeb64toPDF который объеденяет
    передаваемые станицы ПДФ в формате байт64 и записывает
    в файл при передаче признака конца 
    """

    merger = PdfWriter()
    # Создаем замыкание

    def merge_b64_to_pdf(b64, write_flag=False):
        merger.append(b64_to_pdf(b64))
        if write_flag:
            merger.write(file_name)
            merger.close()

    return merge_b64_to_pdf

# функциональное программирование
# Реализация классом


class Unionb64toPDF():
    def __init__(self, file_name="file.pdf") -> None:
        self.merger = PdfWriter()
        self.file_name = file_name

    def append(self, b64):
        self.merger.append(b64_to_pdf(b64))

    def close(self):
        self.merger.write(self.file_name)
        self.merger.close()


if __name__ == '__main__':
    path_fpdf = Path("test", "test.pdf")
    path_test64 = Path("test", "testStringb64.txt")

    u_pdf = union_b64_to_pdf(path_fpdf)
    f = open(path_test64, encoding='utf-8')
    u_pdf(f.read(), True)
    f_pdf = PdfReader(path_fpdf)
    page = f_pdf.pages[0]
    print(page.extract_text())

    u_pdf = Unionb64toPDF(path_fpdf)
    f = open(path_test64, encoding='utf-8')
    u_pdf.append(f.read())
    u_pdf.close()
    f_pdf = PdfReader(path_fpdf)
    page = f_pdf.pages[0]
    print(page.extract_text())
