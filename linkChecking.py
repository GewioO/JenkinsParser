# file <parser.py>
from bs4 import BeautifulSoup
import requests as req
import re, time

def checkBuildState(path):
    textTime    = ""
    buildResult = "No result"
    path        = path.replace(' ', '')

    try:
        if path.rfind("/") < len(path)-1:
            path = path + "/"

        soup       = BeautifulSoup(req.get(path + "console").text, 'lxml')
        resultFind = str(soup.find_all('pre',{"class": "console-output"}))

        if re.search('Finished: SUCCESS', resultFind) != None:
            textTime    = timestampSearch(soup)
            buildResult = "SUCCESS"
        elif re.search('Finished: FAILURE', resultFind) != None:
            textTime    = timestampSearch(soup)
            buildResult = "FAILURE"

        if buildResult == "No result":
            soup = BeautifulSoup(req.get(path).text, 'lxml')

            if re.search(r'In progress',str(soup.find_all("div"))) != None:
                return "in process.", ""
            else:
                return False, ""
    except AttributeError:
        return "Something wrong with your link, maybe your build does not exist, please, check it.", ""
    except BaseException:
        return "Something wrong with your link, please, check it.", ""

    return str(buildResult), str(textTime)
    

def realTimeCheck(path, messageTime):
    state, timeStamp = checkBuildState(path)

    try:
        if messageTime > 3600:
            messageTime = 3600
        elif messageTime < 1:
            messageTime = 60
        else:
            messageTime = int(int(messageTime) * 60)

    except BaseException:
        if messageTime == "readiness":
            messageTime = 120
        else:
            messageTime = 300

    if not(state):
        countRecheck = 0
        if countRecheck < 3:
            time.sleep(20)
            countRecheck += 1
            realTimeCheck(path)
        else:
            return False, ""
    elif state == "in process.":
        time.sleep(messageTime)
        return state, ""
    else:
        return str(state), str(timeStamp)

def checkLastBuildsList(path):
    try:
        soup           = BeautifulSoup(req.get(path).text, 'lxml')
        buildIsRunning = re.search(r'display-name',str(soup.find_all("a"))).group(0)
        builds         = soup.find_all("a", { "class" : "tip model-link inside build-link display-name" }, limit=10, text = True)
        buildNumbers   = []
        buildNames     = ""

        i = 0
        while i < len(builds):
            stringEnd   = re.search(r'</a>',str(builds[i])).start()
            stringStart = re.search(r'>',str(builds[i])).end()
            buildNames  = buildNames + "\n" + str(builds[i])[stringStart:stringEnd]
            buildNumbers.append(re.search(r'\d+',str(builds[i])[stringStart:stringEnd]).group(0))
            i += 1

        return buildNames, buildNumbers   
    except BaseException:
        return "Something wrong with your link, please, check it.", ""

def timestampSearch(text):
    text = str(re.search(r'\d{2}:\d{2}:\d{2}</b> </span>]', str(text.find_all('span',{"class": "timestamp"}))))
    text = str(re.search(r'\d{2}:\d{2}:\d{2}', text).group(0))
    return text
