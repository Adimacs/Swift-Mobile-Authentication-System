import wx
from PIL import Image
import pytesseract             # Python interface to tesseract for OCR
import cv2                     # OpenCV computer vision library
import os
import numpy as np
import re
import subprocess
import time
import sys
import requests

DEBUG = True
VIP_dict = {
            "66344234":"Lokeswaran Subramanian",
            "65442242":"Prabhu Sundaram",
            "57486271":"Sundeep Vijaykumar",
            "67457242":"Vijayaraya T V ",
            "79887771":"Anand Patidar",
            "16929245": "Shakthi",
            "93317197":"Bikranth"
            }

fps = 10

class MainWindow(wx.Frame):

    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size = (600,400))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.Connected = False

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)

        hbox51 = wx.BoxSizer(wx.HORIZONTAL)
        self.VipId = wx.StaticText(panel, label="VIP ID:        ")

        hbox52 = wx.BoxSizer(wx.HORIZONTAL)
        self.InpTxtBox3 = wx.TextCtrl(panel, -1, '', size=(350, 25), style=wx.TE_LEFT | wx.TE_PROCESS_ENTER)
        self.InpTxtBox3.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressedBox3)

        hbox53 = wx.BoxSizer(wx.HORIZONTAL)
        btn_Search = wx.Button(panel, -1, "Search", size=(100, 25), style=wx.CENTER)
        btn_Search.Bind(wx.EVT_BUTTON, self.OnClicked_search, btn_Search)

        hbox51.Add(self.VipId, 1, wx.ALIGN_LEFT | wx.ALL, 8)
        hbox52.Add(self.InpTxtBox3, 1, wx.ALIGN_LEFT | wx.ALL, 8)
        hbox53.Add(btn_Search, 1, wx.ALIGN_LEFT | wx.ALL, 8)

        hbox5.Add(hbox51)
        hbox5.Add(hbox52)
        hbox5.Add(hbox53)


        hbox11 = wx.BoxSizer(wx.HORIZONTAL)

        hbox21 = wx.BoxSizer(wx.HORIZONTAL)
        self.IpAddress = wx.StaticText(panel, label = "IP Address: ")

        hbox22 = wx.BoxSizer(wx.HORIZONTAL)
        self.InpTxtBox = wx.TextCtrl(panel, -1, '', size=(350, 25), style=wx.TE_LEFT | wx.TE_PROCESS_ENTER)
        self.InpTxtBox.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)

        hbox23 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(panel,-1,"Connect",size = (100,25),style = wx.CENTER)
        btn.Bind(wx.EVT_BUTTON,self.OnClicked,btn)

        hbox21.Add(self.IpAddress, 1, wx.ALIGN_LEFT | wx.ALL, 8)
        hbox22.Add(self.InpTxtBox, 1, wx.ALIGN_LEFT | wx.ALL, 8)
        hbox23.Add(btn, 1, wx.ALIGN_LEFT | wx.ALL, 8)

        hbox31 = wx.BoxSizer(wx.HORIZONTAL)
        self.InpTxtBox2 = wx.TextCtrl(panel, -1, '', size=(575, 200), style=wx.TE_LEFT | wx.TE_READONLY | wx.TE_MULTILINE)
        #self.Img = wx.Image(".\\Data\\background.bmp",wx.BITMAP_TYPE_ANY)
        #self.imagebox = wx.StaticBitmap(panel,wx.ID_ANY,self.Img.ConvertToBitmap())
        hbox31.Add(self.InpTxtBox2, 1, wx.ALIGN_CENTER | wx.ALL, 8)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox41 = wx.BoxSizer(wx.HORIZONTAL)
        btn2 = wx.Button(panel, -1, "Clear All", size=(300, 40), style=wx.CENTER)
        btn2.Bind(wx.EVT_BUTTON, self.OnClickedbtn2, btn2)

        hbox42 = wx.BoxSizer(wx.HORIZONTAL)
        btn3 = wx.Button(panel, -1, "Quit", size=(300, 40), style=wx.CENTER)
        btn3.Bind(wx.EVT_BUTTON, self.OnExit, btn3)

        hbox41.Add(btn2, 1, wx.ALIGN_CENTER , 8)
        hbox42.Add(btn3, 1, wx.ALIGN_CENTER , 8)

        hbox4.Add(hbox41)
        hbox4.Add(hbox42)

        hbox11.Add(hbox21)
        hbox11.Add(hbox22)
        hbox11.Add(hbox23)

        #hbox1.Add(hbox4)
        vbox.Add(hbox5)
        vbox.Add(hbox11)
        vbox.Add(hbox31)
        vbox.Add(hbox4)



        panel.SetSizer(vbox)

        #self.timer = wx.Timer(self)
        #self.timer.Start(1000. / fps)

        #self.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.Bind(wx.EVT_TIMER, self.NextFrame)
        #self.InpTxtBox2.AppendText("HAI")

        self.CreateStatusBar()
        self.Centre()
        self.Show()
        self.Fit()

    def OnKeyTyped(self, event):
      print event.GetString()

    def OnEnterPressed(self,event):
        self.OnClicked(event)

    def OnClicked(self,event):
        text = self.InpTxtBox.GetValue()
        text = text.strip()
        if len(text) :
            self.IpAddress = text
            if self.IpAddress:
                while True:
                    url = self.IpAddress + ':8080/shot.jpg'
                    imgResp = requests.get(url)
                    imgNp = np.array(bytearray(imgResp.content), dtype=np.uint8)
                    image = cv2.imdecode(imgNp, -1)
                    imsmall = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                    (h, w) = imsmall.shape[:2]
                    center = (w / 2, h / 2)
                    imcropped = imsmall[((h / 2) - 50):((h / 2) + 50), ((w / 2) - 200):((w / 2) + 200)]
                    im = cv2.cvtColor(imcropped, cv2.COLOR_BGR2GRAY)
                    thresh = 180
                    im_bw = cv2.threshold(im, thresh, 255, cv2.THRESH_BINARY)[1]
                    vimages = np.concatenate((im, im_bw), axis=0)
                    cv2.imshow("Webcam_Capture",vimages)
                    if (cv2.waitKey(1) & 0xFF) == ord(' '):
                        cv2.destroyAllWindows()
                        break
                self.detectedtext = pytesseract.image_to_string(im_bw)
                detect_lines = self.detectedtext.splitlines()
                #self.InpTxtBox2.AppendText('checking started' + '\n')
                print(detect_lines)
                for line in detect_lines:
                    #print("started\n")
                    text = line
                    #text = "SYMC 6544 2241"
                    #text =str(text)
                    if len(text) > 11:
                        text = text.strip()
                        text = text.replace(" ", "")
                        #self.InpTxtBox2.AppendText(text+'\n')
                        if len(text) == 12:
                            partial_text1 = text[0:4]
                            partial_text2 = text[4:]
                            if partial_text1.isalpha():
                                if partial_text2.isdigit():
                                    text = text[4:]
                                        #self.InpTxtBox2.AppendText(text)
                                    if text in VIP_dict.keys():
                                        print(VIP_dict[text])
                                        print(text)
                                        Msg = """!!! Authentication PASSED !!!\n""" \
                                                    + "Employee Name: " + VIP_dict[text] +'\n' \
                                                    + "ID Detected: " + text
                                        self.InpTxtBox2.AppendText(str(Msg)+'\n')
                                        wx.MessageBox(str(Msg),"SMAS Authentication",wx.OK | wx.ICON_INFORMATION)
                                        break
                                    else:
                                        Msg = """!!! Authentication Failed !!!\n
                                        Please click OK to register the mobile or click CANCEL to skip the registration"""
                                        wx.MessageBox(str(Msg), "SMAS Authentication", wx.OK | wx.CANCEL )
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue

        else:
            self.IpAddress = ''

    def OnClickedbtn2(self,event):
        self.InpTxtBox2.Clear()

    def OnClicked_search(self, event):
        text = self.InpTxtBox3.GetValue()
        if len(text) > 11:
            text = text.strip()
            text = text.replace(" ", "")
            # self.InpTxtBox2.AppendText(text+'\n')
            if len(text) == 12:
                partial_text1 = text[0:4]
                partial_text2 = text[4:]
                if partial_text1.isalpha():
                    if partial_text2.isdigit():
                        text = text[4:]
                        # self.InpTxtBox2.AppendText(text)
                        if text in VIP_dict.keys():
                            #print(VIP_dict[text])
                            #print(text)
                            Msg = """!!! Authentication PASSED !!!\n""" \
                                  + "Employee Name: " + VIP_dict[text] + '\n' \
                                  + "ID Detected: " + text
                            self.InpTxtBox2.AppendText(str(Msg) + '\n')
                            wx.MessageBox(str(Msg), "SMAS Authentication", wx.OK | wx.ICON_INFORMATION)
                        else:
                            Msg = """!!! Authentication Failed !!!\n
                            Please click OK to register the mobile or click CANCEL to skip the registration"""
                            wx.MessageBox(str(Msg), "SMAS Authentication", wx.OK | wx.CANCEL)
                    else:
                        Msg = """ Input String Not matching the Given criteria"""
                        wx.MessageBox(str(Msg), "SMAS Authentication", wx.OK | wx.ICON_INFORMATION | wx.ICON_INFORMATION)
                else:
                    Msg = """ Input String Not matching the Given criteria"""
                    wx.MessageBox(str(Msg), "SMAS Authentication", wx.OK | wx.ICON_INFORMATION | wx.ICON_INFORMATION)
            else:
                Msg = """ Input String Not matching the Given criteria"""
                wx.MessageBox(str(Msg), "SMAS Authentication", wx.OK | wx.ICON_INFORMATION | wx.ICON_INFORMATION)


    def OnEnterPressedBox3(self,event):
        self.OnClicked_search()


    def OnExit(self,event):
        self.Close(True)



if __name__ == '__main__':
    app = wx.App()
    Frame = MainWindow(None,-1,"Swift Mobile Authentication System")
    Frame.Show()
    app.MainLoop()