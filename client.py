import tkinter as tk
from tkinter import messagebox
from presets_forms import *

class ClientForm(tk.Frame):

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
        self.lastname = tk.Entry(entry_frame, validate='all',
                                 validatecommand=(entry_frame.register(self.validate_lastname), '%i', '%V', '%S', '%P'))
        self.lastname.grid(row=1, column=0)
        #last name error label
        self.lastname_error = tk.Message(entry_frame, message_args, width=600)
        self.lastname_error.grid(row=1, column=1)

        #first name label
        tk.Label(entry_frame, label_args, text='Ім\'я:*').grid(row=2, column=0)
        #first name entry
        self.firstname = tk.Entry(entry_frame, validate='all',
                                 validatecommand=(entry_frame.register(self.validate_firstname), '%i', '%V', '%S', '%P'))
        self.firstname.grid(row=3, column=0)
        #first mane error label
        self.firstname_error = tk.Message(entry_frame, message_args, width=600)
        self.firstname_error.grid(row=3, column=1)

        #middle name label
        label_middlename = tk.Label(entry_frame, label_args, text='По батькові:')
        label_middlename.grid(row=4, column=0)
        #middle name entry
        self.middlename = tk.Entry(entry_frame, validate='all',
                                   validatecommand=(entry_frame.register(self.validate_middlename), '%i', '%V', '%S', '%P'))
        self.middlename.grid(row=5, column=0)
        #middle name error label
        self.middlename_error = tk.Message(entry_frame, message_args, width=600)
        self.middlename_error.grid(row=5, column=1)

        #phone label
        label_phone = tk.Label(entry_frame, label_args, text='Телефон:*')
        label_phone.grid(row=6, column=0)
        #phone entry
        self.phone = tk.Entry(entry_frame, validate='all',
                              validatecommand=(entry_frame.register(self.validate_phone), '%i', '%V', '%S', '%P'))
        self.phone.grid(row=7, column=0)
        #phone error label
        self.phone_error = tk.Message(entry_frame, message_args, width=600)
        self.phone_error.grid(row=7, column=1)

        #submit button
        self.submit_button= tk.Button(entry_frame,
                                      button_args,
                                      command=lambda:self.submit(),
                                      text='Зберегти')
        self.submit_button.grid(row=8, column=0, pady=10)
        #submit label
        self.submit_label = tk.Label(entry_frame, label_args)
        self.submit_label.grid(row=8, column=1)

        #return to menu button
        back_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.return_clicked(),
                                  text='Повернутись до меню')
        back_button.grid(row=9, column=0, pady=20)

    def validate_lastname(self, index, action, text, res):
        if action == 'key' and index == '50': #last name len is grater than 50
            self.lastname_error.config(text='Ваше прізвище занадто довге')
            return False
        elif action == 'key' and not text.isalpha(): #last name contains of not letters
            self.lastname_error.config(text='Дозволені лише літери')
            return False
        elif action == 'focusout' and (index == '-1' or index == '0' )and res == '': #entry is empty
            self.lastname_error.config(text='Поле не може бути порожнім!')
            return False
        else:
            self.lastname_error.config(text='')
            return True

    def validate_firstname(self, index, action, text, res):
        if action == 'key' and index == '50': #first name len is grater than 50
            self.firstname_error.config(text='Ваше ім\'я занадто довге')
            return False
        elif action == 'key' and not text.isalpha(): #first name contains of not letters
            self.firstname_error.config(text='Дозволені лише літери')
            return False
        elif action == 'focusout' and (index == '-1' or index == '0') and res == '': #entry is empty
            self.firstname_error.config(text='Поле не може бути порожнім!')
            return False
        else:
            self.firstname_error.config(text='')
            return True

    def validate_middlename(self, index, action, text, res):
        if action == 'key' and index == '50': #middle name len is grater than 50
            self.middlename_error.config(text='Ваше по батькові занадто довге')
            return False
        elif action == 'key' and not text.isalpha(): #middle name contains of not letters
            self.middlename_error.config(text='Дозволені лише літери')
            return False
        else:
            self.middlename_error.config(text='')
            return True

    def validate_phone(self, index, action, text, res):
        if action == 'key' and index == '10': #phone len is grater than 10
            self.phone_error.config(text='Номер занадто довгий')
            return False
        elif action == 'key' and not text.isdecimal(): #middle name contains of not digits
            self.phone_error.config(text='Дозволені лише числа')
            return False
        elif action == 'focusout' and (index == '-1' or index == '0') and res == '': #entry is empty
            self.phone_error.config(text='Поле не може бути порожнім!')
            return False
        elif action == 'focusout' and self.has_phone(res):
            self.phone_error.config(text='Клієнт з таким номером вже існує')
            return False
        else:
            self.phone_error.config(text='')
            return True

    def get_client_info(self, phone):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM clients WHERE phone = %s', [phone])
        res = cur.fetchone()
        cur.close()
        return res

    def edit_mode(self, phone):
        (phone, lastname, firstname, middlename) = self.get_client_info(phone)
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

    def clear_entries(self):
        self.firstname.delete(0, 'end')
        self.lastname.delete(0, 'end')
        self.middlename.delete(0, 'end')
        self.phone.delete(0, 'end')

    def submit(self):
        self.submit_label.config(text='')
        firstname = self.firstname.get()
        lastname = self.lastname.get()
        middlename = self.middlename.get()
        phone = self.phone.get()
        if not all([firstname, lastname, phone]):
            self.submit_label.config(fg='red', text='Деякі поля порожні')
            return
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
        self.submit_label.config(fg='green', text='Успішно збережено!')

    def has_phone(self, phone):
        cur = self.conn.cursor()
        cur.execute('SELECT EXISTS(SELECT 1 FROM clients WHERE phone = %s);', [phone])
        return cur.fetchone()[0]

    def update_data(self):
        pass

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
                                   text='Оберіть номер клієнта:',
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

        edit_button = tk.Button(self.button_frame,
                                button_args,
                                command=lambda: self.call_edit(),
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
                               command=lambda:self.return_clicked(),
                               text='Повернутись до меню')
        back_button.pack(side='left', pady=20)

        #frame for text and listbox
        text_frame = tk.Frame(middle_frame, bg='#F5F5F5')
        text_frame.pack(fill='both', side='right', expand=True)

        self.text_label = tk.Label(text_frame,
                                   width=60,
                                   font=('dejavu sans mono', 12),
                                   fg='#212121',
                                   bg='#F5F5F5')
        self.text_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.phone_listbox = tk.Listbox(text_frame,
                                        selectmode='single',
                                        font=('dejavu sans mono', 12))
        self.phone_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.phone_listbox.bind('<<ListboxSelect>>', lambda x : self.phone_listbox_selected())

        self.update_data()

    def call_edit(self):
        selected = self.phone_listbox.curselection()
        phone = self.phone_listbox.get(selected)
        self.controller.show_frame('ClientForm', phone)
        self.text_label.config(text='')
        self.cover_frame.tkraise()

    def return_clicked(self):
        self.controller.show_frame('StartPage')
        self.text_label.config(text='')
        self.cover_frame.tkraise()

    def update_data(self):
        self.phone_listbox.delete(0, tk.END)
        phone_list = self.get_phone_list()
        self.phone_listbox.config(height=len(phone_list))
        for phone in phone_list:
            self.phone_listbox.insert(tk.END, phone)

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
            self.text_label.config(text='')


    def phone_listbox_selected(self):
        self.button_frame.tkraise()
        self.update_text_label()

    def update_text_label(self):
        text = ''
        selected = self.phone_listbox.curselection()
        if selected:
            phone = self.phone_listbox.get(selected)
            (phone, lastname, firstname, middlename) = self.get_client_info(phone)
            text = f"Телефон: {phone}\nПрізвище: {lastname}\nІм'я: {firstname}\nПо батькові: {middlename}"

        self.text_label.config(text=text)

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
