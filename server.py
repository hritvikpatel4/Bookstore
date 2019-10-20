from socket import *
from time import *
import sys

#Books database
#title->0 author->1 quantity->2 price->3 rating->4

def parser(name):
    #Function for parsing the query
    temp = name.split(" ")
    s = " "
    #format is title buy quantity|title modify clear|title modify update quantity|title get
    if temp[-2] == "buy":
        x = find(s.join(temp[:-2]))
        if x >= 0:
            cart(name, x)
    elif temp[-2] == "modify" and temp[-1] == "clear":
        x = find(s.join(temp[:-2]))
        if x >= 0:
            cart(name, x)
    elif temp[-3] == "modify" and temp[-2] == "update":
        x = find(s.join(temp[:-3]))
        if x >= 0:
            cart(name, x)
    elif temp[-1] == "get":
        x = find(s.join(temp[:-1]))
        if x >= 0:
            #handling title get
            transfer(x)

def find(title):
    #returns the index of the title from the database
    for i in range(len(books)):
        if title == books[i][0]:
            return i
    return -1

def transfer(i):
    details = books[i][0].title() + " by " + books[i][1].title() + "\nRating: " + books[i][4] + "\nIn Stock: " + books[i][2] + "\tPrice: " + books[i][3]
    details_en = str.encode(details)
    connsocket.send(details_en)

cart_total = 0
purchaseinfo = {}
def cart(items, index):
    global cart_total
    p = items.split(" ")
    #handling query of type title buy quantity|title modify clear|title modify update quantity
    if p[-2] == "buy":
        if int(p[-1]) > int(books[index][2]) or int(p[-1]) == 0:
            e1 = "Error: Quantity cannot be processed"
            e1_en = str.encode(e1)
            connsocket.send(e1_en)
        else:
            books[index][2] = str(int(books[index][2]) - int(p[-1]))
            cart_total += (int(p[-1])*int(books[index][3]))
            purchaseinfo[books[index][0]] = int(p[-1])
            m1 = "Successfully added to cart!\n" + "Updated quantity for " + books[index][0].title() + " is " + books[index][2] + "\nCart Value: " + str(cart_total)
            m1_en = str.encode(m1)
            connsocket.send(m1_en)
    if p[-2] == "modify" and p[-1] == "clear":
        books[index][2] = str(int(books[index][2]) + purchaseinfo[books[index][0]])
        cart_total -= (purchaseinfo[books[index][0]]*int(books[index][3]))
        m2 = "Successfully modified cart!\n" + "Updated quantity for " + books[index][0].title() + " is " + books[index][2] + "\nCart Value: " + str(cart_total)
        m2_en = str.encode(m2)
        connsocket.send(m2_en)
    if p[-3] == "modify" and p[-2] == "update" and int(p[-1]) > 0 and int(p[-1]) <= int(purchaseinfo[books[index][0]]):
        books[index][2] = str(int(books[index][2]) + purchaseinfo[books[index][0]] - int(p[-1]))
        cart_total -= (int(p[-1])*int(books[index][3]))
        purchaseinfo[books[index][0]] -= int(p[-1])
        m3 = "Successfully modified cart!\n" + "Updated quantity for " + books[index][0].title() + " is " + books[index][2] + "\nCart Value: " + str(cart_total)
        m3_en = str.encode(m3)
        connsocket.send(m3_en)
    
if __name__ == "__main__":
    #Socket programming
    port = 13000
    serverconn = socket(AF_INET, SOCK_STREAM)
    serverconn.bind(("",port))
    serverconn.listen()
    print("s_log: Server running on", port)
    db = open("books.data", 'r+')
    books = db.read()
    print("The books database contains: ")
    print(books)
    books = books.split(";")
    for line in range(len(books)):
        temp = books[line].split(",")
        del books[line]
        books.insert(line, temp)
    print("Update")
    print(books)
    
    connsocket, addr = serverconn.accept()
    while 1:
        term = connsocket.recv(16384)
        decodedterm = term.decode()
        decodedterm = decodedterm.lower()
        if decodedterm == "exit":
            if bool(purchaseinfo):
                #TODO: Update file with contents
            if not bool(purchaseinfo):
                #TODO: Clear the dictionary and revert the transactions
            print("s_log: Closed connection")
            connsocket.shutdown(1)
            connsocket.close()
            db.close()
            books.clear()
            sys.exit()
        print("s_log: Received data from client")
        sleep(0.25)
        print("s_log: Searching database")
        sleep(0.5)
        parser(decodedterm)
        print("s_log: Sending details for the search parameter")
