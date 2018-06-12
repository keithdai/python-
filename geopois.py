# -*- coding: utf-8 -*-
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import xlrd
import xlwt
from Tkinter import *
import tkMessageBox
import tkFileDialog as tkFD
import urllib
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

sfilename=''
keywrod='肯德基'
cityname='南海区'

def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    #lng=float(lng)
    #lat=float(lat)
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret
def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def on_click():  # 单击函数xls_text,sheet_text,loop_text,sleep_text
    # databasename = self.xls_text.get()#数据库
    # tablename = self.sheet_text.get()#数据库
    cityname = city_text.get()
    keywrod= keyword_text.get()
    #save = self.save_text.get()
    # self.interval = self.sleep_text.get()
    # save=self.save_text.get()
    # string = str("数据库名：%s sheet名：%s 持续时间：%s 间隔时间：%s key=：%s" % (databasename, tablename, self.duration, self.interval,save))
    # print("xls名：%s sheet名：%s 持续时间：%s 间隔时间：%s " % (x, s, l, sl))
    tkMessageBox.showinfo(title='采集POIs', message='选择文件保存位置')
    sfilename = tkFD.asksaveasfilename(initialdir='C:', defaultextension='xls',
                                       filetypes=[('all files', '.*'), ('text files', '.xls')],
                                       initialfile='1.xls', title='选择输出文件保存的位置')  # 打开对话框存文件
    page = '1'
    url = 'http://restapi.amap.com/v3/place/text?key=a0e8201f84716690ae7c07155273d03a&keywords=' + keywrod + '&types=&city=' + cityname + '&children=1&citylimit=true&offset=20&page=1&extensions=all'
    # url = 'http://restapi.amap.com/v3/place/polygon?key=a0e8201f84716690ae7c07155273d03a&polygon=' + (coords) + '&keywords='+keywrod+'&types=&offset=20&page='+page+'&extensions=all'
    r = requests.get(url, auth=('user', 'pass'))
    r_js = r.json()
    count = r_js['count']
    print '该关键词POIS共计：'
    print count
    workbook = xlwt.Workbook()  # 注意Workbook的开头W要大写
    sheetname = cityname + keywrod
    sheet1 = workbook.add_sheet('POIs', cell_overwrite_ok=True)  # 创建excel表
    sheet1.write(0, 0, 'pname')
    sheet1.write(0, 1, 'cityname')
    sheet1.write(0, 2, 'adname')
    sheet1.write(0, 3, 'caddress')
   # sheet1.write(0, 4, 'location')
    sheet1.write(0, 4, 'name')
    sheet1.write(0, 5, 'type')
    sheet1.write(0, 6, 'GCJ02-lng')
    sheet1.write(0, 7, 'GCJ02-lat')
    sheet1.write(0, 8, 'WGS1984-lng')
    sheet1.write(0, 9, 'WGS1984-Lat')
    curline = 1
    for num in range(1,int(count) / 20 + 2):
        url = 'http://restapi.amap.com/v3/place/text?key=a0e8201f84716690ae7c07155273d03a&keywords='+ keywrod + '&types=&city=' + cityname + '&children=1&offset=20&page=' + str(
            num) + '&extensions=all'
        # url = 'http://restapi.amap.com/v3/place/polygon?key=a0e8201f84716690ae7c07155273d03a&polygon=' + coords + '&keywords='+keywrod+'&types=&offset=20&page='+str(num)+'&extensions=all'
        r = requests.get(url, auth=('user', 'pass'))
        r_js = r.json()
        pois = r_js['pois']
        for p in pois:
            address = p['address']
            adname = p['adname']
            cityname1 = p['cityname']
            pname = p['pname']
            location = p['location']
            name = p['name']
            type = p['type']
            sheet1.write(curline, 3, address)
            sheet1.write(curline, 2, adname)
            sheet1.write(curline, 1, cityname1)
            sheet1.write(curline, 0, pname)
            sheet1.write(curline, 4, name)
            sheet1.write(curline, 5, type)
            xy=location.split(',')
            sheet1.write(curline, 6, float(xy[0]))
            sheet1.write(curline, 7, float(xy[1]))
            wgsxy=gcj02_to_wgs84(float(xy[0]),float(xy[1]))
            sheet1.write(curline, 8, wgsxy[0])
            sheet1.write(curline, 9, wgsxy[1])
            curline += 1
    workbook.save(sfilename)
    #print 'SNM'
    tkMessageBox.showinfo(title='采集高德POIs', message='采集成功')
    return
root = Tk()
root.title("POIs采集系统（高德接口）v 0.1")
root.geometry('500x110')  # 是x 不是*
l3 = Label(root, text="采集城市（区）：")
l3.place(x=10, y=10, width=100, height=30)  # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
city_text = StringVar()
loop = Entry(root, textvariable=city_text,foreground = '#0F0F0F')
city_text.set("南海")
loop.place(x = 120, y = 10, width=80, height=30)
l3 = Label(root, text="采集POI关键词：")
l3.place(x=210, y=10, width=100, height=30)  # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
keyword_text = StringVar()
loop = Entry(root, textvariable=keyword_text,foreground = '#0F0F0F')
keyword_text.set("肯德基")
loop.place(x = 320, y = 10, width=80, height=30)
Button(root, text="开始采集", command=on_click, bg='#CDB7B5').place(x=410, y=10, width=80, height=30)
l3 = Label(root, text="数据为火星坐标系+WGS坐标系")#daizhi@sutpc.com，QQ：493549072
l3.place(x=10, y=50, width=480, height=30)  # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM3
l3 = Label(root, text="daizhi@sutpc.com，QQ：493549072，仅供学习参考")#daizhi@sutpc.com，QQ：493549072
l3.place(x=10, y=80, width=480, height=30)  # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
root.mainloop()
#cityname = str(raw_input("你所需要采集的POI的城市?"))
#keywrod = str(raw_input("你所需要采集的POI的关键词?"))
