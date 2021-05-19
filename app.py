import tkinter as tk
import psycopg2
from startpage import *
from client import *
from order import *
from details import *
from pricelist import *
from master import *
from requests import *

class MyApp(tk.Tk):

    def __init__(self, conn, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu = tk.Menu(self, tearoff=0)
        self.config(menu=menu)
        add_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Додати', menu=add_menu)
        add_menu.add_command(label='Клієнт', command=lambda:self.show_frame('ClientForm'))
        add_menu.add_command(label='Замовлення', command=lambda:self.show_frame('OrderForm'))
        add_menu.add_command(label='Деталі', command=lambda:self.show_frame('DetailsForm'))
        add_menu.add_command(label='Прайс-лист', command=lambda:self.show_frame('PricelistForm'))
        add_menu.add_command(label='Майстер', command=lambda:self.show_frame('MasterForm'))
        add_menu.add_separator()
        add_menu.add_command(label='Вийти', command=self.quit)

        info_menu = tk.Menu(menu, tearoff=0)
       # menu.add_cascade(label='Інфо', menu=info_menu)
       # info_menu.add_command(label='Про нас')

        self.frames = {}
        for F in (StartPage, ClientForm, ClientInfo, OrderForm, OrderInfo, PricelistForm, PricelistInfo, MasterForm, MasterInfo, DetailsForm, DetailsInfo, RequestsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self, conn=conn)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name, pk=''):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.update_data()
        if pk:
            frame.edit_mode(pk)
        frame.tkraise()

if __name__ == "__main__":
    conn = psycopg2.connect(host='localhost',
                            port=5432,
                            database='workshop',
                            user='maksym',
                            password='')

    app = MyApp(conn)
    app.mainloop()

    conn.close()
