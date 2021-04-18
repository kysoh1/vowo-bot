import json, requests, re, datetime
from _datetime import timedelta

mods = [('NF', 1), ('EZ', 2), ('HD', 8), ('HR', 16), ('SD', 32), ('DT', 64), ('RL', 128), ('HT', 256), ('NC', 512), ('FL', 1024)]

class osuStats():
    def __init__(self, token):
        self.token = token
        self.api_base_url = "https://osu.ppy.sh/api/"
    
    def getData(self, url):
        data = requests.get(url)
        return data.json()
    
    def getBeatmaps(self, mapUrl, mod, user=None, mode=None):
        setId, mapId = self.getMapIds(mapUrl)
        
        if 'old' in mapUrl:
            url = self.api_base_url + 'get_beatmaps?&k=' + self.token + '&b=' + setId + '&m=0'
        else:
            url = self.api_base_url + 'get_beatmaps?&k=' + self.token + '&s=' + setId + '&b=' + mapId + '&m=0'

        if mod != '0':
            url = url + '&mods=' + mod
        
        data = self.getData(url)
        
        if len(data) != 0:
            data = data[0]
        
        return data
        
    def getUser(self, user, mode, type=None):
        url = self.api_base_url + 'get_user?k=' + self.token + '&u=' + user + '&m=' + mode
        data = self.getData(url)
        
        if len(data) != 0:
            data = data[0]
        
        return data
        
    def getScores(self, mapUrl, user, mode, type=None):            
        setId, mapId = self.getMapIds(mapUrl)
        
        if 'old' in mapUrl:
            url = self.api_base_url + 'get_scores?k=' + self.token + '&b=' + setId + '&u=' + user + '&m=' + mode
        else:
            url = self.api_base_url + 'get_scores?k=' + self.token + '&b=' + mapId + '&u=' + user + '&m=' + mode
        
        data = self.getData(url)
        
        if len(data) != 0:
            data = data[0]
        
        return data
    
    def getUserBest(self, user, mode, type=None):
        url = self.api_base_url + 'get_user_best?k=' + self.token + '&u=' + user + '&m=' + mode + '&limit=1'
        data = self.getData(url)
        
        if len(data) == 0:
            return data
        else:
            return data[0]
    
    def getUserRecent(self, user, mode):
        url = self.api_base_url + 'get_user_recent?k=' + self.token + '&u=' + user + '&m=' + mode
        data = self.getData(url)
        
        if len(data) != 0:
            data = data[0]
        
        return data
    
    def getMods(self, bitValue):
        bitValue = int(bitValue)
        getMods = ''
        diffValue = bitValue
    
        for x in reversed(mods):
            if bitValue >= x[1]:
                bitValue = bitValue - x[1]
        
                if x[0] == 'NC':
                    bitValue = bitValue - 64  
                    diffValue = diffValue - 64     
            
                if x[0] == 'HD':
                    diffValue = diffValue - 8
                elif x[0] == 'FL':
                    diffValue = diffValue - 1024
                elif x[0] == 'NF':
                    diffValue = diffValue - 1
                elif x[0] == 'SD':
                    diffValue = diffValue - 32
                elif x[0] == 'RL':
                    diffValue = diffValue - 128
            
                getMods = x[0] + getMods 

        if getMods == '':
            getMods = 'No Mod'

        return getMods, diffValue

    def calcAccuracy(self, count300, count100, count50, countMiss):
        accuracy = (50 * count50 + 100 * count100 + 300 * count300) / (300 * (countMiss + count50 + count100 + count300))
    
        return round(accuracy * 100, 2)
    
    def getMapIds(self, mapUrl):
        ids = ['', '']
        index = 0
        
        for i in range(0, len(mapUrl)):
            if mapUrl[i].isdigit():
                ids[index] = ids[index] + mapUrl[i]
                
                if i + 1 != len(mapUrl):
                    if not mapUrl[i + 1].isdigit():
                        index = index + 1

        return ids 
    
    def reformatDate(self, dateStr):
        date = dateStr.split(' ')[0]
        parts = date.split('-')
        
        newDate = ''
        for part in reversed(parts):
            newDate = newDate + part + '-'
            
        return newDate[:-1]
    
    def diffTime(self, dateStr):
        time = dateStr.split(' ')[1]
        parts = time.split(':')
        time = str((int(parts[0]) + 8) % 24) + ':' + parts[1] + ':' + parts[2]
        timeObj = datetime.datetime.now()
        currTime = str(timeObj.hour) + ':' + str(timeObj.minute) + ':' + str(timeObj.second)
        timeFormat = '%H:%M:%S'
        
        timeDiff = datetime.datetime.strptime(currTime, timeFormat) - datetime.datetime.strptime(time, timeFormat)
        if timeDiff.days < 0:
            timeDiff = timedelta(days=0, seconds=timeDiff.seconds, microseconds=timeDiff.microseconds)
    
        hour, minute, second = str(timeDiff).split(':')
        timeStr = ''
        if int(hour) != 0:
            timeStr = timeStr + str(int(hour)) + ' hrs, '
            
        if int(minute) != 0:
            timeStr = timeStr + str(int(minute)) + ' mins, '
            
        if int(second) != 0:
            timeStr = timeStr + str(int(second)) + ' seconds'
            
        if (int(hour) == 0 and int(minute) == 0 and int(second) == 0):
            timeStr = 'Just now'
        else:
            timeStr = timeStr + ' ago'
            
        return timeStr
        