from tkinter import *
from socket import *
from time import *

def query():
    #Function which parses the query and sends to server and receives response from the server also
    search_term = book_title.get()
    codedstr = str.encode(search_term)
    conn.send(codedstr)
    print("c_log: The query is", search_term)
    det = conn.recv(32768)
    details = det.decode()
    sleep(0.25)
    print("c_log: Received data from server")
    sleep(0.5)
    update(details)

def update(m):
    #updating the UI with response received from server
    if m == "":
        #checking for empty response from server. Such a case arises only when the command "exit" is sent to the server and the server responds to it with an empty response
        terminate()
    data = Message(update_frame, text=m, width=2000)
    data.config(font=('Helvetica',12))
    data.pack()
    #clearing the query field
    book_title.delete(0, 'end')
    book_title.focus()
    book_title.pack()

def terminate():
    #Close the connection and exit
    emergency = "exit"
    coded_emergency = str.encode(emergency)
    conn.send(coded_emergency)
    sleep(0.5)
    conn.shutdown(1)
    conn.close()
    ui.quit()

def aboutus():
    #create a new UI window for About US
    about = Tk()
    about.title('About US')

    #prints details
    details = Message(about, text='Done By:\nHritvik Patel\tPES1201700125\nSanket HS\tPES1201700158\nYoshitha V\tPES1201701744\n\nCSE CN Project', width=5000)
    details.config(font=('Helvetica',12))
    details.pack()
    
if __name__ == "__main__":
    #Socket programming
    conn = socket(AF_INET, SOCK_STREAM)
    hostname = "localhost"
    port = 13000
    conn.connect((hostname,port))
    
    #initialize the UI
    ui = Tk()
    ui.title('Blossom Book Store')

    #Menubar
    menu = Menu(ui)
    ui.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='Exit', command=terminate)
    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About', command=aboutus)

    #Welcome message
    welcome_frame = Frame(ui)
    welcome_frame.pack(side=TOP)
    z = "You can enter anything in the query like:" + "\n1. <title> get" + "\n2. <title> buy <quantity>" + "\n3. <title> modify clear" + "\n4. <title> modify update <quantity to be kept in cart>" + "\n5. exit"
    welcome = Message(welcome_frame, text=z, width=1000)
    welcome.config(font=('Helvetica', 12))
    welcome.pack()

    #Searching for book with associated UI
    search_frame = Frame(ui)
    search_frame.pack(side=BOTTOM)
    Label(search_frame, text='Enter query').pack(side=LEFT)
    book_title = Entry(search_frame, width=40)
    book_title.pack(side=LEFT)
    book_title.focus()
    button = Button(search_frame, text='Go!', width=8, command=query)
    button.pack(side=LEFT)

    #Updated UI frame
    update_frame = Frame(ui)
    update_frame.pack(side=BOTTOM)

    #run the UI indefinitely
    mainloop()
