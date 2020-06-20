# Developer: Afaq Ahmad
# Email: afaq.ahmad100@gmail.com
import selenium
import sys
import re
import time
import getopt
import datetime
import io

import csv
import json

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sqlite3
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

reload(sys)
sys.setdefaultencoding('utf-8')

class Test( QtGui.QWidget ):

    def __init__( self, database, parent=None):
        super( Test, self ).__init__( parent )
        
        self.db = database
        
        layout1 = QHBoxLayout()
        
        layout2 = QHBoxLayout()
        self.lbl1 = QtGui.QLabel("Recently in hours")
        self.lbl2 = QtGui.QLabel("Blog counts limit")
        self.te1 = QtGui.QLineEdit()
        self.te1.setPlaceholderText("hour limit")
        self.te2 = QtGui.QLineEdit()
        self.te2.setPlaceholderText("blog limit")
        layout2.addWidget(self.lbl1)
        layout2.addWidget(self.te1)
        layout2.addWidget(self.lbl2)
        layout2.addWidget(self.te2)



        self.setFixedSize(400,120)
        self.cb = QtGui.QComboBox()
        self.cb.setEditable(True)
        
        self.btn = QtGui.QPushButton("Search")
        self.btn.clicked.connect(lambda:self.search())
        
#        layout1.addWidget(self.cb, 1)
        layout1.addWidget(self.btn)
        
        layout = QVBoxLayout()
        layout.addLayout(layout2, 1)
        layout.addLayout(layout1, 2)
        
        self.setLayout(layout)
        self.setWindowTitle("Twitter Helper")
        self.show()
        
        keywords = self.db.getkeywords()
        for x in xrange(len(keywords)):
            self.cb.addItem(keywords[x])
        

    def search(self):
        if self.db.isexist(self.cb.currentText()) == False:
            self.db.insertkeyword(self.cb.currentText())
            self.cb.addItem(self.cb.currentText())
        st = ScrapeTwitter(self.te1.text(), self.te2.text())
        
        keywords = []
        f = open('input.txt')
        if f is not None:
            line = f.readline()

            while line:
                keywords = keywords + [line]
                line = f.readline()
            f.close()
            st.scrapeall(keywords)
            QMessageBox.information(self, "Complete", "Scraping Complete");
        else:
            QMessageBox.information(self, "No Input", "Please check input file");
        
        
 
class DBManager(object):
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='keywords'"
        self.cursor = self.conn.cursor()
        if not self.cursor.execute(query).fetchone():
            self.createtable()
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        
    def createtable(self):
        query = "CREATE TABLE keywords (id INTEGER PRIMARY KEY, keyword text)"
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        defvals = [("Dermira"), ("Cimzia"), ("DRM04"), ("DRM01"), ("Aclaris"), ("Aclaris Therapeutics"), ("A-101"), ("ATI-50001"), ("ATI-50002"), ("ATI-50003"), ("Otonomy"), ("Otiprio"), ("OTO-104"), ("OTO-311"), ("OTO-4XX"), ("dexamethasone"), ("gacyclidine"), ("AVERTS-1"), ("AVERTS-2"), ("ACImmune"), ("crenezumab"), ("ACI-24"), ("ACI-35"), ("Morphomer Tau"), ("Argos Therapeutics"), ("Argos"), ("AGS-003"), ("sunitinib"), ("AGS-004"), ("Marinus Pharmaceuticals"), ("Marinus Pharma"), ("Marinus"), ("Ganaxolone"), ("PTC therapeutics"), ("Ptcbio"), ("PTC"), ("ataluren"), ("Intracellular Therapies"), ("Intra-Cellular Therapies"), ("ITI-007"), ("ITI-002"), ("ITI-214"), ("Alexion"), ("Alexion Pharmaceuticals"), ("Alexion Pharma"), ("Soliris"), ("eculizumab"), ("ALXN1210"), ("ALXN1101"), ("SBC-103"), ("Samalizumab"), ("ALXN6000"), ("REGAIN Study"), ("REGAIN Trial"), ("PREVENT Study"), ("PREVENT Trial"), ("Clovis Oncology"), ("Clovis"), ("Rucaparib"), ("ARIEL3"), ("ARIEL4"), ("TRITON2"), ("TRITON3"), ("RIO Study"), ("RIO Trial"), ("PLATFORM Study"), ("PLATFORM Trial"), ("MITO-25"), ("Atezolizumab"), ("STRAT-STAMPEDE"), ("Atara Biotherapeutics"), ("Atara Bio"), ("Atara"), ("EBV-CTL"), ("CMV-CTL"), ("WT1-CTL"), ("STM434"), ("Immunomedics"), ("Epratuzumab"), ("Sacituzumab govitecan"), ("IMU-132"), ("Labetuzumab govetican"), ("IMMU-130"), ("Veltuzumab"), ("Milatuzumab"), ("IMMU-114"), ("Reata Pharmaceuticals"), ("Reata Pharma"), ("Reata"), ("Bardoxolone Methyl"), ("Omaveloxolone"), ("Esperion"), ("Bempedoic Acid"), ("Ezetimibe"), ("CLEAR Study"), ("CLEAR Trial"), ("Zogenix"), ("ZX008"), ("Relday"), ("Dravet Syndrome"), ("Sage Therapeutics"), ("Sagerx"), ("STATUS Trial"), ("PPD-202"), ("SAGE-547"), ("Aerie Pharmaceuticals"), ("Aerie Pharma"), ("Rhopressa"), ("Roclatan"), ("ROCKET 1 Study"), ("ROCKET 1 Trial"), ("ROCKET 2 Study"), ("ROCKET 2 Trial"), ("ROCKET 3 Study"), ("ROCKET 3 Trial"), ("Ignyta"), ("Ignyta Inc"), ("Entrectinib"), ("RXDX-105"), ("Taladegib"), ("RXDX-106"), ("STARTRK"), ("STARTRK Trial"), ("STARTRK Study"), ("Eiger biopharmaceuticals"), ("Eiger Bio"), ("Eiger Biopharma"), ("Sarasar"), ("Ionafarnib"), ("Pegylated Interferon Lambda"), ("Exendin 9-39"), ("Ubenimex"), ("Insmed"), ("ARIKAYCE"), ("INS1009"), ("Sunesis"), ("Sunesis Pharmaceuticals"), ("Sunesis Pharma"), ("Vosaroxin"), ("Valor Trial"), ("VALOR Study"), ("TAK-580"), ("SNS-062"), ("SNS-229"), ("QINPREZO"), ("Axovant Sciences"), ("Axovant"), ("Intepirdine"), ("RVT-101"), ("Nelotanserin"), ("RVT-102"), ("RVT-103"), ("RVT-104"), ("MINDSET Study"), ("MINDSET Trial"), ("HEADWAY Study"), ("HEADWAY Trial"), ("Xenon Pharmaceuticals"), ("Xenon Pharma"), ("Glybera"), ("XEN801"), ("Stemline Therapeutics"), ("SL-401"), ("SL-701"), ("SL-801"), ("Selecta Biosciences"), ("Acceleron Pharma"), ("Acceleron"), ("Luspatercept"), ("Sotatercept"), ("Dalantercept"), ("ACE-083"), ("ACE-2494")]
        for keyword in defvals:
            self.insertkeyword(keyword)
        
    def insertkeyword(self,keyword):
        query = "INSERT INTO keywords (keyword) VALUES ('" + str(keyword) + "')"
        self.cursor.execute(query)
        self.conn.commit()
        
    def isexist(self,keyword):
        query = "SELECT id FROM keywords WHERE keyword='" + str(keyword) + "'"
        if not self.cursor.execute(query).fetchone():
            return False
        else:
            return True
        
    def getkeywords(self):
        query = "SELECT keyword FROM keywords"
        rows = self.cursor.execute(query)
        result = {}
        _count = 0
        for row in rows:
            result[_count] = row[0]
            _count = _count + 1
        return result
        
class ScrapeTwitter(object):
    def __init__(self, hlimits, blimits):
        
        _blimits = str(blimits)
        if _blimits == "":
            self.blimit = 20
        else:
            self.blimit = int(_blimits)
        
        _hlimits = str(hlimits)
        if _hlimits == "":
            _hlimits = "5h"
        
        if "h" in _hlimits:
            _hlimits = _hlimits.replace("h", "")
            self.hlimits = int(_hlimits) * 60 * 60
        elif "m" in _hlimits:
            _hlimits = _hlimits.replace("m", "")
            self.hlimits = int(_hlimits) * 60
        elif "s" in _hlimits:
            _hlimits = _hlimits.replace("s", "")
            self.hlimits = int(_hlimits)
        else:
            self.hlimits = int(_hlimits) * 60 * 60
            
        # seconds since epoch
        self.hlimits = ((int)((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds())) - self.hlimits
    
    def scrapeall(self, keywords):
        self.browser = webdriver.Chrome()
        strheader = "Author, Author Link, Content, CardLink, Image/Video, Date Tiem\n"
        self.outfile = io.open('data.csv', 'w',encoding='utf8')
        self.outfile.write(unicode(strheader))
        for keyword in keywords:
            print keyword
            self.scrapenow(keyword)
        self.outfile.close()
        self.browser.close()

    
    def scrapenow(self, keyword):
        self.url = "https://twitter.com/search?f=tweets&vertical=default&q="
        self.url = self.url + keyword
        self.pause = 3
        self.browser.get(str(self.url))
        time.sleep(2)

        blogs = None
        i = 0
        pause = 1

        lastHeight = self.browser.execute_script("return document.body.scrollHeight")
#        self.browser.get_screenshot_as_file("test03_1_"+str(i)+".jpg")
        while True:
            # find elements
            blogs = self.browser.find_elements_by_css_selector(".js-stream-item.stream-item.stream-item")

            # first size compare break
            if len(blogs) >= self.blimit:
                break

                # second last element's time compare break
            if len(blogs) == 0:
                break
            lastblog = blogs[-1]
            _timeblogs = lastblog.find_element_by_css_selector(".tweet-timestamp.js-permalink.js-nav.js-tooltip")
            _timeblog = _timeblogs.find_element_by_tag_name("span")
            _timedata = _timeblog.get_attribute("data-time") #_timedata = seconds since epoch
            if ((int)(_timedata)) <= ((int)(self.hlimits)):
                break
            
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.pause)
            newHeight = self.browser.execute_script("return document.body.scrollHeight")
            lastHeight = newHeight
            i += 1
#            self.browser.get_screenshot_as_file("test03_1_"+str(i)+".jpg")
        
        time.sleep(self.pause*2)
        
        _count = 0
        
        blogs = self.browser.find_elements_by_css_selector(".js-stream-item.stream-item.stream-item")
        
        for blog in blogs:
            _jitem = {}
            _timeblogs = blog.find_element_by_css_selector("a[class='tweet-timestamp js-permalink js-nav js-tooltip']")
            _timeblog = _timeblogs.find_element_by_tag_name("span")
            _timedata = _timeblog.get_attribute("data-time")
            if ((int)(_timedata)) < ((int)(self.hlimits)):
                break
            
            _bauthor = blog.find_element_by_css_selector("span[class='FullNameGroup']")
            #text and then link
            _jitem[0] = str(_bauthor.text)
            _jitem[0] = _jitem[0].replace(","," ")
            _jitem[0] = _jitem[0].replace("\n"," ")
            
            _bauthorurlspan = _bauthor.find_element_by_xpath('..')
            _bauthorurl = _bauthorurlspan.get_attribute('href')
            _jitem[1] = str(_bauthorurl)
            _jitem[1] = _jitem[1].replace(","," ")
            _jitem[1] = _jitem[1].replace("\n"," ")
            
            _bcontent = blog.find_element_by_css_selector(".TweetTextSize.js-tweet-text.tweet-text")#text
            _jitem[2] = str(_bcontent.text)
            _jitem[2] = _jitem[2].replace(","," ")
            _jitem[2] = _jitem[2].replace("\n"," ")
            
            try:
                _blink = blog.find_element_by_tag_name("iframe")
                _jitem[3] = str(_blink.get_attribute('src'))
            except:
                _jitem[3] = " "
            _jitem[3] = _jitem[3].replace(","," ")
            _jitem[3] = _jitem[3].replace("\n"," ")
            
            try:
                _imagediv = blog.find_element_by_css_selector("div[class='AdaptiveMedia-container']")
                _image = _imagediv.find_element_by_tag_name("img")#src
                _jitem[4] = str(_image.get_attribute('src'))
            except:
                _jitem[4] = " "
            _jitem[4] = _jitem[4].replace(","," ")
            _jitem[4] = _jitem[4].replace("\n"," ")
            
            _jitem[5] = datetime.datetime.fromtimestamp(((float)(_timedata))).strftime("%Y-%m-%d %H:%M:%S")
            _jitem[5] = _jitem[5].replace(","," ")
            _jitem[5] = _jitem[5].replace("\n"," ")
            
            _count = _count + 1;
            if _count > self.blimit:
                break
            strc = _jitem[0] + ", " + _jitem[1] + ", " + _jitem[2] + ", " + _jitem[3] + ", " + _jitem[4] + ", " + _jitem[5] + "\n"
            self.outfile.write(unicode(strc))

   
if __name__ == '__main__':
    app = QtGui.QApplication( sys.argv )
    db = DBManager("keywords.db")
    mainW = Test(db)
    sys.exit( app.exec_() )