import tkinter as tk
from tkinter import messagebox

class ClientForm(tk.Frame):

    def __init__(self, parent, controller, conn, **kwargs):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.conn = conn

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
        #last name entry
        self.lastname = tk.Entry(entry_frame)
        self.lastname.grid(row=1, column=0)
        #last name error label
        self.lastname_error = tk.Label(entry_frame, label_args)
        self.lastname_error.grid(row=1, column=1)

        #first name label
        label_firstname = tk.Label(entry_frame, label_args, text='Ім\'я:*')
        label_firstname.grid(row=2, column=0)
        #first name entry
        self.firstname = tk.Entry(entry_frame)
        self.firstname.grid(row=3, column=0)
        #first mane error label
        self.firstname_error = tk.Label(entry_frame, label_args)
        self.firstname_error.grid(row=3, column=1)

        #middle name label
        label_middlename = tk.Label(entry_frame, label_args, text='По батькові:')
        label_middlename.grid(row=4, column=0)
        #middle name entry
        self.middlename = tk.Entry(entry_frame)
        self.middlename.grid(row=5, column=0)
        #middle name error label
        self.middlename_error = tk.Label(entry_frame, label_args)
        self.middlename_error.grid(row=5, column=1)

        #phone label
        label_phone = tk.Label(entry_frame, label_args, text='Телефон:*')
        label_phone.grid(row=6, column=0)
        #phone entry
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

        #submit button
        submit_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.submit(),
                                  text='Зберегти')
        submit_button.grid(row=8, column=0, pady=10)
        #submit label
        self.submit_label = tk.Label(entry_frame, label_args)
        self.submit_label.grid(row=8, column=1)

        #return to menu button
        back_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('StartPage'),
                                  text='Повернутись до меню')
        back_button.grid(row=9, column=0, pady=20)

    def submit(self):
        self.submit_label.config(text='')
        if not all([self.validate_firstname(), self.validate_lastname(), self.validate_middlename(), self.validate_phone()]):
            return

        firstname = self.firstname.get()
        lastname = self.lastname.get()
        middlename = self.middlename.get()
        phone = self.phone.get()

        cur = self.conn.cursor()
        cur.execute('''INSERT INTO clients (lastname, firstname, middlename, phone)
                    VALUES ( %s, %s, %s, %s );''',
                    (lastname, firstname, middlename, phone))
        self.conn.commit()
        cur.close()

        self.firstname.delete(0, 'end')
        self.lastname.delete(0, 'end')
        self.middlename.delete(0, 'end')
        self.phone.delete(0, 'end')

        self.submit_label.config(fg='green', text='Успішно збережено!')

    def validate_firstname(self):
        firstname = self.firstname.get()
        is_ok = False
        message = ''
        if(not firstname):
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
        if(not lastname):
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
        if(not phone):
            message = 'Введіть номер'
        elif(len(phone) > 10):
            message = 'Ваш телефон занадто довгий'
        elif(len(phone) < 4):
            message = 'Ваш телефон занадто короткий'
        elif(not phone.isdecimal()):
            message = 'Дозволені лише числа'
        elif(self.has_phone(phone)):
            message = 'Клієнт з таким номером вже існує'
        else:
            is_ok = True

        self.phone_error.config(text=message, fg='red', width=len(message))
        return is_ok

    def has_phone(self, phone):
        cur = self.conn.cursor()
        cur.execute('SELECT EXISTS(SELECT 1 FROM clients WHERE phone = %s);', [phone])
        return cur.fetchone()[0]

class ClientInfo(tk.Frame):

    def __init__(self, parent, controller, conn, **kwargs):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.conn = conn

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
                                 text=' Інформація про клієнтів',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack()

        #label bellow main label
        selection_label = tk.Label(self,
                                   text='Оберіть клієнта:',
                                   font=('dejavu sans mono',20),
                                   bg='#BDBDBD',
                                   fg='white',
                                   anchor='w')
        selection_label.pack(fill='x')

        #middle frame
        middle_frame = tk.Frame(self, bg='#F5F5F5')
        middle_frame.pack(fill='both', expand=True)

        #frame for containing button and covering frame
        left_frame = tk.Frame(middle_frame, bg='#F5F5F5')
        left_frame.pack(fill='both', side='left', expand=True)

        #button frame
        self.button_frame = tk.Frame(left_frame, bg='#F5F5F5')
        self.button_frame.grid(row=0, column=0, sticky='wsne')

        #covering frame to cover buttons
        self.cover_frame = tk.Frame(left_frame, bg='#F5F5F5')
        self.cover_frame.grid(row=0, column=0, sticky='wsne')

        button_args = {'bg' : '#7C4DFF',
                        'border': 0,
                        'fg' : 'white',
                        'width' : 20,
                        'height' : 2,
                        'font' : ('dejavu sans mono',10)
                        }

        edit_button = tk.Button(self.button_frame,
                                button_args,
                                text='Редагувати')
        edit_button.grid(row=0, column=0, pady=5)

        delete_button = tk.Button(self.button_frame,
                                  button_args,
                                  command=lambda: self.delete_client(),
                                  text='Видалили')
        delete_button.grid(row=1, column=0, pady=5)

        #bottom frame for return button
        bottom_frame = tk.Frame(self, bg='#F5F5F5')
        bottom_frame.pack(side='bottom', fill='x',)

        #return to menu button
        back_button= tk.Button(bottom_frame,
                               button_args,
                               command=lambda:controller.show_frame('StartPage'),
                               text='Повернутись до меню')
        back_button.pack(side='left', pady=20)

        #frame for text and listbox
        text_frame = tk.Frame(middle_frame, bg='#F5F5F5')
        text_frame.pack(fill='both', side='right', expand=True)

        self.text_info = tk.Text(text_frame, state='disabled', height=4, font=('dejavu sans mono', 12))
        self.text_info.grid(row=0, column=1, padx=10, pady=10)

        phone_list = self.get_phone_list()
        self.phone_listbox = tk.Listbox(text_frame, height=len(phone_list), selectmode='single', font=('dejavu sans mono', 12))
        for phone in phone_list:
            self.phone_listbox.insert(tk.END, phone)
        self.phone_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.phone_listbox.bind('<<ListboxSelect>>', lambda x : self.phone_listbox_selected())

    def delete_client(self):
        answer = tk.messagebox.askyesno(title='Увага!',
                                        message='Це видалить клієнта, його замовлення та деталі замовлень. Продовити?')
        if answer:
            cur = self.conn.cursor()

            selected = self.phone_listbox.curselection()
            phone = self.phone_listbox.get(selected)

            cur.execute('DELETE FROM clients WHERE phone = %s', [phone])
            self.conn.commit()
            cur.close()

            self.phone_listbox.delete(selected)


    def phone_listbox_selected(self):
        self.button_frame.tkraise()
        self.update_text_info()

    def update_text_info(self):
        text = ''
        selected = self.phone_listbox.curselection()
        if selected:
            phone = self.phone_listbox.get(selected)
            (phone, lastname, firstname, middlename) = self.get_client_info(phone)
            text = f"Телефон: {phone}\nПрізвище: {lastname}\nІм'я: {firstname}\nПо батькові: {middlename}"

        self.text_info.config(state='normal')
        self.text_info.delete(1.0, tk.END)
        self.text_info.insert(tk.INSERT, text)
        self.text_info.config(state='disabled')

    def get_client_info(self, phone):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM clients WHERE phone = %s', [phone])
        res = cur.fetchone()
        cur.close()
        return res

    def get_phone_list(self):
        cur = self.conn.cursor()
        cur.execute('SELECT phone FROM clients;')
        res = [i[0] for i in cur.fetchall()]
        cur.close()
        return res
