import tkinter as tk
from tkinter import messagebox
from presets_forms import *
from decimal import Decimal
import re

class MasterForm(tk.Frame):

    NAME_LENGTH = 13
    MAX_PERCENT = 100
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
                                 text=' Форма майстра',
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
        label_code = tk.Label(entry_frame, label_args, text='Код*:')
        label_code.grid(row=0, column=0)
        #code entry
        self.code = tk.Entry(entry_frame)
        self.code.insert(0, self.get_next_code())
        self.code.config(state='disabled')
        self.code.grid(row=1, column=0)

        #last name label and entry
        label_lastname = tk.Label(entry_frame, label_args, text='Прізвище:*')
        label_lastname.grid(row=2, column=0)
        #last name entry
        self.lastname = tk.Entry(entry_frame)
        self.lastname.grid(row=3, column=0)
        #last name error label
        self.lastname_error = tk.Message(entry_frame, message_args)
        self.lastname_error.grid(row=3, column=1, sticky='W')

        #first name label
        label_firstname = tk.Label(entry_frame, label_args, text='Ім\'я:*')
        label_firstname.grid(row=4, column=0)
        #first name entry
        self.firstname = tk.Entry(entry_frame)
        self.firstname.grid(row=5, column=0)
        #first mane error label
        self.firstname_error = tk.Message(entry_frame, message_args)
        self.firstname_error.grid(row=5, column=1, sticky='W')

        #middle name label
        label_middlename = tk.Label(entry_frame, label_args, text='По батькові:')
        label_middlename.grid(row=6, column=0)
        #middle name entry
        self.middlename = tk.Entry(entry_frame)
        self.middlename.grid(row=7, column=0)
        #middle name error label
        self.middlename_error = tk.Message(entry_frame, message_args)
        self.middlename_error.grid(row=7, column=1, sticky='W')

        #percent label
        label_percent = tk.Label(entry_frame, label_args, text='Відсоток винагороди:*')
        label_percent.grid(row=8, column=0)
        #percent entry
        self.percent = tk.Entry(entry_frame)
        self.percent.grid(row=9, column=0)
        #percent error label
        self.percent_error = tk.Message(entry_frame, message_args)
        self.percent_error.grid(row=9, column=1, sticky='W')

        #submit button
        submit_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.submit(),
                                  text='Зберегти')
        submit_button.grid(row=10, column=0, pady=10)
        #submit label
        self.submit_message = tk.Message(entry_frame, message_args)
        self.submit_message.grid(row=10, column=1, sticky='W')

        #return to menu button
        back_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.return_clicked(),
                                  text='Повернутись до меню')
        back_button.grid(row=11, column=0, pady=20)

    def get_next_code(self):
        cur = self.conn.cursor()
        cur.execute("SELECT nextval('masters_code_seq')")
        res = cur.fetchone()[0]
        cur.execute("SELECT setval('masters_code_seq', %s)", [int(res)-1])
        self.conn.commit()
        cur.close()
        return int(res)

    def get_master_info(self, code):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM masters WHERE code = %s', [code])
        res = cur.fetchone()
        cur.close()
        return res

    def edit_mode(self, code):
        (code, lastname, firstname, middlename, percent) = self.get_master_info(code)
        if middlename == None:
            middlename = ''
        self.lastname.insert(0, lastname)
        self.firstname.insert(0, firstname)
        self.middlename.insert(0, middlename)
        self.percent.insert(0, percent)
        self.code.config(state='normal')
        self.code.delete(0, 'end')
        self.code.insert(0, code)
        self.code.config(state='disabled')
        self.editmode = True

    def return_clicked(self):
        self.controller.show_frame('StartPage')
        self.editmode = False
        self.clear_entries()
        self.clear_messages()

    def clear_messages(self):
        self.firstname_error.config(text='')
        self.lastname_error.config(text='')
        self.middlename_error.config(text='')
        self.percent_error.config(text='')
        self.submit_message.config(text='')

    def clear_entries(self):
        self.firstname.delete(0, 'end')
        self.lastname.delete(0, 'end')
        self.middlename.delete(0, 'end')
        self.percent.delete(0, 'end')
        self.code.config(state='normal')
        self.code.delete(0, 'end')
        self.code.insert(0, self.get_next_code())
        self.code.config(state='disabled')

    def submit(self):
        self.submit_message.config(text='')
        if not all([self.validate_firstname(), self.validate_lastname(), self.validate_middlename(), self.validate_percent()]):
            return
        code = self.code.get()
        firstname = self.firstname.get()
        lastname = self.lastname.get()
        middlename = self.middlename.get()
        percent = self.percent.get()

        cur = self.conn.cursor()
        if not self.editmode:
            command = '''INSERT INTO masters (lastname, firstname, middlename, reward_percent)
                    VALUES ( %s, %s, %s, %s );'''
            cur.execute(command,
                        (lastname, firstname, middlename, percent))
        else:
            command = '''UPDATE masters SET lastname = %s, firstname = %s, middlename = %s, reward_percent = %s
                        WHERE code = %s;'''
            cur.execute(command,
                        (lastname, firstname, middlename, percent, code))
            self.editmode = False
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

    def validate_percent(self):
        percent = self.percent.get()
        if self.editmode:
            return True
        is_ok = False
        message = ''
        if(not percent):
            message = 'Введіть відсоток'
        elif(not percent.replace('.', '', 1).isdigit()):
            message = 'Некоректне введення'
        elif(Decimal(percent) > self.MAX_PERCENT):
            message = 'Відсоток завеликий'
        else:
            is_ok = True
        self.percent_error.config(text=message, fg='red')
        return is_ok

    def update_data(self):
        self.clear_messages()

class MasterInfo(tk.Frame):

    NAME_LENGTH = 13
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
                                 text=' Інформація про майстрів',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack()

        #label bellow main label
        selection_label = tk.Label(self,
                                   text='Оберіть майстра:',
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
        button_frame.pack(side='left', fill='y')

        self.edit_button = tk.Button(button_frame,
                                button_args,
                                command=lambda: self.call_edit(),
                                text='Редагувати')
        self.edit_button.grid(row=0, column=0, pady=5, padx=10)

        self.delete_button = tk.Button(button_frame,
                                  button_args,
                                  command=lambda: self.delete_master(),
                                  text='Видалили')
        self.delete_button.grid(row=1, column=0, pady=5, padx=10)

        #return to menu button
        back_button= tk.Button(button_frame,
                               button_args,
                               command=lambda:self.return_clicked(),
                               text='Повернутись до меню')
        back_button.grid(row=2, column=0, pady=20)

        #frame for text and listbox
        text_frame = tk.Frame(middle_frame, bg='#F5F5F5')
        text_frame.pack(fill='both', side='right', expand=True)

        self.code_listbox = tk.Listbox(text_frame,
                                       selectmode='single',
                                       width=110,
                                       font=('dejavu sans mono', 12))
        self.code_listbox.bind('<<ListboxSelect>>', lambda x : self.code_listbox_selected())
        self.code_listbox.grid(row=0, column=0, sticky='NW', padx=10, pady=10)

        self.text_message = tk.Message(text_frame,
                                     width=600,
                                     font=('dejavu sans mono', 12),
                                     fg='#212121',
                                     bg='#F5F5F5')
        self.text_message.grid(row=0, column=1, sticky='W')

        self.update_data()

    def call_edit(self):
        selected = self.code_listbox.curselection()
        code = re.findall("\d+", self.code_listbox.get(selected))[0]
        self.controller.show_frame('MasterForm', code)

    def return_clicked(self):
        self.controller.show_frame('StartPage')

    def update_data(self):
        self.disable_buttons()
        self.text_message.config(text='')
        self.code_listbox.delete(0, tk.END)
        code_list = self.get_code_list()
        self.code_listbox.config(height=len(code_list))
        for code in code_list:
            (code, lastname, firstname, middlename, percent) = self.get_master_info(code)
            code = str(code) + ' ' * (3-len(str(code)))
            lastname = lastname + ' ' * (self.NAME_LENGTH-len(lastname))
            firstname = firstname + ' ' * (self.NAME_LENGTH-len(firstname))
            middlename = middlename + ' ' * (self.NAME_LENGTH-len(middlename))
            percent = str(percent) + ' ' * (6-len(str(percent))) + '%'
            self.code_listbox.insert(tk.END, f'Код: {code} | Прізвище: {lastname} | Ім\'я: {firstname} | По батькові: {middlename} | Винагорода: {percent}')

    def delete_master(self):
        answer = tk.messagebox.askyesno(title='Увага!',
                                        message='Це видалить обраного майстра. Продовжити?')
        if answer:
            cur = self.conn.cursor()
            selected = self.code_listbox.curselection()
            code = re.findall("\d+", self.code_listbox.get(selected))[0]
            cur.execute('DELETE FROM masters WHERE code = %s', [code])
            self.conn.commit()
            cur.close()
            self.update_data()

    def disable_buttons(self):
        self.delete_button.config(state='disabled')
        self.edit_button.config(state='disabled')

    def raise_buttons(self):
        self.delete_button.config(state='normal')
        self.edit_button.config(state='normal')

    def code_listbox_selected(self):
        self.update_text_message()
        self.raise_buttons()

    def update_text_message(self):
        text = ''
        selected = self.code_listbox.curselection()
        if selected:
            code = re.findall("\d+", self.code_listbox.get(selected))[0]
            (code, lastname, firstname, middlename, percent) = self.get_master_info(code)
            text = f"Код майстра: {code}\nПрізвище: {lastname}\nІм'я: {firstname}\nПо батькові: {middlename}\nВідсоток винагороди {percent}"
        self.text_message.config(text=text)

    def get_master_info(self, code):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM masters WHERE code = %s', [code])
        res = cur.fetchone()
        cur.close()
        return res

    def get_code_list(self):
        cur = self.conn.cursor()
        cur.execute('SELECT code FROM masters;')
        res = [i[0] for i in cur.fetchall()]
        cur.close()
        return res
