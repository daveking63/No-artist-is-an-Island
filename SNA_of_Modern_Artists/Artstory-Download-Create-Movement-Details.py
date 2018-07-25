from bs4 import BeautifulSoup
import re
import pprint
from os import listdir
from os.path import isfile, join
import unicodedata
from urllib.request import urlopen

def download(urlPage):
    src = None
    try:
        #req = url.request.Request(urlPage)
        src = urlopen(urlPage)
        html = src.read()
    finally:
        if src:
            src.close() 
    return html

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

def createListofHTMLFiles(fPath,fname):
    fileName = fPath + fname
    with open(fileName) as f:
        htmlListing = f.read()  
        f.close()
    htmlFiles = htmlListing.split('\n')
    return htmlFiles

def retrieveAndStoreHTMLsLocal(path,htmlList,start):  
    cnt = 0
    for moveHtml in htmlList[start:len(htmlList)]:
        artStoryPrefix = "https://www.theartstory.org/"
        moveHtmlLong = artStoryPrefix + moveHtml
        movePage = download(moveHtmlLong)
        if movePage == None:
            print(cnt, "Missing", moveHtml)
        else:
            moveFile = path + moveHtml   
            fOpen = open(moveFile, 'wb')
            fOpen.write(movePage)
            fOpen.close()
            print(cnt, "Found", moveFile)
        cnt += 1

def createFileOfMovementDetails(movePath, moveFiles,dPath,dFile):
    detailFile = dPath + dFile
    fOpen = open(detailFile,'w')
    mCnt = 0
    lf = '\n'
    for moveFile in moveFiles[0:]:
        print('####')
        moveMark = '####' + lf
        fOpen.write(moveMark)
        #
        moveFile = movePath + moveFile
        with open(moveFile, encoding='utf-8') as f:
            data = f.read()  
            f.close()
        soup = BeautifulSoup(data, 'html.parser')
        # retrieve movement name
        moveName = soup.find("title")
        moveNameTmp = moveName.get_text()
        moveStrt = moveNameTmp.find('Movement')
        moveNameTemp = moveNameTmp[0:moveStrt-1]
        moveNameTxt = remove_accents(moveNameTemp)
        print('0-', moveNameTxt)
        mNStr = '0-' + moveNameTxt.decode("utf-8") + lf
        fOpen.write(mNStr)
        # setup ID number which is current movement count
        print('1-', mCnt)
        mCntStr = '1-' + str(mCnt) + lf        
        fOpen.write(mCntStr)
        # movement file in c:/
        print('2-',moveFile) 
        mFStr = '2-' + moveFile + lf
        fOpen.write(mFStr)
        # setup start and end years for movement -- number of "wacky" formats involved
        moveYears = soup.find("div", class_="years-holder box-movement")
        tmpParags = moveYears.find_all("p")
        yrsParags = []
        for x in tmpParags:
            yrsParags.append(str(x))        
        pNum = 0
        # start year
        startParag = yrsParags[0]
        locEnd = startParag.find('</p>')
        startTxt = startParag[25:locEnd - 1]
        moveYrStart = startTxt[0:4] #default value for 0000, 0000s, 0000's
        if startTxt.find('c.') > -1:
            moveYrStart = startTxt[2:6]                      
        elif startTxt.find('Early') > -1:
            moveYrStart = startTxt[6:9] + '0'              
        elif startTxt.find('Mid') > -1:
            moveYrStart = startTxt[4:7] + '5'
        elif startTxt.find('Late') > -1:
            moveYrStart = startTxt[5:8] + '9'
        elif startTxt.find('Origins') > -1:
            moveYrStart = '1960'
        elif startTxt.find('Current') > -1:
            moveYrStart = '2020'
        print('3-', moveYrStart)
        mSYrStr = '3-' + moveYrStart + lf
        fOpen.write(mSYrStr)
        # end year
        if len(yrsParags) == 2:
            endParag = yrsParags[1]
            endParag = endParag.replace('\t','')
            locEnd = endParag.find('</p>')
            endTxt = endParag[24:locEnd]
            moveYrEnd = endTxt[0:4] #default value for 0000, 0000s, 0000's
            if endTxt.find('c.') > -1:
                moveYrEnd = endTxt[2:6]                      
            elif endTxt.find('Early') > -1:
                moveYrEnd = endTxt[6:9] + '0'              
            elif endTxt.find('Mid') > -1:
                moveYrEnd = endTxt[4:7] + '5'
            elif endTxt.find('Late') > -1:
                moveYrEnd = endTxt[5:8] + '9'  
            elif endTxt.find('Current') > -1:
                moveYrEnd = '2020'
        else:
            moveYrEnd = '2020'
        print('4-', moveYrEnd)
        mEYrStr = '4-' + str(moveYrEnd) + lf
        fOpen.write(mEYrStr)
        moveArtistGroup = soup.find("div", class_="keyartists-box")
        #print(moveArtistGroup)
        aCnt = 0
        aHrefCnt = 0
        if moveArtistGroup == None:
            artistName = "No Key Artists"
            print('5-', artistName)
            aNameStr = '5-' + artistName + lf
            fOpen.write(aNameStr)
            artistLink = "No Key HREFs"
            print('6-', artistLink)
            aLinkStr = '6-' + artistLink + lf
            fOpen.write(aLinkStr)
        if moveArtistGroup != None:
            artistMoveTableCells = moveArtistGroup.find_all("td", class_="table-desc small-table-desc")
            for tableCell in artistMoveTableCells:
                aMSpanTxt = tableCell.find('span').get_text(strip=True)
                artistName = remove_accents(aMSpanTxt)
                print('5-', artistName)
                aNameStr = '5-' + artistName.decode("utf-8") + lf
                fOpen.write(aNameStr)
                aCnt += 1
            artistMoveHref = moveArtistGroup.find_all("a", class_="detail-view-link")
            for aHref in artistMoveHref:
                aHrefTmp = str(aHref)
                aHrefStrt = aHrefTmp.find('href=') + 6
                aHrefEnd = aHrefTmp.find('">')
                aHrefType = aHrefTmp.find('artist')
                aHrefTxt = aHrefTmp[aHrefStrt:aHrefEnd]
                artistLink = remove_accents(aHrefTxt)
                print('6-', artistLink)
                aLinkStr = '6-' + artistLink.decode("utf-8") + lf
                fOpen.write(aLinkStr)
                aHrefCnt += 1
        fOpen.write(moveMark)
        if aCnt != aHrefCnt:
            print('**** Mismatch ', aCnt, aHrefCnt)
        mCnt += 1
    fOpen.close()   
        
# Main

# create a list of ArtStory.Org movement HTML pages to download
path = 'C:/Research/artstory/'
fileName = 'Artstory-Movements-HTM-Links-July-2018.txt'
movementHTMLs = createListofHTMLFiles(path,fileName)

# use list - movementHTMLs -  to download movement HTML pages from Artstory.org
# and store locally in directory movePath
movePath = 'C:/Research/artstory/Artstory-Movements-July-2018/'
retrieveAndStoreHTMLsLocal(movePath,movementHTMLs,0)

detailPath = 'C:/research/artstory/'
tempDetailFile = 'ArtStory-Movements-Details-July-2018.txt'
moveFiles = listdir(movePath)
createFileOfMovementDetails(movePath, moveFiles,detailPath,tempDetailFile)