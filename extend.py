import requests
from pick import pick

class bus :   

    Login_URL = "https://api.369cx.cn/v2/Auth/LoginByTemp"
    SearchBus_URL = "https://api.369cx.cn/v2/Search"
    Info_URL = "https://api.369cx.cn/v2/Line/GetRealTimeLineInfo/"
    Location_URL = "http://iwaybook.369cx.cn/server-ue2/rest/buses/busline/370100/"

    def __init__(self):
        cursor = requests.post(self.Login_URL).json()
        token = cursor['result']['token']
        self.headers = {'Authorization':token}
    
    def Search(self,busid):
        payload = {"keyword":busid}
        cursor = requests.post(self.SearchBus_URL,json=payload,headers=self.headers).json()
        cursor = cursor['result']['result']
        bus = []
        for i in range(len(cursor)):
            sententce = str(cursor[i]['text1']) + " 由 " +  str(cursor[i]['text2'][3:]) + " 开往 " + str(cursor[i]['text3'][3:])
            temp = {'sentence':sententce,'lineid':cursor[i]['guid']}
            bus.append(temp)
        return bus
    
    def getStation(self,lineid):
        Station_URL = self.Info_URL + str(lineid)
        cursor = requests.get(Station_URL,headers=self.headers).json()['result']['stations']
        number = len(cursor)
        station = []
        for i in range(number):
            station.append(cursor[i]['name'])
        return station
    
    def getInfo(self,lineid):
        Info_URL = self.Info_URL + str(lineid)
        All_Station = self.getStation(lineid)
        cursor = requests.get(Info_URL,headers=self.headers).json()['result']
        name = cursor['name']
        businfo = cursor['busses']
        Allbus = []
        Allbus.append(name[:-1])
        if businfo == 'None':
            return '没有车辆'
        for i in range(len(businfo)):
            bus = businfo[i]
            id = bus['busId']
            station = All_Station[bus['stationNo']]
            Air = bus['openAirCon']
            temp = {'id':id,'station':station,"air":Air}
            Allbus.append(temp)
        Allbus.append(cursor['nextBus']['planTime'])
        return Allbus
    
if __name__=='__main__':
    test = bus()
    title = "选择路线"
    busid = input('输入查询的线路')
    line = test.Search(busid)
    options = []
    for i in range(len(line)):
        options.append(line[i]['sentence'])
    index = pick(options,title)[1]
    print (test.getInfo(line[index]['lineid']))