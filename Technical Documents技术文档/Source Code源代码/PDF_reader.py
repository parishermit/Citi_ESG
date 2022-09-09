"""
author: guohang
"""

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def pdf_reader(path):
    res_scentence = ""
    fp = open(path, 'rb')
    praser = PDFParser(fp)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:

        rsrcmgr = PDFResourceManager()

        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)


        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages():  # doc.get_pages() 获取page列表

                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        # 需要写出编码格式
                        tmp_scetence = x.get_text()
                        res_scentence += tmp_scetence.strip('\n')
    return res_scentence
if __name__ == '__main__':
    path = r"C:\Users\Eleven最沉着\Desktop\venv\2019-04-23-600309.SH-600309万华化学2018年度社会责任报告.pdf"
    try:
        pdf_txt = pdf_reader(path)
        print(pdf_txt)
    except :
        print('提取失败')
    # xinxi=[]
    # print(len(xinxi))



