class Auth:
    def __init__(self, username):
        self.username = username

    def isManager(self):
        with open("managerlist.txt","r") as managerfile:
            managerlist = managerfile.readlines()
            for manager in managerlist:
                if(self.username == manager):
                    return True
                return False

    def addManager(self):
        with open("managerlist.txt", "a") as managerfile:
            managerfile.write("\n" + self.username)
