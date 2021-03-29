from mycroft import MycroftSkill, intent_file_handler
from mycroft_bus_client import MessageBusClient                                 

import json
import requests
import re

class HotCompagny(MycroftSkill):
    
    ###############################################
    # Init
    ###############################################
    def __init__(self):
        MycroftSkill.__init__(self)
        client = MessageBusClient()
        
    ###############################################
    # Main
    ###############################################
    @intent_file_handler('compagny.hot.intent')
    def handle_compagny_hot(self, message):
        
        # Get user speech
        registeredMessage = message.data.get('utterance').lower()
        userWord = message.data["words"]

        # Sentence about user
        if ("user" in registeredMessage):
    
            if ("add a new user" in registeredMessage):
                self.addUser(userWord)

            elif ("select the user" in registeredMessage):
                self.selectUser(userWord)

            elif ("remove the user" in registeredMessage):
                self.removeUser(userWord)

        # Sentence about heat
        elif (registeredMessage in mess for mess in ["grill me", "roast me", "toast me"] or "bread" in registeredMessage):
             
            heatingWord = registeredMessage.split()[0].lower()
            self.speak_dialog('I will ' + heatingWord + ' "{}"'.format(userWord))

            if ("add new bread" in registeredMessage):
                self.addBread(userWord)
            
            elif ("remove the bread" in registeredMessage):
                self.removeBread(userWord)

            elif ("grill me" in registeredMessage or "toast me" in registeredMessage or "roast me" in registeredMessage):
                self.prepareBread(userWord)

    ###############################################
    # Get all users from database
    ###############################################
    def getAllUsers(self):
        getAllRequest = "https://jsonplaceholder.typicode.com/users" # only for testing
        # getAllRequest = "http://pi@192.168.43.171/Users/"
        headers = {'content-type': 'application/json'}
        r = requests.get(getAllRequest, headers=headers)
        details = json.loads(r.text)
        listUser = []
        for key in details: # get id after 'id:' substring
            tempStr = "id: %s-name: %s" % (key["id"], key["name"].lower())
            listUser.append(tempStr)
    
        # self.speak_dialog('Users getted : "{}"'.format(listUser))
        return listUser

    ###############################################
    # Find the good selection with this name, return his Id
    # TODO : Add a verif if multiple selections have same name
    ###############################################
    def findSelectionId(self, userWord, listSelection):
        positionName = -1
        selectionFounded = False
        for i, s in enumerate(listSelection):
            if userWord in s:
                positionName = i
                selectionFounded = True
                break
        
        if(selectionFounded  == True):
            rowSelection = listSelection[positionName]
            idSelectionStr = rowSelection.split("-")[0] # get the id part
            idSelection = idSelectionStr.rpartition(": ")[-1] # get the number
            return idSelection
        else:
            self.speak_dialog("Name not found in list !")


    ###############################################
    # Add a user to database
    ###############################################
    def addUser(self, userWord):
        url = "http://pi@192.168.43.171/Users/"
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data = userWord)
        details = request.loads(r.text) 
        self.speak_dialog('User created : "{}"'.format(details))

    ###############################################
    ###############################################
    def selectUser(self, userWord):
        
        # Get all users to return their id
        listUser = self.getAllUsers();
        id = self.findSelectionId(userWord, listUser)
        
        if (id != None):
            # Call API
            url = "https://jsonplaceholder.typicode.com/users/" + str(id)
            #url = "http://pi@192.168.43.171/Users/:" + str(id)
            headers = {'content-type': 'application/json'}
            r = requests.get(url, headers=headers)
            details = json.loads(r.text)
            self.speak_dialog('User selected : "{}"'.format(details))
        
        

    ###############################################
    # Remove user from database
    ###############################################
    def removeUser(self, userWord):
        
        # Get all users to return their id
        listUser = self.getAllUsers();
        id = self.findSelectionId(userWord, listUser)
        
        if (id != None):
            # Call API
            url = "http://pi@192.168.43.171/Users/:id"
            headers = {'content-type': 'application/json'}
            r = requests.remove(url, headers=headers)
            details = json.loads(r.text)
            self.speak_dialog('User removed : "{}"'.format(details))

    ###############################################
    # Get all breads from database to return their id
    ###############################################
    def getAllBreads(self):

        # Get all breads to return their id
        getAllRequest = "http://pi@192.168.43.171/Breads/"
        id = self.findSelectionId(userWord, listUser)

        if (id != None):
            # Call API
            headers = {'content-type': 'application/json'}
            r = requests.get(getAllRequest, headers=headers)
            details = json.loads(r.text)
            listBread = []
            for key in details: # get id after 'id:' substring
                listBread.append(key["id"], ": ", key["name"])
        
            self.speak_dialog('Breads getted : "{}"'.format(listBread))
            return listBread

    ###############################################
    # Add a bread to database
    ###############################################
    def addBread(self, userWord):
        url = "http://pi@192.168.43.171/Breads/"
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data = words)
        details = requests.loads(r.text)
        self.speak_dialog('Bread created : "{}"'.format(details))

    ###############################################
    # Prepare bread 
    ###############################################
    def prepareBread(self, userWord):
        
        # Get all breads to return their id
        listBread = self.getAllBreads()
        id = self.findSelectionId(userWord, listUser)

        if (id != None):
            # Call API
            url = "http://pi@192.168.43.171/Toast/:id"
            headers = {'content-type': 'application/json'}
            r = requests.post(url, headers=headers)
            details = json.loads(r.text)
            self.speak_dialog('CHAUFFE MARCEL CHAUFFE!')

    ###############################################
    # Remove bread from database
    ###############################################
    def removeBread(self, userWord):
        
        # Get all users to return their id
        listBread = self.getAllBreads()
        id = self.findSelectionId(userWord, listUser)

        if (id != None):
            # Call API
            url = "http://pi@192.168.43.171/Breads/:id"
            headers = {'content-type': 'application/json'}
            r = requests.remove(url, headers=headers)
            details = json.loads(r.text)
            self.speak_dialog('Bread removed : "{}"'.format(details))

###############################################
# End function
###############################################                
def create_skill():
    return HotCompagny()