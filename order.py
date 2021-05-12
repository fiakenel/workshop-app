import tkinter as tk
from tkinter import messagebox
from presets_forms import *
from tkcalendar import Calendar, DateEntry
from tkinter import ttk

class OrderForm(tk.Frame):

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
                                 text=' Форма замовлення',
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

        #code label
        label_code = tk.Label(entry_frame, label_args, text='Код:')
        label_code.grid(row=0, column=0)
        #code entry
        self.code = tk.Entry(entry_frame)
        #self.code.insert(0, self.get_next_code())
        self.code.config(state='disabled')
        self.code.grid(row=1, column=0)

        #date label
        label_date = tk.Label(entry_frame, label_args, text='Дата:*')
        label_date.grid(row=2, column=0)
        #date entry
        self.date = DateEntry(entry_frame, width=12, background='#7C4DFF',
                        foreground='white', borderwidth=2)
        self.date.grid(row=3, column=0)
        #date error label
        self.date_error = tk.Label(entry_frame, label_args)
        self.date_error.grid(row=3, column=2)

        #time label
        label_time = tk.Label(entry_frame, label_args, text='Час:*')
        label_time.grid(row=4, column=0)
        #time spinboxes
        spinframe = tk.Frame(entry_frame, bg='#F5F5F5')
        spinframe.grid(row=5, column=0)
        self.time = (tk.Spinbox(spinframe, from_=0, to=24, width=2),
                     tk.Spinbox(spinframe, from_=0, to=60, width=2))
        self.time[0].pack(side='left')
        self.time[1].pack(side='left')

        #phone label
        label_phone = tk.Label(entry_frame, label_args, text='Телефон замовника:*')
        label_phone.grid(row=6, column=0)
        #phone combobox
        self.phone = ttk.Combobox(entry_frame)
        self.phone.grid(row=7, column=0)

        #submit button
        submit_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.submit(),
                                  text='Зберегти')
        submit_button.grid(row=8, column=0, pady=10)
        #submit label
        self.submit_label = tk.Label(entry_frame, label_args)
        self.submit_label.grid(row=8, column=2)

        #return to menu button
        back_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.return_clicked(),
                                  text='Повернутись до меню')
        back_button.grid(row=9, column=0, pady=20)

    def get_next_code(self):
        pass

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
        self.clear_entries()

    def clear_entries(self):
        self.firstname.delete(0, 'end')
        self.lastname.delete(0, 'end')
        self.middlename.delete(0, 'end')
        self.phone.delete(0, 'end')

    def submit(self):
        self.submit_label.config(text='')
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
        if self.editmode:
            return True
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

    def update_data(self):
        pass

class OrderInfo(tk.Frame):

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

        self.text_info = tk.Text(text_frame, state='disabled', height=4, font=('dejavu sans mono', 12))
        self.text_info.grid(row=0, column=1, padx=10, pady=10)

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
        self.delete_text()
        self.cover_frame.tkraise()

    def delete_text(self):
        self.text_info.config(state='normal')
        self.text_info.delete(1.0, tk.END)
        self.text_info.config(state='disabled')

    def return_clicked(self):
        self.controller.show_frame('StartPage')
        self.delete_text()
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
            self.delete_text()


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
