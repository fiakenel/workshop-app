import tkinter as tk
import tkinter.ttk as ttk

class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu = tk.Menu(self, tearoff=0)
        self.config(menu=menu)
        add_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Додати', menu=add_menu)
        add_menu.add_command(label='Клієнт')
        add_menu.add_command(label='Замовлення')
        add_menu.add_command(label='Деталі')
        add_menu.add_command(label='Прайс-лист')
        add_menu.add_command(label='Майстер')
        add_menu.add_separator()
        add_menu.add_command(label='Вийти', command=self.quit)

        info_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Інфо', menu=info_menu)
        info_menu.add_command(label='Про нас')

        self.frames = {}
        for F in (StartPage, ClientForm, OrderForm):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title('Майстерня "у Івана"')
        self.controller.iconphoto(False, tk.PhotoImage(file='spanner.png'))

        # Top frame for main label and icon
        top_frame = tk.Frame(self, borderwidth=40, bg='#9E9E9E')
        top_frame.pack(fill='x', side='top')

        #icon
        icon = tk.PhotoImage(file='spanner.png')
        icon_label = tk.Label(top_frame, image=icon, bg='#9E9E9E')
        icon_label.pack(side='left')
        icon_label.image = icon

        #main label
        heading_label = tk.Label(top_frame,
                                 text='Майстерня "у Івана"',
                                 font=('dejavu sans mono',40),
                                 pady=20,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack()

        #label above the buttons
        selection_label = tk.Label(self,
                                   text='Переглянути дані:',
                                   font=('dejavu sans mono',20),
                                   bg='#BDBDBD',
                                   fg='white',
                                   anchor='w')
        selection_label.pack(fill='x')

        #frame for buttons
        button_frame = tk.Frame(self, bg='#F5F5F5')
        button_frame.pack(fill='both', expand=True)

        buttons_args = {'bg' : '#7C4DFF',
                        'border': 0,
                        'fg' : 'white',
                        'width' : 30,
                        'height' : 2,
                        'font' : ('dejavu sans mono',10)
                        }
        #client button
        button_client = tk.Button(button_frame,
                                  buttons_args,
                                  command=lambda:controller.show_frame('ClientInfo'),
                                  text='Клієнти')
        button_client.grid(row=0, column=0, pady=5)

        #order button
        button_order = tk.Button(button_frame,
                                  buttons_args,
                                  command=lambda:controller.show_frame('OrderInfo'),
                                  text='Замовлення')
        button_order.grid(row=1, column=0, pady=5)

        #details button
        button_details = tk.Button(button_frame,
                                  buttons_args,
                                  command=lambda:controller.show_frame('DetailsInfo'),
                                  text='Деталі замовлення')
        button_details.grid(row=2, column=0, pady=5)

        #priselist button
        button_pricelist = tk.Button(button_frame,
                                  buttons_args,
                                  command=lambda:controller.show_frame('PricelistInfo'),
                                  text='Прайс-листи')
        button_pricelist.grid(row=3, column=0, pady=5)

        #master button
        button_master = tk.Button(button_frame,
                                  buttons_args,
                                  command=lambda:controller.show_frame('MasterInfo'),
                                  text='Майстри')
        button_master.grid(row=4, column=0, pady=5)

        #empty label
        tk.Label(button_frame, bg='#F5F5F5').grid(row=5, column=0, pady=5)

        #request button
        button_requests = tk.Button(button_frame,
                                  buttons_args,
                                  command=lambda:controller.show_frame('RequestsPage'),
                                  text='Запити')
        button_requests.grid(row=6, column=0, pady=5)

class ClientForm(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class OrderForm(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
