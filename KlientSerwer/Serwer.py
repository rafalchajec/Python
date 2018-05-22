import gettext
import socket
import Task
import json
import pickle


class Server:

    def __init__(self):
        print('Uruchomiono serwer!')
        self.taskDict = self.loadFromJson()
        self.maxID = int(self.taskDict['MaxID'])
        self.host = ''
        self.port = 8888
        self.size = 1024
        self.backlog = 1
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen(self.backlog)

    def __del__(self):
        print('Serwer zamkniety')

    def run(self):
        client, address = self.s.accept()
        print('Polaczono z ' + str(address))
        while True:
            received = client.recv(self.size)
            if not received:
                break
            received = received.decode('utf-8')

            if received == 'Dodaj':
                task = client.recv(self.size)
                task = pickle.loads(task)
                task.id = self.maxID
                self.taskDict[task.priority].append([task.id, task.toDo])
                self.maxID = self.maxID + 1
                self.taskDict['MaxID'] = self.maxID
                client.send(str.encode('Dodano nowe zadanie!'))
                self.saveToJson()

            elif received == 'Pokaz':
                priority = client.recv(self.size)
                priority = priority.decode('utf-8')
                tasks = str(self.taskDict[priority])
                client.send(str.encode(tasks))
            elif received == 'Wszystkie':
                priority = client.recv(self.size)
                priority = priority.decode('utf-8')
                tasks = str(self.taskDict[priority])
                client.send(str.encode(tasks))
                priority = client.recv(self.size)
                priority = priority.decode('utf-8')
                tasks = str(self.taskDict[priority])
                client.send(str.encode(tasks))
                priority = client.recv(self.size)
                priority = priority.decode('utf-8')
                tasks = str(self.taskDict[priority])
                client.send(str.encode(tasks))				

            elif received == 'Usun':
                wantedID = client.recv(self.size)
                wantedID = int(wantedID.decode('utf-8'))
                self.taskDict['Wysoki'] = [i for i in self.taskDict['Wysoki'] if i[0] != int(wantedID)]
                self.taskDict['Normalny'] = [i for i in self.taskDict['Normalny'] if i[0] != int(wantedID)]
                self.taskDict['Niski'] = [i for i in self.taskDict['Niski'] if i[0] != int(wantedID)]
                self.saveToJson()
                client.send(str.encode('Zakonczono'))
            else:
                client.send(str.encode('Nieprawidlowe dane: ' + received))

        client.close()

    def saveToJson(self):
        data = json.dumps(self.taskDict)
        with open('TaskList.json', 'w') as file:
            file.write(data)
        file.close()

    def loadFromJson(self):
        f = open('TaskList.json', 'r')
        data = f.read()
        data = json.loads(data)
        f.close()
        return data


if __name__ == '__main__':
    try:
        server = Server()
        server.run()
    except:
        print('Serwer zamkniety')
