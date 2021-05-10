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
        add_menu.add_command(label='Клієнт', command=lambda:self.show_frame('ClientForm'))
        add_menu.add_command(label='Замовлення', command=lambda:self.show_frame('OrderForm'))
        add_menu.add_command(label='Деталі', command=lambda:self.show_frame('DetailsForm'))
        add_menu.add_command(label='Прайс-лист', command=lambda:self.show_frame('PricelistForm'))
        add_menu.add_command(label='Майстер', command=lambda:self.show_frame('MasterForm'))
        add_menu.add_separator()
        add_menu.add_command(label='Вийти', command=self.quit)

        info_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Інфо', menu=info_menu)
        info_menu.add_command(label='Про нас')

        self.frames = {}
        for F in (StartPage, ClientForm):
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
        top_frame = tk.Frame(self, borderwidth=10, bg='#9E9E9E')
        top_frame.pack(fill='x', side='top')

        #icon
        icon = tk.PhotoImage(file='spanner.png')
        icon_label = tk.Label(top_frame, image=icon, bg='#9E9E9E')
        icon_label.pack(side='left')
        icon_label.image = icon

        #main label
        heading_label = tk.Label(top_frame,
                                 text=' Майстерня "у Івана"',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack(side="top")

        #label bellow main label
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

        button_args = {'bg' : '#7C4DFF',
                        'border': 0,
                        'fg' : 'white',
                        'width' : 30,
                        'height' : 2,
                        'font' : ('dejavu sans mono',10)
                        }
        #client button
        button_client = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('ClientInfo'),
                                  text='Клієнти')
        button_client.grid(row=0, column=0, pady=5)

        #order button
        button_order = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('OrderInfo'),
                                  text='Замовлення')
        button_order.grid(row=1, column=0, pady=5)

        #details button
        button_details = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('DetailsInfo'),
                                  text='Деталі замовлення')
        button_details.grid(row=2, column=0, pady=5)

        #priselist button
        button_pricelist = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('PricelistInfo'),
                                  text='Прайс-листи')
        button_pricelist.grid(row=3, column=0, pady=5)

        #master button
        button_master = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('MasterInfo'),
                                  text='Майстри')
        button_master.grid(row=4, column=0, pady=5)

        #empty label
        tk.Label(button_frame, bg='#F5F5F5').grid(row=5, column=0, pady=5)

        #request button
        button_requests = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('RequestsPage'),
                                  text='Запити')
        button_requests.grid(row=6, column=0, pady=5)

class ClientForm(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Top frame for main label and icon
        top_frame = tk.Frame(self, borderwidth=10, bg='#9E9E9E')
        top_frame.pack(fill='x', side='top')

        #icon
        icon = tk.PhotoImage(file='spanner.png')
        icon_label = tk.Label(top_frame, image=icon, bg='#9E9E9E')
        icon_label.pack(side='left')
        icon_label.image = icon

        #main label
        heading_label = tk.Label(top_frame,
                                 text=' Додати клієнта',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack()

        #label bellow main label
        selection_label = tk.Label(self,
                                   text='Введіть дані:',
                                   font=('dejavu sans mono',20),
                                   bg='#BDBDBD',
                                   fg='white',
                                   anchor='w')
        selection_label.pack(fill='x')

        #frame for entries
        entry_frame = tk.Frame(self, bg='#F5F5F5')
        entry_frame.pack(fill='both', expand=True)

        label_args = {'font' : ('dejavu sans mono', 10),
                      'bg' : '#F5F5F5',
                      'width' : 20,
                      'fg' : '#212121',
                      'anchor' : 'w'}

        #last name label and entry
        label_lastname = tk.Label(entry_frame, label_args, text='Прізвище:*')
        label_lastname.grid(row=0, column=0)

        self.lastname = tk.Entry(entry_frame)
        self.lastname.grid(row=1, column=0)

        #last name error label
        self.lastname_error = tk.Label(entry_frame, label_args)
        self.lastname_error.grid(row=1, column=1)

        #first name label and entry
        label_firstname = tk.Label(entry_frame, label_args, text='Ім\'я:*')
        label_firstname.grid(row=2, column=0)

        self.firstname = tk.Entry(entry_frame)
        self.firstname.grid(row=3, column=0)

        #first mane error label
        self.firstname_error = tk.Label(entry_frame, label_args)
        self.firstname_error.grid(row=3, column=1)

        #middle name label and entry
        label_middlename = tk.Label(entry_frame, label_args, text='По батькові:')
        label_middlename.grid(row=4, column=0)

        self.middlename = tk.Entry(entry_frame)
        self.middlename.grid(row=5, column=0)

        #middle name error label
        self.middlename_error = tk.Label(entry_frame, label_args)
        self.middlename_error.grid(row=5, column=1)

        #phone label and entry
        label_phone = tk.Label(entry_frame, label_args, text='Телефон:*')
        label_phone.grid(row=6, column=0)

        self.phone = tk.Entry(entry_frame)
        self.phone.grid(row=7, column=0)

        #phone error label
        self.phone_error = tk.Label(entry_frame, label_args)
        self.phone_error.grid(row=7, column=1)

        button_args = {'bg' : '#7C4DFF',
                        'border': 0,
                        'fg' : 'white',
                        'width' : 20,
                        'height' : 2,
                        'font' : ('dejavu sans mono',10)
                        }

        submit_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.submit(),
                                  text='Зберегти')
        submit_button.grid(row=8, column=0, pady=10)
        back_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('StartPage'),
                                  text='Повернутись до меню')
        back_button.grid(row=9, column=0, pady=20)

    def submit(self):
        self.validate_firstname()
        self.validate_lastname()
        self.validate_middlename()
        self.validate_phone()

    def validate_firstname(self):
        firstname = self.firstname.get()
        is_ok = False
        message = ''
        if(len(firstname) == 0):
            message = 'Введіть ім\'я'
        elif(len(firstname) > 50):
            message = 'Ваше ім\'я занадто довге'
        elif(not firstname.isalpha()):
            message = 'Дозволені лише літери'
        else:
            is_ok = True

        self.firstname_error.config(text=message, fg='red', width=len(message))
        return is_ok

    def validate_lastname(self):
        lastname = self.lastname.get()
        is_ok = False
        message = ''
        if(len(lastname) == 0):
            message = 'Введіть прізвище'
        elif(len(lastname) > 50):
            message = 'Ваше прізвище занадто довге'
        elif(not lastname.isalpha()):
            message = 'Дозволені лише літери'
        else:
            is_ok = True

        self.lastname_error.config(text=message, fg='red', width=len(message))
        return is_ok

    def validate_middlename(self):
        middlename = self.middlename.get()
        is_ok = False
        message = ''
        if(len(middlename) > 50):
            message = 'Ваше по батькові занадто довге'
        elif(not middlename.isalpha() and len(middlename) != 0):
            message = 'Дозволені лише літери'
        else:
            is_ok = True

        self.middlename_error.config(text=message, fg='red', width=len(message))
        return is_ok

    def validate_phone(self):
        phone = self.phone.get()
        is_ok = False
        message = ''
        if(len(phone) == 0):
            message = 'Введіть номер'
        elif(len(phone) > 10):
            message = 'Ваш телефон занадто довгий'
        elif(len(phone) < 4):
            message = 'Ваш телефон занадто короткий'
        elif(not phone.isdecimal()):
            message = 'Дозволені лише числа'
        else:
            is_ok = True

        self.phone_error.config(text=message, fg='red', width=len(message))
        return is_ok



class OrderForm(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
