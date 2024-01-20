import pyrebase
import datetime
class Weather_Database():


    def __init__(self):
        firebaseConfig = {
              'apiKey': "AIzaSyDv7JJnoDvCS6yu1lGLNlGTOoeTlwbfxhI",
              'authDomain': "weather-database-36241.firebaseapp.com",
              'projectId': "weather-database-36241",
              'storageBucket': "weather-database-36241.appspot.com",
              'messagingSenderId': "558229311382",
              'appId': "1:558229311382:web:e18300e1ef36d2911397b7",
              "databaseURL": "https://weather-database-36241-default-rtdb.asia-southeast1.firebasedatabase.app/"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()
    def getData(self,limit = 10):
        dictionary = {}
        
        datasets = self.db.child("Weather").order_by_child("Date").limit_to_last(limit).get()


        for data in datasets.each():
            if(data.val()["location"] not in dictionary):
                dictionary[data.val()["location"]] = [[],[],[],[],[],[]]


            dictionary[data.val()["location"]][0].append(data.val()["Date"])
            dictionary[data.val()["location"]][1].append(data.val()["humid_data"])
            dictionary[data.val()["location"]][2].append(data.val()["precip_data"])
            dictionary[data.val()["location"]][3].append(data.val()["press_data"])
            dictionary[data.val()["location"]][4].append(data.val()["temp_data"])
            dictionary[data.val()["location"]][5].append(data.val()["wind_data"])
        return dictionary

    def getByDayDate(self,start, end):
        dictionary = {}
        
        datasets = self.db.child("Weather").order_by_child("Date").start_at(start).end_at(end).get()


        for data in datasets.each():
            if(data.val()["location"] not in dictionary):
                dictionary[data.val()["location"]] = [[],[],[],[],[],[]]


            dictionary[data.val()["location"]][0].append(data.val()["Date"])
            dictionary[data.val()["location"]][1].append(data.val()["humid_data"])
            dictionary[data.val()["location"]][2].append(data.val()["precip_data"])
            dictionary[data.val()["location"]][3].append(data.val()["press_data"])
            dictionary[data.val()["location"]][4].append(data.val()["temp_data"])
            dictionary[data.val()["location"]][5].append(data.val()["wind_data"])
        return dictionary

    def uploadData(self,date, humid_data, precip_data,press_data, temp_data, wind_data, location = "QC"):
        data = {"Date": date,
                "humid_data":  humid_data,
                "precip_data": precip_data,
                "press_data": press_data,
                "temp_data": temp_data,
                "wind_data": wind_data,
                "location": location}
        self.db.child("Weather").push(data)

    def getAverageDataByDay(self, dateNow, interval = 7, currentDay = False):
        upperDictionary = {}
        for i in range(interval,0 if not currentDay else -1,-1):
            dateToUse = (dateNow - datetime.timedelta(days = i)).replace(hour = 0 ,minute = 0, second = 0, microsecond = 0)
            dateToEnd = (dateToUse + datetime.timedelta(hours = 23, minutes = 59, seconds = 59))
            datasets = self.db.child("Weather").order_by_child("Date").start_at(int(dateToUse.timestamp())).end_at(int(dateToEnd.timestamp())).get()
            dictionary = {}
            for data in datasets.each():
                if(data.val()["location"] not in dictionary):
                    dictionary[data.val()["location"]] = [[],[],[],[],[],[]]
                dictionary[data.val()["location"]][0].append(data.val()["Date"])
                dictionary[data.val()["location"]][1].append(data.val()["humid_data"])
                dictionary[data.val()["location"]][2].append(data.val()["precip_data"])
                dictionary[data.val()["location"]][3].append(data.val()["press_data"])
                dictionary[data.val()["location"]][4].append(data.val()["temp_data"])
                dictionary[data.val()["location"]][5].append(data.val()["wind_data"])
            for locs in dictionary.keys():
                if(locs not in upperDictionary):
                    upperDictionary[locs] = [[],[],[],[],[],[]]
                upperDictionary[locs][0].append(int(dateToUse.timestamp()))
                upperDictionary[locs][1].append(dictionary[data.val()["location"]][1])
                upperDictionary[locs][2].append(dictionary[data.val()["location"]][2])
                upperDictionary[locs][3].append(dictionary[data.val()["location"]][3])
                upperDictionary[locs][4].append(dictionary[data.val()["location"]][4])
                upperDictionary[locs][5].append(dictionary[data.val()["location"]][5])
        return upperDictionary

    def getDataByHour(self, dateNow, interval = 1):
        upperDictionary = {}

        for i in range(interval, 0, -1):
            dateToUse = (dateNow - datetime.timedelta(hours = i-1)).replace(minute = 0, second = 0, microsecond = 0)
            dateToEnd = (dateToUse + datetime.timedelta(minutes = 59, seconds = 59))
            datasets = self.db.child("Weather").order_by_child("Date").start_at(int(dateToUse.timestamp())).end_at(int(dateToEnd.timestamp())).get()
            dictionary = {}
            for data in datasets.each():
                if(data.val()["location"] not in dictionary):
                    dictionary[data.val()["location"]] = [[],[],[],[],[],[]]
                dictionary[data.val()["location"]][0].append(data.val()["Date"])
                dictionary[data.val()["location"]][1].append(data.val()["humid_data"])
                dictionary[data.val()["location"]][2].append(data.val()["precip_data"])
                dictionary[data.val()["location"]][3].append(data.val()["press_data"])
                dictionary[data.val()["location"]][4].append(data.val()["temp_data"])
                dictionary[data.val()["location"]][5].append(data.val()["wind_data"])
            for locs in dictionary.keys():
                if(locs not in upperDictionary):
                    upperDictionary[locs] = [[],[],[],[],[],[]]
                upperDictionary[locs][0].append(int(dateToUse.timestamp()))
                upperDictionary[locs][1].append(dictionary[data.val()["location"]][1])
                upperDictionary[locs][2].append(dictionary[data.val()["location"]][2])
                upperDictionary[locs][3].append(dictionary[data.val()["location"]][3])
                upperDictionary[locs][4].append(dictionary[data.val()["location"]][4])
                upperDictionary[locs][5].append(dictionary[data.val()["location"]][5])
        return upperDictionary
