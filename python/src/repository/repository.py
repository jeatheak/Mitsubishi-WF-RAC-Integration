from requests import post, Response
import time

class Repository:
    def getAirconStats(ip: str) -> str:
        url = 'http://%s:51443/beaver/command/getAirconStat'%ip
        myobj = {'apiVer':'1.0','command':'getAirconStat','deviceId':'1234567890ABCDEF','operatorId':'d2bc4571-1cea-4858-b0f2-34c18bef1901','timestamp':1649703587}

        x = post(url, json=myobj)

        return x.json()['contents']['airconStat']
    
    def sendAircoCommand( command:str, ip: str):
        url = 'http://%s:51443/beaver/command/setAirconStat'%ip
        myobj = {'apiVer':'1.0','command':'setAirconStat','contents': { 'airconId':'a043b05ad1f2', 'airconStat':command },'deviceId':'a68d811862d2ef38','operatorId':'54302674-f763-4deb-bdba-46d8d92c152d','timestamp': round(time.time())}

        x = post(url, json=myobj)

        return x.json()['contents']['airconStat']