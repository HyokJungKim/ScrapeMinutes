# -*- coding: <utf-8> -*-

# ------------------------------------------------------------------------------
#
# News Data Analysis Project
#   Class No. 0: Scrape ECB Statements or Minutes
#
# Authors : Kim, Hyok Jung(Department of Economics, UC Davis)
#
# Date : October 27th, 2017
#
# To improve: Main function has been appended, but not checked yet!
#
# ------------------------------------------------------------------------------

# Python standard libraries
import os
import glob
import unidecode

# Other packages
from bs4 import BeautifulSoup
import requests
import pandas as pd

class Cls_ECB: 
    def __init__(self):
        self.ListYears = ["https://www.ecb.europa.eu/press/pressconf/"
                          +str(i)+
                          "/html/index.en.html" for i in range(1998,2019)]
        self.BaseURL = "https://www.ecb.europa.eu"

    # Get list of Dates in the current page
    def getDates(self, ConferenceSection):
        # Fetch Dates for the Press Conferences
        ListData = ConferenceSection.find_all(name='dt')
        ListData = [i.text for i in ListData]

        outListYear = [i[-4:] for i in ListData]
        outListMonth = [i[3:5] for i in ListData]
        outListDay = [i[0:2] for i in ListData]

        return outListYear, outListMonth, outListDay 

    # Get list of English URLs in the current page
    def getEngURLs(self, ConferenceSection):
        # Fetch URLs for English transcript
        EngURLs = ConferenceSection.find_all(name="span", attrs={'class':'offeredLanguage'})

        # Make list of URLs for English transcript
        ListEngURLs = [self.BaseURL + i.find(name='a')['href'] for i in EngURLs]

        return ListEngURLs

    # Fetch text data by paragraphs
    def getEngTranscript(self, TranscriptURL):
        soup = self.ConnectURL(TranscriptURL)

        PressContent = soup.find(name="div", attrs={"class",
                                                    "ecb-pressContent"})

        ListPressContent = PressContent.find_all('p')

        ListPressContent = [i.text for i in ListPressContent]

        return ListPressContent

    def ConnectURL(self, URL):
        while True:
            URLobj = requests.Session().get(URL)
            if URLobj.status_code == 200:
                break

        soup = BeautifulSoup(URLobj.content, 'lxml')

        return soup

    def MainGetData(self):

        ListYear = []
        ListMonth  = []
        ListDay = []
        ListTexts = []

        for i in self.ListYears:
            soup = self.ConnectURL(i)

            ConferenceSection = soup.find(name ='dl', 
                                          attrs={'class':'ecb-basicList'})
            tempYear, tempMonth, tempDay = self.getDates(ConferenceSection)

            ListYear = ListYear + tempYear
            ListMonth = ListMonth + tempMonth
            ListDay = ListDay + tempDay
            
            ListURLs = self.getEngURLs(ConferenceSection)

            for j in ListURLs:
                ListTexts = ListTexts + [self.getEngTranscript(j)]

            print('year '+str(i)+' complete')

        Combined = []
        for ii, jj, kk in zip(ListYear, ListMonth, ListDay):
            for ss in ListTexts[ListYear.index(ii)]:
                ss = unidecode.unidecode(ss)
                ss.replace('\n','')

                Combined.append([ii, jj, kk, ss])

        DataCombined = pd.DataFrame(Combined, index = None)

        DataCombined.rename(index=None, inplace=True,
                             columns={0:'Year', 1:'Month', 2:'Day', 3:'Paragraph'})

        DataCombined.sort_values(by=['Year','Month','Day'], ascending=True, inplace=True)

        return DataCombined