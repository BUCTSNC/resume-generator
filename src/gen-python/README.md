# Python方法

确定最后使用Pypi上仅存的Python读写PDF框架[fpdf2](https://pypi.org/project/fpdf2/)

文档可见 https://github.com/PyFPDF/fpdf2

先假设用户是windows，后期再做跨平台处理

非预设字体尤其是utf8字体需要自己安装到系统然后add到py文件，在此推荐sarasa而不是noto sans//serif hans或者source sans hans

https://forum.ubuntu.org.cn/viewtopic.php?t=492571 选择哪一个字体

https://github.com/be5invis/Sarasa-Gothic 下载（国内推荐TUNA镜像）

导入示例：

```python
pdf.add_font('更纱黑体', fname=os.path.join("C:\\","Windows","Fonts",'sarasa-mono-slab-sc-light.ttf'))
pdf.set_font('更纱黑体', size=14)
```

---

另有lxgw字体，见https://github.com/lxgw/LxgwWenKai/releases

导入示例：

```python
pdf.add_font('鹭霞文楷', fname=os.path.join("C:\\","Windows","Fonts",'LXGWWenKaiMono-Bold.ttf'))
pdf.set_font('鹭霞文楷', size=14)
```

