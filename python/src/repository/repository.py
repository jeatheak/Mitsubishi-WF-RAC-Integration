from requests import post, Response

class Repository:
    def getAirconStats(ip: str) -> str:
        url = 'http://%s:51443/beaver/command/getAirconStat'%ip
        myobj = {'apiVer':'1.0','command':'getAirconStat','deviceId':'1234567890ABCDEF','operatorId':'d2bc4571-1cea-4858-b0f2-34c18bef1901','timestamp':1649703587}

        x = post(url, json=myobj)

        return x.json()['contents']['airconStat']