# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 13:33:55 2018

@author: nilesh
"""
from collections import OrderedDict
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import urllib
import csv
k=1;

#Importing movie data
moviesList_file = pd.read_excel('MovieData.xls', sheetname='Sheet1')
movie=moviesList_file['title'][0]
titletag=moviesList_file['position'][0]
home_url = 'http://www.imdb.com/title/' + urllib.parse.quote(titletag)+"/releaseinfo?ref_=tt_ov_inf"
html = urllib.request.urlopen(home_url).read()
soup_sub_html=BeautifulSoup(html,'html.parser')
releaseDatesTable = soup_sub_html.find('table',attrs={'class':'subpage_data spFirst'})


#Program Variables
datarow=0
releaseDatesHrefTags=[]
releaseDatesHrefTagsIds=[]
datarow1=0
globalreleaseDatesHrefTags=[]
globalreleaseDatesHrefTagsIds=[]

#Non-USA and USA ReleaseDates Info
for row in releaseDatesTable.find_all('tr'):
    column_marker = 0
    columns = row.find('td').find('a')['href']
    if '/calendar/?region=us' in columns:
        releaseDatesHrefTags.append(columns)
        globalreleaseDatesHrefTags.append(columns)
        releaseDatesHrefTagsIds.append(int(columns.split('ttrel_rel_')[1]))
        
        datarow+=1  
    if not '/calendar/?region=us' in columns:
        globalreleaseDatesHrefTags.append(columns)
        globalreleaseDatesHrefTagsIds.append(int(columns.split('ttrel_rel_')[1]))
        datarow1+=1

################## USA Only Information ##############################################
######################################################################################        
usRel = None
premiereDatesDict={}
premiereDatesDict1={}
filmFestivalDatesDict={}
filmFestivalDatesDict1={}

for item in releaseDatesHrefTags:
    releaseDatesHrefFinalTag=item
    usaGeneral = soup_sub_html.find('table',attrs={'class':'subpage_data spFirst'}).find('a',href=releaseDatesHrefFinalTag).text
    #print(usaGeneral)
    premFest=soup_sub_html.find('table',attrs={'class':'subpage_data spFirst'}).find('a',href=releaseDatesHrefFinalTag).parent.find_next_sibling().find_next_sibling().text
    releaseDate= soup_sub_html.find('table',attrs={'class':'subpage_data spFirst'}).find('a',href=releaseDatesHrefFinalTag).parent.find_next_sibling().text
    #USA release Date
    #print(releaseDate)
    #Premiere/Festival
    #print(premFest)
    
    if premFest =='':
        #String to date conversion
        if datetime.strptime(releaseDate, '%d %B %Y').date():
            toDate=datetime.strptime(releaseDate, '%d %B %Y').date()
        elif datetime.strptime(releaseDate, '%B %Y').date():
            toDate=datetime.strptime(releaseDate, '%B %Y').date()
        #Date to String conversion
        toStr= datetime.strftime(toDate, '%m/%d/%Y')
        usRel=toStr
    try:
        if datetime.strptime(releaseDate, '%d %B %Y').date():
            datetime_object = datetime.strptime(releaseDate, '%d %B %Y').date()
        elif datetime.strptime(releaseDate, '%B %Y').date():
            datetime_object = datetime.strptime(releaseDate, '%B %Y').date()    
    except:
        continue
    if 'premiere' in premFest:
        if datetime_object not in premiereDatesDict:
            countryWithPremiere=usaGeneral +':'+ premFest 
            premiereDatesDict.update({datetime_object:countryWithPremiere})
    if ('Festival' in premFest or 'fest' in premFest ):
        if datetime_object not in filmFestivalDatesDict:
            countryWithPremiere=usaGeneral +':'+ premFest 
            filmFestivalDatesDict.update({datetime_object:countryWithPremiere})
    

########### USA General Release
#print(usRel)    
########### USA Premiere Start                

sortedPremiereDatesDict1 = OrderedDict(sorted(premiereDatesDict.items(), key=lambda t: t[0]))
#Sorted Dictionary
#print(sortedPremiereDatesDict1)
#First Premiere Name
if len(sortedPremiereDatesDict1) == 0:
    usaFirstPremiereRawName=None
    usaFirstPremiereName=usaFirstPremiereRawName
    usaFirstPremiereDate=None
else:
    usaFirstPremiereRawName=list(sortedPremiereDatesDict1.items())[0][1]
    usaFirstPremiereName=usaFirstPremiereRawName.replace('(','').replace(')','').replace('\n',' ').strip()
    usaFirstPremiereDate= datetime.strftime(list(sortedPremiereDatesDict1.items())[0][0], '%m/%d/%Y')

#print(usaFirstPremiereName)
#First Premiere Date
#print(usaFirstPremiereDate)

########################################    USA Premiere End
########################################    USA Film Festival Start

#print(filmFestivalDatesDict)
#premiereDatesDict={'12 May 2005':'pre','10 May 2005':'preed','1 May 2005':'aasa'}    
filmFestivalDatesDict1=OrderedDict(sorted(filmFestivalDatesDict.items(), key=lambda t: t[0]))
#Sorted Dictionary
#print(filmFestivalDatesDict1)
#First Film Festival Name
if len(filmFestivalDatesDict1) == 0:
    usaFirstFilmFestivalRawName=None
    usaFirstFilmFestivalName=usaFirstFilmFestivalRawName
    usaFirstFilmFestivalDate=None
else:
    usaFirstFilmFestivalRawName=list(filmFestivalDatesDict1.items())[0][1]
    usaFirstFilmFestivalName=usaFirstFilmFestivalRawName.replace('(','').replace(')','').replace('\n',' ').strip()
    usaFirstFilmFestivalDate= datetime.strftime(list(filmFestivalDatesDict1.items())[0][0], '%m/%d/%Y')
#print(usaFirstFilmFestivalName)
#First Film Festival Date
#print(usaFirstFilmFestivalDate)

########################################    USA Film Festival End
################## USA Only Information End ##########################################

############################ Global Release ########################################## 
######################################################################################

globalRelDict={}
globalRelDict1={}
globalpremiereDatesDict={}
globalpremiereDatesDict1={}
globalfilmFestivalDatesDict={}
globalfilmFestivalDatesDict1={}
globalCountry=None
globalReleaseCountry={}
for item in globalreleaseDatesHrefTags:
    globalreleaseDatesHrefFinalTag=item
    globalCountry = soup_sub_html.find('table',attrs={'class':'subpage_data spFirst'}).find('a',href=globalreleaseDatesHrefFinalTag).text.strip()
    releaseDateGlobal= soup_sub_html.find('table',attrs={'class':'subpage_data spFirst'}).find('a',href=globalreleaseDatesHrefFinalTag).parent.find_next_sibling().text.strip()
    print(globalCountry)
    #print(releaseDateGlobal)
    premFestGlobal=soup_sub_html.find('table',attrs={'class':'subpage_data spFirst'}).find('a',href=globalreleaseDatesHrefFinalTag).parent.find_next_sibling().find_next_sibling().text
    print(premFestGlobal)
    #print(len(premFestGlobal))        
    
    #Premiere/Festival
    #print(premFestGlobal)
    
    
    if ('Festival' not in premFestGlobal and 'fest' not in premFestGlobal and 'premiere' not in premFestGlobal and len(premFestGlobal)==0):
        print('Hii2')
        #String to date conversion
        try:
            if datetime.strptime(releaseDateGlobal, '%d %B %Y').date():
                toDate=datetime.strptime(releaseDateGlobal, '%d %B %Y').date()
            elif datetime.strptime(releaseDateGlobal, '%B %Y').date():
                toDate=datetime.strptime(releaseDateGlobal, '%B %Y').date()
        except:
            continue
        #print(globalCountry)
        #print(toDate)
        if toDate not in globalReleaseCountry:
            globalReleaseCountry.update({toDate:globalCountry})
    
    try:
        if datetime.strptime(releaseDateGlobal, '%d %B %Y').date():
            datetime_object = datetime.strptime(releaseDateGlobal, '%d %B %Y').date()
        elif datetime.strptime(releaseDateGlobal, '%B %Y').date():
            datetime_object = datetime.strptime(releaseDateGlobal, '%B %Y').date()    
    except:
        continue
    if ('premiere' in premFestGlobal and 'USA' not in globalCountry):
        if datetime_object not in globalpremiereDatesDict:
            countryWithPremiere=globalCountry +':'+ premFestGlobal 
            globalpremiereDatesDict.update({datetime_object:countryWithPremiere})
    if (('Festival' in premFestGlobal or 'fest' in premFestGlobal )and 'USA' not in globalCountry):
        if datetime_object not in globalpremiereDatesDict:
            countryWithPremiere=globalCountry +':'+ premFestGlobal 
            globalfilmFestivalDatesDict.update({datetime_object:countryWithPremiere})

########### Global Release Country
globalRelCountrySorted = OrderedDict(sorted(globalReleaseCountry.items(), key=lambda t: t[0]))

if len(globalRelCountrySorted) == 0:
    globalRelCountryDate=None
    globalRelCountry=None
else:
    globalRelCountryDate= datetime.strftime(list(globalRelCountrySorted.items())[0][0], '%m/%d/%Y')
    globalRelCountry=(list(globalRelCountrySorted.items()))[0][1].replace(')','').replace('(','').replace('\n',' ').strip()

print(globalRelCountryDate)
print(globalRelCountry)

#Another way to sort
#sorted(globalRelDict, key=lambda d: map(int, d.split(' ')))

#First Global Premiere Name
globalpremiereDatesDictSorted = OrderedDict(sorted(globalpremiereDatesDict.items(), key=lambda t: t[0]))

if len(globalpremiereDatesDictSorted) == 0:
    globalFirstPremiereName=None
    globalFirstPremiereDate=None
else:
    globalFirstPremiereName=(list(globalpremiereDatesDictSorted.items()))[0][1].replace(')','').replace('(','').replace('\n',' ').strip()
    globalFirstPremiereDate= datetime.strftime(list(globalpremiereDatesDictSorted.items())[0][0], '%m/%d/%Y')
#print(globalFirstPremiereName)
#First Global Premiere Date
#print(globalFirstPremiereDate)
########################################    Global Premiere End

########################################    Global Film Festival Start
globalfilmFestivalDatesDictSOrted=OrderedDict(sorted(globalfilmFestivalDatesDict.items(), key=lambda t: t[0]))
#print(globalfilmFestivalDatesDictSOrted)
#First Film Festival Name
if len(globalfilmFestivalDatesDictSOrted) == 0:
    globalFirstFilmFestivalRawName=None
    globalFirstFilmFestivalName=globalFirstFilmFestivalRawName
    globalFirstFilmFestivalDate=None
else:
    globalFirstFilmFestivalRawName=list(globalfilmFestivalDatesDictSOrted.items())[0][1]
    globalFirstFilmFestivalName=globalFirstFilmFestivalRawName.replace('(','').replace(')','').replace('\n',' ').strip()
    globalFirstFilmFestivalDate= datetime.strftime(list(globalfilmFestivalDatesDictSOrted.items())[0][0], '%m/%d/%Y')

#print(globalFirstFilmFestivalName)
#First Film Festival Date
#print(globalFirstFilmFestivalDate)

########################################    Global Film Festival End
################## Global Only Information End ##########################################

    
print(str(k)+" "+ str(movie)+" "+str(usaGeneral)+" "+str(usRel)+" "+str(usaFirstPremiereName)+" "+str(usaFirstPremiereDate)+" "+str(usaFirstFilmFestivalName)+" "+str(usaFirstFilmFestivalDate)+" "+" "+str(globalRelCountry)+" "+str(globalRelCountryDate)+" "+str(globalFirstPremiereName)+" "+str(globalFirstPremiereDate)+" "+str(globalFirstFilmFestivalName)+" "+str(globalFirstFilmFestivalDate)+"\n")
arraylist=[[movie, usaGeneral,usRel,usaFirstPremiereName,usaFirstPremiereDate,usaFirstFilmFestivalName,usaFirstFilmFestivalDate,globalRelCountry,globalRelCountryDate,globalFirstPremiereName,globalFirstPremiereDate,globalFirstFilmFestivalName,globalFirstFilmFestivalDate]]


myFile = open('USARelease.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(arraylist)