#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: tanzz
# Date : 2021/5/28 9:41
# File : Assister md_image_mul_thread_download.py
# Desc : wx: throup
# ----------Import---------------
import os
import tkinter
from tkinter import messagebox
from tkinter.messagebox import showinfo
from urllib.request import urlretrieve

import windnd
import re

IMG_TAG = r'![图片](http'
IMG_TAG_CNT = len(IMG_TAG)
IMG_FOLDER = 'images'


def draggedFiles(files):
    for file in files:
        filepath = file.decode('gbk')
        ret = mdFileHandle.handle(filepath)


class TkView:
    def __init__(self, tk):
        self.tk = tk

    def init(self):
        pass


class mdFileHandle:
    @classmethod
    def preHandle(cls, filepath):
        if not os.path.exists(filepath):
            # raise Exception("文件不存在: " + filepath)
            return -1, None
        filepath, filename = os.path.split(filepath)
        print(filepath, ' --- ', filename)
        if not filename.endswith('.md'):
            return 0, None
        imgPath = os.path.join(filepath, IMG_FOLDER)
        os.makedirs(imgPath, exist_ok=True)
        return 1, (filepath, filename, imgPath)

    @classmethod
    def handle(cls, ofile):
        ret, info = cls.preHandle(ofile)
        if ret == -1:
            showinfo('文件不存在', "文件不存在: " + ofile)
            return ret
        elif ret == 0:
            showinfo('文件类型', "文件类型只支持 *.md")
            return ret
        mdPath, mdName, imgPath = info[0], info[1], info[2]
        newMdFilename = os.path.join(mdPath, mdName[:-3] + '_loc' + mdName[-3:])
        if os.path.exists(newMdFilename):
            flag = messagebox.askyesno('是否覆盖', '是否覆盖:\n' + newMdFilename)
            if not flag:
                return 0

        newMdFile = open(newMdFilename, 'w', encoding='utf-8')
        imgIdx = 0
        with open(ofile, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                tagImgUrls = ComUtil.idUrls(line)
                if len(tagImgUrls) == 0:
                    newMdFile.write(line + '\n')
                else:
                    for tagImgUrl in tagImgUrls:
                        imgUrl = ComUtil.getMdImgUrl(tagImgUrl)
                        try:
                            imgIdx += 1
                            tFilename = mdName[:-3] + "_" + str(imgIdx) + cls._guestImgExt(imgUrl)
                            imgFile = os.path.join(imgPath, tFilename)
                            # 应该考虑多线程，多线程中的顺序执行
                            urlretrieve(imgUrl, imgFile)
                            idx = tagImgUrl.find(']')
                            newMdFile.write(tagImgUrl[:idx + 1] + '(%s\%s)\n' % (IMG_FOLDER, tFilename))
                        except:
                            print('Warning download: ', imgUrl)
                            newMdFile.write(line + '\n')
        newMdFile.close()
        print('成功生成: ', newMdFilename)

        return ret

    @classmethod
    def _guestImgExt(cls, url: str):
        u = url.lower()
        extLst = ['jpg', 'png', 'jpeg', 'bmp', 'gif']
        for i in extLst:
            ext = '.' + i
            if u.find(ext) > 0:
                return ext
        for i in extLst:
            if u.find(i) > 0:
                return '.' + i
        return '.jpg'


class ComUtil:
    RE_MD_IMG_TAG = r'!\[[\w\ ]*\]\(https?://(?:[-\w./?=&,]|(?:%[\da-fA-F]{2}))+\)'
    RE_MD_IMG_URL = r'!\[[\w\ ]*\]\((https?://(?:[-\w./?=&,]|(?:%[\da-fA-F]{2}))+)\)'

    @classmethod
    def idUrls(cls, line):
        return re.findall(cls.RE_MD_IMG_TAG, line)

    @classmethod
    def getMdImgUrl(cls, tagImg):
        match = re.match(cls.RE_MD_IMG_URL, tagImg)
        return match.groups()[0]


def testRe():
    s0 = '![图片](https://mmbiz.qpic.cn/mmbiz_png/UGxk62Z8n3T6DWibuAr3z1IklcicS2icI0IZMxUEcfxqvMNqIgbG9TG4f4QCNhBN6CLVS1QhnJM718uOIqFm0nGEg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)![22](http://aaa)'
    s1 = '![图片](https://mmbiz.qp'
    s2 = '![图片](https://mmbiz.qpic.cn/mmbiz_png/UGxk62Z8n3T6DWibuAr3z1IklcicS2icI0I4M8htdCUkllB0dUsEcpQNicPEQg706uJZib5MywV50rTXeYUL8Snsnsw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)'
    r0 = ComUtil.idUrls(s0)
    r1 = ComUtil.idUrls(s1)
    r2 = ComUtil.idUrls(s2)
    # print(r0)
    # print(r1)
    # print(r2)
    for u in r0:
        print(ComUtil.getMdImgUrl(u))
    for u in r2:
        print(ComUtil.getMdImgUrl(u))


if __name__ == '__main__1':
    testRe()

if __name__ == '__main__':
    tk = tkinter.Tk()
    windnd.hook_dropfiles(tk, func=draggedFiles)
    view = TkView(tk)
    view.init()
    tk.mainloop()
