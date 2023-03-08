import datetime
import os
import sys
import xlrd
import requests
import glob
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Image


Contour = 'Contour'
pdfmetrics.registerFont(TTFont(Contour, 'Contour.ttf'))


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\src'
DIST_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\dist'
EXCEL_FILES = []
PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]
CONSTRUCTION_NAME = 'CONSTRUCTION_NAME'  # 社团名称
APARTMENT_NAME = 'APARTMENT_NAME'   #部门名称


def getFiles():
    for parent, dirnames, filenames in os.walk(SRC_PATH):
        for filename in filenames:
            if os.path.splitext(filename)[-1] == '.xls' or os.path.splitext(filename)[-1] == '.xlsx':
                EXCEL_FILES.append(f'{parent}\\{filename}')


def getData():
    fileData = {}
    for filename in EXCEL_FILES:
        try:
            table = xlrd.open_workbook(filename)
            sheet = table.sheet_by_index(0)
            tableData = []
            for i in range(1, sheet.nrows):
                rowData = {'id': sheet.cell_value(i, 0), 'name': sheet.cell_value(i, 6),
                           'gender': sheet.cell_value(i, 7), 'nation': sheet.cell_value(i, 8),
                           'tel': sheet.cell_value(i, 9), 'photo': sheet.cell_value(i, 10),
                           'college': sheet.cell_value(i, 11), 'position': sheet.cell_value(i, 12),
                           'class': sheet.cell_value(i, 13), 'speciality': sheet.cell_value(i, 14),
                           'first': sheet.cell_value(i, 15), 'second': sheet.cell_value(i, 16),
                           'adjustment': sheet.cell_value(i, 17), 'remarks': sheet.cell_value(i, 18)}
                tableData.append(rowData)
            fileData[filename] = tableData
        except xlrd.biffh.XLRDError:
            print(f'\033[31m ERROE! {filename} generate failed! File size error! Please check the file!\033[0m')
    return fileData


def _changeSize(filein, fileout):
    img = pImg.open(filein)
    if img.size[0] > img.size[1]:
        width = 800
        height = 600
    else:
        width = 600
        height = 800
    type = img.format
    out = img.resize((width, height), Image.ANTIALIAS)
    # 第二个参数：
    # Image.NEAREST ：低质量
    # Image.BILINEAR：双线性
    # Image.BICUBIC ：三次样条插值
    # Image.ANTIALIAS：高质量
    out.save(fileout, type)


def downloadImages(fileData):
    newData = fileData
    for filename in fileData:
        fileDir = BASE_PATH + '\\dist\\' + filename.split('\\')[-1].split('.')[0]
        if os.path.exists(fileDir):
            if os.path.exists(fileDir + '\\images'):
                pass
            else:
                os.makedirs(fileDir + '\\images')
        else:
            os.makedirs(fileDir)
            os.makedirs(fileDir + '\\images')
        imgBasePath = fileDir+'\\images'
        # print(imgBasePath)
        index = 1
        total = len(fileData[filename])

        for row in fileData[filename]:
            if not os.path.exists(imgBasePath + '\\' + row['name'] + '.jpg'):
                # print(row['photo'])
                img = requests.get(row['photo'], stream=True)
                with open(imgBasePath + '\\' + row['name'] + '.jpg', 'wb+') as f:
                    for chunk in img.iter_content(chunk_size=512):
                        if chunk:
                            f.write(chunk)
                f.close()
            newData[filename][index-1]['photo'] = imgBasePath + '\\' + row['name'] + '.jpg'
            print("\r", end="")
            print(f"Download images: {index}/{total} ", "▋" * (index // 2), end="")
            sys.stdout.flush()
            index += 1
        print('\nDownload finished!')
        # changeSize(filename.split('\\')[-1].split('.')[0])
        return newData


def drawBasicInfo(c: Canvas, info, filename):
    c.saveState()
    c.setFillColor(colors.black)
    c.setFont(Contour, 12)
    c.drawString(50, PAGE_HEIGHT - 140, f"姓名: {info['name']}")
    c.drawString(50, PAGE_HEIGHT - 160, f"性别: {info['gender']}")
    c.drawString(50, PAGE_HEIGHT - 180, f"民族: {info['nation']}")
    c.drawString(50, PAGE_HEIGHT - 200, f"学院: {info['college']}")
    c.drawString(50, PAGE_HEIGHT - 220, f"班级: {info['class']}")
    c.drawString(50, PAGE_HEIGHT - 260, f"第一志愿: {info['first']}")
    c.drawString(50, PAGE_HEIGHT - 280, f"第二志愿: {info['second']}")
    c.drawString(50, PAGE_HEIGHT - 300, f"是否接受调剂:  {info['adjustment']}")
    c.drawString(50, PAGE_HEIGHT - 320, f"特长: {info['speciality']}")
    c.drawString(50, PAGE_HEIGHT - 360, f"备注: {info['remarks']}")
    
    # 显示图片
    # image_path = f"dist/{filename}/images/{info['name']}.jpg"
    # img = Image(image_path)
    # width = img.drawWidth
    # height = img.drawHeight
    # if width <= 3000 and height <= 5000:
    #     c.drawImage(image=image_path, x=PAGE_WIDTH-60-width * 0.1, y=PAGE_HEIGHT-120-height * 0.1,
    #                 width=width * 0.1, height=height * 0.1,
    #                 mask=None, preserveAspectRatio=False, anchor='c',
    #                 anchorAtXY=True, showBoundary=True)
    # else:
    #     c.drawImage(image=image_path, x=PAGE_WIDTH - 60 - width * 0.05, y=PAGE_HEIGHT - 120 - height * 0.05,
    #                 width=height * 0.05, height=width * 0.05,
    #                 mask=None, preserveAspectRatio=False, anchor='c',
    #                 anchorAtXY=True, showBoundary=True)
    c.restoreState()


def drawPage(c, info, filename):
    c.saveState()
    c.setFillColor(colors.black)
    c.setFont(Contour, 26)
    c.drawCentredString(300, PAGE_HEIGHT - 70, f"{CONSTRUCTION_NAME}面试简历")
    c.line(30, PAGE_HEIGHT - 100, 570, PAGE_HEIGHT - 100)
    c.setStrokeColor(colors.dimgrey)
    c.line(30, PAGE_HEIGHT - 790, 570, PAGE_HEIGHT - 790)
    c.setFont(Contour, 8)
    c.setFillColor(colors.black)
    c.drawString(30, PAGE_HEIGHT - 810, f"生成日期：{datetime.date.today()}")
    c.drawString(PAGE_WIDTH-(len(CONSTRUCTION_NAME) + 7)*8-30, PAGE_HEIGHT - 810, f'仅用作{CONSTRUCTION_NAME}面试使用')
    drawBasicInfo(c, info, filename)
    c.restoreState()


def main():
    # doc = SimpleDocTemplate("dist/output/pdftest.pdf")
    # Story = [Spacer(1, 2 * inch)]
    # doc.build(Story, onFirstPage=myFirstPage)
    # my_canvas = Canvas('dist/output/pdftest.pdf', pagesize=A4)
    # drawPage(my_canvas)
    # my_canvas.save()
    getFiles()
    infos = downloadImages(getData())
    print("generating...")
    for filename in infos:
        fileDir = BASE_PATH + '\\dist\\' + filename.split('\\')[-1].split('.')[0]
        name = filename.split('\\')[-1].split('.')[0]
        if os.path.exists(fileDir):
            pass
        else:
            os.makedirs(fileDir)
        for info in infos[filename]:
            if os.path.exists(BASE_PATH + '\\dist\\'+name+'\\{APARTMENT_NAME}'):
                pass
            else:
                os.makedirs(BASE_PATH + f'\\dist\\'+name+'\\{APARTMENT_NAME}')
            if os.path.exists(BASE_PATH + f'\\dist\\'+name+'\\{APARTMENT_NAME}\\第一志愿'):
                pass
            else:
                os.makedirs(BASE_PATH + f'\\dist\\'+name+'\\{APARTMENT_NAME}\\第一志愿')
            if os.path.exists(BASE_PATH + f'\\dist\\'+name+'\\{APARTMENT_NAME}\\第二志愿'):
                pass
            else:
                os.makedirs(BASE_PATH + f'\\dist\\'+name+'\\{APARTMENT_NAME}\\第二志愿')
            if info['first'] == '{APARTMENT_NAME}':
                can = Canvas(f"dist\\{name}\\{APARTMENT_NAME}\\第一志愿\\{info['name']}.pdf", pagesize=A4)
                drawPage(can, info, name)
                can.save()
            elif info['second'] == '{APARTMENT_NAME}':
                can = Canvas(f"dist\\{name}\\{APARTMENT_NAME}\\第二志愿\\{info['name']}.pdf", pagesize=A4)
                drawPage(can, info, name)
                can.save()
        try:
            for i in os.listdir(f"dist\\{name}\\images_fixed"):
                path = os.path.join(f"dist\\{name}\\images_fixed", i)
                os.remove(path)
            os.rmdir(f"dist\\{name}\\images_fixed")
        except FileNotFoundError:
            print('', end='')
    print('finish!', end='')


if __name__ == '__main__':
    main()
