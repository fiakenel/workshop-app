import tkinter as tk

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
