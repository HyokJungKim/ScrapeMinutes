# -*- coding: <utf-8> -*-

# ------------------------------------------------------------------------------
#
# News Data Analysis Project
#   Class No. 1: Scrape Fed Minutes
# 
# Authors : Kim, Hyok Jung(Department of Economics, UC Davis)
#
# Date : October 28th, 2017
#
# Note : Code should be in two parts which is very annoying
#
# 
# ------------------------------------------------------------------------------

# Other packages
from bs4 import BeautifulSoup
import requests
import pandas as pd

class Cls_USA: 
    def __init__(self):
        HTML_S = "https://www.federalreserve.gov/monetarypolicy/fomchistorical"
        HTML_E = ".htm"
        self.ListHTML = [HTML_S + str(i) + HTML_E for i in range(1993,2014)]

        self.BaseURL = "https://www.federalreserve.gov"


    def ConnectURL(self, URL):
        while True:
            URLobj = requests.Session().get(URL)
            if URLobj.status_code == 200:
                break

        soup = BeautifulSoup(URLobj.content, 'lxml')

        return soup

    def getDates(self, inText):
        DictMonth = {'January':'01',
                 'February':'02',
                 'March':'03',
                 'April':'04',
                 'May':'05',
                 'June':'06',
                 'July':'07',
                 'August':'08',
                 'September':'09',
                 'October':'10',
                 'November':'11',
                 'December':'12'}

        OutYear = inText[-4:]

        SplittedDate = inText.split()

        OutMonth = DictMonth[SplittedDate[0]]

        if SplittedDate[1].find("-") == -1:
            OutDay = SplittedDate[1]
        else:
            OutDay = SplittedDate[1].split("-")[0]

        return OutYear, OutMonth, OutDay

    def replaceIrrelevant(self, inText):
        inText = inText

        ListIrrelevant = {"\xa0":"", "\n":"", "\r":""}

        for i in ListIrrelevant:
            inText = inText.replace(i, ListIrrelevant[i])

        return inText

    def MainGetData(self):
        ListYear = []
        ListMonth = []
        ListDay = []
        ListURL = []

        for ii in self.ListHTML:
            soup = self.ConnectURL(ii)

            Panels = soup.find_all(name="div",
                                   attrs={"class":"panel panel-default"})
            for jj in Panels:
                Tabs = jj.find_all(name="div", attrs={"class":"col-xs-12 col-md-6"})

                if len(Tabs) != 0:
                    TextDate = jj.find(name="h5").text

                    [yy, mm, dd] = self.getDates(TextDate)

                    ListYear.append(yy)
                    ListMonth.append(mm)
                    ListDay.append(dd)

                    paragraphs = Tabs[1].find_all("p")

                    for kk in paragraphs:
                        if "Minutes" in kk.text:
                            if kk.a['href'][0:4] == 'http':
                                ListURL.append(kk.a['href'])
                            else:
                                ListURL.append(self.BaseURL + kk.a['href'])

            print(ii, ' complete')

        listAll = []

        for ii in ListURL:
            soup = self.ConnectURL(ii)

            for jj in soup.find_all("p"):
                FilteredText = self.replaceIrrelevant(jj.text)

                listAll.append([ListYear[ListURL.index(ii)],
                                ListMonth[ListURL.index(ii)],
                                ListDay[ListURL.index(ii)],
                                FilteredText])

            print(ListURL.index(ii), " / ", len(ListURL))

        PT2HTML = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"

        DictMonth2 = {'Jan':'01',
                      'Feb':'02',
                      'Mar':'03',
                      'Apr':'04',
                      'May':'05',
                      'Jun':'06',
                      'Jul':'07',
                      'Aug':'08',
                      'Sep':'09',
                      'Oct':'10',
                      'Nov':'11',
                      'Dec':'12'}

        soup = self.ConnectURL(PT2HTML)

        ListYear = []
        ListMonth = []
        ListDay = []
        ListURL = []

        YYPanels = soup.find_all(name="div",
                                 attrs={"class":"panel panel-default"})

        for souploop in YYPanels:

            header = souploop.find(name="h4")
            yy = header.text 
            yy = yy[:4]

            WhiteP = souploop.find_all(name="div", 
                                       attrs={"class":"row fomc-meeting"})

            BlackP = souploop.find_all(name="div", 
                                       attrs={"class":"fomc-meeting--shaded row fomc-meeting"})

            for ii in range(0, len(WhiteP)):
                FOMCmeet = WhiteP[ii].find(name="div",
                                           attrs={"class":"col-xs-12 col-md-4 col-lg-4 fomc-meeting__minutes"})
                try:
                    URL = FOMCmeet.find_all(name ="a")[1]
    
                    URL = URL['href']
    
                    if not(URL[0:4] == 'http'):
                        URL = self.BaseURL + URL

                    mm = WhiteP[ii].find(name="div",
                                         attrs={"class":"fomc-meeting__month col-xs-5 col-sm-3 col-md-2"})

                    mm = DictMonth2[mm.text[:3]]

                    dd = WhiteP[ii].find(name="div",
                                         attrs={"class":"fomc-meeting__date col-xs-4 col-sm-9 col-md-10 col-lg-1"})

                    dd = dd.text
                    if "-" in dd:
                        dd = dd.split("-")[0]

                    ListYear.append(yy)
                    ListMonth.append(mm)
                    ListDay.append(dd)
                    ListURL.append(URL)
                except IndexError:
                    pass

                try:
                    FOMCmeet = BlackP[ii].find(name="div",
                                               attrs={"class":"col-xs-12 col-md-4 col-lg-4 fomc-meeting__minutes"})
                except IndexError:
                    continue
    
                try:
                    URL = FOMCmeet.find_all(name ="a")[1]
    
                    URL = URL['href']
    
                    if not(URL[0:4] == 'http'):
                        URL = self.BaseURL + URL

                    mm = BlackP[ii].find(name="div",
                                         attrs={"class":"fomc-meeting--shaded fomc-meeting__month col-xs-5 col-sm-3 col-md-2"})
                                             
                    mm = DictMonth2[mm.text[:3]]

                    dd = BlackP[ii].find(name="div",
                                         attrs={"class":"fomc-meeting__date col-xs-4 col-sm-9 col-md-10 col-lg-1"})

                    dd = dd.text
                    if "-" in dd:
                        dd = dd.split("-")[0]

                    ListYear.append(yy)
                    ListMonth.append(mm)
                    ListDay.append(dd)
                    ListURL.append(URL)
                except IndexError:
                    pass

        listAll2 = []
        for ii in ListURL:
            soup = self.ConnectURL(ii)
            mainArticle = soup.find(name="div", attrs={"id":"article"})

            for jj in mainArticle.find_all("p"):
                FilteredText = self.replaceIrrelevant(jj.text)
        
                listAll2.append([ListYear[ListURL.index(ii)],
                                 ListMonth[ListURL.index(ii)],
                                 ListDay[ListURL.index(ii)],
                                 FilteredText])
    
            print(ListURL.index(ii), " / ", len(ListURL))

        listAll = listAll + listAll2

        outData = pd.DataFrame(listAll, index=None)
        outData.rename(index=None, inplace=True,
                        columns={0:'Year',1:'Month', 2:'Day', 3:'Paragraph'})

        outData.sort_values(by=['Year','Month','Day'], ascending=True, inplace=True)

        return outData