import socket
import Task
import pickle

class Client:

    def __init__(self):
        self.port = 8888
        self.size = 1024
        self.host = 'localhost'

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        print('Polaczono z serwerem \n'
              '|---------------------------------------|\n'
              '|1. Dodawanie nowego zadania (Dodaj))   |\n' 
              '|---------------------------------------|\n'
              '|2. Pokaz zadania (Pokaz))              |\n'
              '|---------------------------------------|\n'
              '|3. Pokaz wszystkie zadania (Wszystkie))|\n'
              '|---------------------------------------|\n'
              '|4. Usuwanie zadania (Usun))            |\n'
              '|---------------------------------------|\n'
              '|5. Wyjscie z aplikacji (Zamknij)       |')
        print('|---------------------------------------|\n')
        menuChoice = input("Co chcesz zrobic? ")
        while menuChoice != 'Zamknij':
            print('---   ')
            if menuChoice == 'Pomoc':
                print('Dodaj - dodaj nowe zadanie\n'
                'Pokazanie zadania o wybranym priorytecie (Pokaz)\n'
                'Usuwanie zadania (Usun))\n'
                'Wyjscie z aplikacji (Zamknij)\n')
            elif menuChoice == 'Dodaj':
                s.send(str.encode(menuChoice))
                task = Task.Task()
                task.toDo = input('Tresc: ')
                task.priority = input('Priorytet (Wysoki, Normalny, Niski)? ')
                s.send(pickle.dumps(task))
                received = s.recv(self.size)
                print(received.decode('utf-8'))
            elif menuChoice == 'Pokaz':
                s.send(str.encode(menuChoice))
                priority = input('Ktory priorytet pokazac(Wysoki, Normalny, Niski)? ')
                s.send(str.encode(priority))
                received = s.recv(self.size)
                print(received.decode('utf-8'))
            elif menuChoice == 'Wszystkie':
                s.send(str.encode(menuChoice))
                priority = 'Wysoki'
                s.send(str.encode(priority))
                received = s.recv(self.size)
                print(received.decode('utf-8'))
                priority = 'Normalny'
                s.send(str.encode(priority))
                received = s.recv(self.size)
                print(received.decode('utf-8'))
                priority = 'Niski'
                s.send(str.encode(priority))
                received = s.recv(self.size)
                print(received.decode('utf-8'))
            elif menuChoice == 'Usun':
                s.send(str.encode(menuChoice))
                wantedID = input('ID zadania, ktore chcesz usunac? ')
                s.send(str.encode(wantedID))
                received = s.recv(self.size)
                print(received.decode('utf-8'))
            else:
                s.send(str.encode(menuChoice))
                received = s.recv(self.size)
                print(received.decode('utf-8'))
            print('   ')
            menuChoice = input('Co chcesz zrobic? ')
        s.close()


if __name__ == '__main__':
    try:
        client = Client()
        client.run()
    except Exception as e:
        print(str(e))

