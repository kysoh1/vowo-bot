import io
import person

class tracker():
    def __init__(self):
        self.trackPeople = []
        
    def addPerson(self, person):
        self.trackPeople.append(person)
        
    def getPerson(self, personID):
        for person in self.trackPeople:
            if person.id == personID:
                return person
            
    def updateDatabase(self, updatedPerson):
        for i in range(0, len(self.trackPeople)):
            if self.trackPeople[i] == updatedPerson.id:
                self.trackPeople[i] = updatedPerson
                break
    
    def readFile(self):
        file = open("database.txt", "r")
        
        for line in file:
            parts = line.split(",")
            personStats = person.personStats(int(parts[0]), int(parts[1]), int(parts[2]))
            self.trackPeople.append(personStats)
        
        file.close()
         
    def writeFile(self):
        file = open("database.txt", "w")
        
        for person in self.trackPeople:
            file.write(str(person.id) + "," + str(person.purplePity) + "," + str(person.yellowPity) + "\n")
            
        file.close()
                
        