import tkinter as tk
from tkinter import messagebox
from presets_forms import *
import re

class ClientForm(tk.Frame):

    NAME_LENGTH = 13
    PHONE_LENGTH = 10
    editmode = False
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
                                 text=' Форма клієнта',
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

        #last name label and entry
        label_lastname = tk.Label(entry_frame, label_args, text='Прізвище:*')
        label_lastname.grid(row=0, column=0)
        #last name entry
        self.lastname = tk.Entry(entry_frame)
        self.lastname.grid(row=1, column=0)
        #last name error label
        self.lastname_error = tk.Message(entry_frame, message_args)
        self.lastname_error.grid(row=1, column=1, sticky='W')

        #first name label
        label_firstname = tk.Label(entry_frame, label_args, text='Ім\'я:*')
        label_firstname.grid(row=2, column=0)
        #first name entry
        self.firstname = tk.Entry(entry_frame)
        self.firstname.grid(row=3, column=0)
        #first mane error label
        self.firstname_error = tk.Message(entry_frame, message_args)
        self.firstname_error.grid(row=3, column=1, sticky='W')

        #middle name label
        label_middlename = tk.Label(entry_frame, label_args, text='По батькові:')
        label_middlename.grid(row=4, column=0)
        #middle name entry
        self.middlename = tk.Entry(entry_frame)
        self.middlename.grid(row=5, column=0)
        #middle name error label
        self.middlename_error = tk.Message(entry_frame, message_args)
        self.middlename_error.grid(row=5, column=1, sticky='W')

        #phone label
        label_phone = tk.Label(entry_frame, label_args, text='Телефон:*')
        label_phone.grid(row=6, column=0)
        #phone entry
        self.phone = tk.Entry(entry_frame)
        self.phone.grid(row=7, column=0)
        #phone error label
        self.phone_error = tk.Message(entry_frame, message_args)
        self.phone_error.grid(row=7, column=1, sticky='W')

        #submit button
        submit_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.submit(),
                                  text='Зберегти')
        submit_button.grid(row=8, column=0, pady=10)
        #submit label
        self.submit_message = tk.Message(entry_frame, message_args)
        self.submit_message.grid(row=8, column=1)

        #return to menu button
        back_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.return_clicked(),
                                  text='Повернутись до меню')
        back_button.grid(row=9, column=0, pady=20)

    def get_client_info(self, phone):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM clients WHERE phone = %s', [phone])
        res = cur.fetchone()
        cur.close()
        return res

    def edit_mode(self, phone):
        (phone, lastname, firstname, middlename) = self.get_client_info(phone)
        if middlename == None:
            middlename = ''
        self.lastname.insert(0, lastname)
        self.firstname.insert(0, firstname)
        self.middlename.insert(0, middlename)
        self.phone.insert(0, phone)
        self.phone.config(state='disabled')
        self.editmode = True

    def return_clicked(self):
        self.controller.show_frame('StartPage')
        self.phone.config(state='normal')
        self.editmode = False
        self.clear_entries()
        self.clear_messages()

    def clear_messages(self):
        self.firstname_error.config(text='')
        self.lastname_error.config(text='')
        self.middlename_error.config(text='')
        self.phone_error.config(text='')
        self.submit_message.config(text='')

    def clear_entries(self):
        self.firstname.delete(0, 'end')
        self.lastname.delete(0, 'end')
        self.middlename.delete(0, 'end')
        self.phone.delete(0, 'end')

    def submit(self):
        self.submit_message.config(text='')
        if not all([self.validate_firstname(), self.validate_lastname(), self.validate_middlename(), self.validate_phone()]):
            return

        firstname = self.firstname.get()
        lastname = self.lastname.get()
        middlename = self.middlename.get()
        phone = self.phone.get()

        cur = self.conn.cursor()
        if not self.editmode:
            command = '''INSERT INTO clients (lastname, firstname, middlename, phone)
                    VALUES ( %s, %s, %s, %s );'''
        else:
            command = '''UPDATE clients SET lastname = %s, firstname = %s, middlename = %s
                        WHERE phone = %s;'''
            self.phone.config(state='normal')
            self.editmode = False
        cur.execute(command,
                    (lastname, firstname, middlename, phone))
        self.conn.commit()
        cur.close()

        self.clear_entries()
        self.submit_message.config(fg='green', text='Успішно збережено!')

    def validate_firstname(self):
        firstname = self.firstname.get()
        is_ok = False
        message = ''
        if(not firstname):
            message = 'Введіть ім\'я'
        elif(len(firstname) > self.NAME_LENGTH):
            message = 'Ваше ім\'я занадто довге'
        elif(not firstname.isalpha()):
            message = 'Дозволені лише літери'
        else:
            is_ok = True

        self.firstname_error.config(text=message, fg='red')
        return is_ok

    def validate_lastname(self):
        lastname = self.lastname.get()
        is_ok = False
        message = ''
        if(not lastname):
            message = 'Введіть прізвище'
        elif(len(lastname) > self.NAME_LENGTH):
            message = 'Ваше прізвище занадто довге'
        elif(not lastname.isalpha()):
            message = 'Дозволені лише літери'
        else:
            is_ok = True

        self.lastname_error.config(text=message, fg='red')
        return is_ok

    def validate_middlename(self):
        middlename = self.middlename.get()
        is_ok = False
        message = ''
        if(len(middlename) > self.NAME_LENGTH):
            message = 'Ваше по батькові занадто довге'
        elif(not middlename.isalpha() and len(middlename) != 0):
            message = 'Дозволені лише літери'
        else:
            is_ok = True

        self.middlename_error.config(text=message, fg='red')
        return is_ok

    def validate_phone(self):
        phone = self.phone.get()
        if self.editmode:
            return True
        is_ok = False
        message = ''
        if(not phone):
            message = 'Введіть номер'
        elif(len(phone) > self.PHONE_LENGTH):
            message = 'Ваш телефон занадто довгий'
        elif(not phone.isdecimal()):
            message = 'Некоректне введення'
        elif(self.has_phone(phone)):
            message = 'Клієнт з таким номером вже існує'
        else:
            is_ok = True

        self.phone_error.config(text=message, fg='red')
        return is_ok

    def has_phone(self, phone):
        cur = self.conn.cursor()
        cur.execute('SELECT EXISTS(SELECT 1 FROM clients WHERE phone = %s);', [phone])
        return cur.fetchone()[0]

    def update_data(self):
        self.clear_messages()

class ClientInfo(tk.Frame):

    NAME_LENGTH = 13
    PHONE_LENGTH = 10
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

        #button frame
        button_frame = tk.Frame(middle_frame, bg='#F5F5F5')
        button_frame.pack(fill='y', side='left')

        self.edit_button = tk.Button(button_frame,
                                button_args,
                                command=lambda: self.call_edit(),
                                text='Редагувати')
        self.edit_button.grid(row=0, column=0, pady=10, padx=10)

        self.delete_button = tk.Button(button_frame,
                                  button_args,
                                  command=lambda: self.delete_client(),
                                  text='Видалили')
        self.delete_button.grid(row=1, column=0, pady=10, padx=10)

        #return to menu button
        back_button= tk.Button(button_frame,
                               button_args,
                               command=lambda:self.return_clicked(),
                               text='Повернутись до меню')
        back_button.grid(row=2, column=0, pady=20)

        #frame for text and listbox
        text_frame = tk.Frame(middle_frame, bg='#F5F5F5')
        text_frame.pack(fill='both', side='right', expand=True)

        self.client_listbox = tk.Listbox(text_frame,
                                        selectmode='single',
                                        width=100,
                                        font=('dejavu sans mono', 12))
        self.client_listbox.grid(row=0, column=0, padx=10, pady=10, sticky='NW')
        self.client_listbox.bind('<<ListboxSelect>>', lambda x : self.client_listbox_selected())

        self.update_data()

    def call_edit(self):
        selected = self.client_listbox.curselection()
        phone = re.findall("\d+", self.client_listbox.get(selected))[0]
        self.controller.show_frame('ClientForm', phone)

    def return_clicked(self):
        self.controller.show_frame('StartPage')

    def update_data(self):
        self.disable_buttons()
        self.client_listbox.delete(0, tk.END)
        phone_list = self.get_phone_list()
        self.client_listbox.config(height=len(phone_list))
        for phone in phone_list:
            (phone, lastname, firstname, middlename) = self.get_client_info(phone)
            phone = str(phone) + ' ' * (self.PHONE_LENGTH - len(str(phone)))
            lastname = lastname + ' ' * (self.NAME_LENGTH - len(lastname))
            firstname = firstname + ' ' * (self.NAME_LENGTH - len(firstname))
            middlename = middlename + ' ' * (self.NAME_LENGTH - len(middlename))
            self.client_listbox.insert(tk.END, f'Телефон: {phone} | Прізвище: {lastname} | Ім\'я: {firstname} | По батькові: {middlename}')

    def delete_client(self):
        answer = tk.messagebox.askyesno(title='Увага!',
                                        message='Це видалить клієнта, його замовлення та деталі замовлень. Продовити?')
        if answer:
            cur = self.conn.cursor()
            selected = self.client_listbox.curselection()
            phone = re.findall("\d+", self.client_listbox.get(selected))[0]
            cur.execute('DELETE FROM clients WHERE phone = %s', [phone])
            self.conn.commit()
            cur.close()
            self.client_listbox.delete(selected)

    def disable_buttons(self):
        self.delete_button.config(state='disabled')
        self.edit_button.config(state='disabled')

    def raise_buttons(self):
        self.delete_button.config(state='normal')
        self.edit_button.config(state='normal')

    def client_listbox_selected(self):
        self.raise_buttons()


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
