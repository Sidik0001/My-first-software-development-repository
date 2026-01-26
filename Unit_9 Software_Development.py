
'''
Unit 9- Software Development Consolidate Task

Window creation with button

Tkinter Spreadsheet saving and loading via text file

'''


from tkinter import *
from tkinter import ttk
root = Tk()
frm = ttk.Frame(root, padding=90)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()



class Window:
    def __init__(self, master):
        self.master = master

        self.Main = Frame(self.master)


        #Top section
        self.top = Frame(self.Main)

        self.title = Label(self.top, text = 'Welcome welcome')
        self.title.pack(padx = 5, pady =5)

        self.top.pack(padx = 5, pady =5)
        # Top section


        #Middle section
        self.middle = Frame(self.Main)

        self.row = 10
        self.col = 12

        self.cells = [[None for i in range(self.col)] for j in range(self.row)]

        for i in range(self.row):
            for j in range(self.col):
                self.cells[i][j] = Entry(self.middle, width = 5)
                self.cells[i][j].grid(row = i, column = j)

        self.middle.pack(padx = 5, pady = 5)
        #Middle section

        #Bottom section
        self.bottom = Frame(self.Main)

        self.saveButton = Button(self.bottom, text = 'Save', command = self.save)
        self.saveButton.pack(padx = 5, pady =5, side = RIGHT)

        self.loadButton = Button(self.bottom, text = 'Load', command = self.load)
        self.loadButton.pack(padx = 5, pady = 5, side = RIGHT)

        self.clearButton = Button(self.bottom, text ='Clear', command =self.clear)
        self.clearButton.pack(padx = 5, pady =5, side = LEFT)

        self.bottom.pack(padx = 5, pady = 5, expand = True, fill = X)
        #Bottom section

        self.Main.pack(padx = 5, pady = 5, expand = True, fill = X)
    
    
    def save(self):
        file = open('data.txt', 'w')

        for i in range (self.row):
            for j in range (self.col):
                file.write(self.cells[i][j].get() + ',')
            file.write('\n')

        file.close()

    
    def load(self):
        file = open('data.txt', 'r')

        self.clear()

        for i in range(self.row):
            temp = file.readline()
            temp = temp.split(',')
            for j in range(self.col):
                self.cells[i][j].insert(0, temp[j].strip())
    
    def clear(self):

         for i in range(self.row):
             for j in range(self.col):
                 self.cells[i][j].delete(0, 'end')

root = Tk()
window = Window(root)
root.mainloop()


