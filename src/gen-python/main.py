from fpdf import FPDF

import os


pdf = FPDF()
pdf.add_page()
pdf.add_font('更纱黑体', fname=os.path.join("C:\\","Windows","Fonts",'sarasa-mono-slab-sc-light.ttf'))
pdf.set_font('更纱黑体', size=14)
pdf.cell(txt="你好，世界")

if os.path.exists(os.path.join(os.getcwd(),"output")) == False:
    os.mkdir(os.path.join(os.getcwd(),"output"))
pdf.output(os.path.join(os.getcwd(),"output","hello_world.pdf"))