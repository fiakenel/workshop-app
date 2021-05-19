import datetime
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from decimal import Decimal
from tkinter import ttk
from presets_forms import *
import re

class PricelistForm(tk.Frame):

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
                                 text=' Форма прайс-листа',
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

        #work name label
        label_workname = tk.Label(entry_frame, label_args, text='Назва роботи:*')
        label_workname.grid(row=2, column=0)
        #work name entry
        self.workname = tk.Text(entry_frame, width=25, height=4)
        self.workname.grid(row=3, column=0)
        #work name error label
        self.workname_error = tk.Message(entry_frame, message_args)
        self.workname_error.grid(row=3, column=1, sticky='W')

        #price label
        label_price = tk.Label(entry_frame, label_args, text='Ціна:*')
        label_price.grid(row=4, column=0)
        #price entry
        self.price = tk.Entry(entry_frame)
        self.price.grid(row=5, column=0)
        #price error field
        self.price_error = tk.Message(entry_frame, message_args)
        self.price_error.grid(row=5, column=1, sticky='W')

        #submit button
        submit_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.submit(),
                                  text='Зберегти')
        submit_button.grid(row=6, column=0, pady=10)
        self.submit_message = tk.Message(entry_frame, message_args, fg='green')
        self.submit_message.grid(row=6, column=1)

        #return to menu button
        back_button= tk.Button(entry_frame,
                               button_args,
                               justify='left',
                               command=lambda:self.return_clicked(),
                               text='Повернутись до меню')
        back_button.grid(row=7, column=0, pady=20)

    def get_next_code(self):
        cur = self.conn.cursor()
        cur.execute("SELECT nextval('pricelist_code_seq')")
        res = cur.fetchone()[0]
        cur.execute("SELECT setval('pricelist_code_seq', %s)", [int(res)-1])
        self.conn.commit()
        cur.close()
        return int(res)

    def edit_mode(self, code):
        self.clear_entries()
        (code, text, price) = self.get_pricelist_info(code)
        self.code.config(state='normal')
        self.code.delete(0, 'end')
        self.code.insert(0, code)
        self.code.config(state='disabled')
        self.workname.insert('1.0', text)
        self.price.insert(0, price[1:])
        self.editmode = True

    def return_clicked(self):
        self.controller.show_frame('StartPage')
        self.editmode = False
        self.clear_messages()
        self.clear_entries()

    def clear_entries(self):
        self.price.delete(0, 'end')
        self.workname.delete('1.0', 'end')
        self.code.config(state='normal')
        self.code.delete(0, 'end')
        self.code.insert(0, self.get_next_code())
        self.code.config(state='disabled')
        self.clear_messages()

    def clear_messages(self):
        self.price_error.config(text='')
        self.workname_error.config(text='')
        self.submit_message.config(text='')

    def validate_workname(self):
        workname = self.workname.get('1.0', 'end')
        workname = workname[:len(workname)-1]
        is_ok = False
        message = ''
        if(not workname):
            message = 'Введіть назву'
        elif(len(workname) > 100):
            message = 'Не більше 100 символів'
        else:
            is_ok = True
        self.workname_error.config(text=message, fg='red')
        return is_ok

    def validate_price(self):
        price = self.price.get()
        is_ok = False
        message = ''
        if(not price):
            message = 'Введіть ціну роботи'
        elif(not price.replace('.', '', 1).isdigit()):
            message = 'Дозволені лише числа'
        elif Decimal(price) >= 1000:
            message = 'Задорого!'
        else:
            is_ok = True
        self.price_error.config(text=message, fg='red')
        return is_ok

    def submit(self):
        self.clear_messages()
        if not all([self.validate_workname(), self.validate_price()]):
            return

        code = self.code.get()
        workname = self.workname.get('1.0', 'end')
        workname = workname[:len(workname)-1]
        price = Decimal(self.price.get())
        cur = self.conn.cursor()

        if not self.editmode:
            command = '''INSERT INTO pricelist (work_name, price)
                    VALUES ( %s, %s);'''
            cur.execute(command,
                    (workname, price))
        else:
            command = '''UPDATE pricelist SET work_name  = %s, price = %s
                        WHERE code = %s;'''
            cur.execute(command,
                    (workname, price, code))
            self.editmode = False
        self.conn.commit()
        cur.close()
        self.clear_entries()
        self.clear_messages()
        self.submit_message.config(fg='green', text='Успішно збережено!')


    def update_data(self):
        self.clear_entries()

    def get_pricelist_info(self, code):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM pricelist WHERE code = %s', [code])
        res = cur.fetchone()
        cur.close()
        return res

class PricelistInfo(tk.Frame):

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
                                 text=' Прайс-лист',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack()

        #label bellow main label
        selection_label = tk.Label(self,
                                   text='Оберіть роботу:',
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
                                  command=lambda: self.delete_pricelist(),
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

        self.pricelistbox = tk.Listbox(text_frame,
                                       selectmode='single',
                                       width=70,
                                       font=('dejavu sans mono', 12))
        self.pricelistbox.bind('<<ListboxSelect>>', lambda x : self.pricelistbox_selected())
        self.pricelistbox.grid(row=0, column=0, sticky='NW', padx=10, pady=10)

        self.update_data()

    def call_edit(self):
        selected = self.pricelistbox.curselection()
        code = re.findall("\d+", self.pricelistbox.get(selected))[0]
        self.controller.show_frame('PricelistForm', code)

    def return_clicked(self):
        self.controller.show_frame('StartPage')

    def update_data(self):
        self.disable_buttons()
        self.pricelistbox.delete(0, tk.END)
        code_list = self.get_code_list()
        self.pricelistbox.config(height=len(code_list))
        for code in code_list:
            (code, text, price) = self.get_pricelist_info(code)
            code = str(code) + ' ' * (5-len(str(code)))
            text = text + ' ' * (100-len(text))
            price = str(price) + ' ' * (7-len(str(price)))
            self.pricelistbox.insert(tk.END, f'Код: {code} | Ціна: {price} | Робота: {text}')

    def delete_pricelist(self):
        answer = tk.messagebox.askyesno(title='Увага!',
                                        message='Це видалить обраний прайс-лист. Продовжити?')
        if answer:
            cur = self.conn.cursor()
            selected = self.pricelistbox.curselection()
            code = re.findall("\d+", self.pricelistbox.get(selected))[0]
            cur.execute('DELETE FROM pricelist WHERE code = %s', [code])
            self.conn.commit()
            cur.close()
            self.update_data()

    def disable_buttons(self):
        self.delete_button.config(state='disabled')
        self.edit_button.config(state='disabled')

    def raise_buttons(self):
        self.delete_button.config(state='normal')
        self.edit_button.config(state='normal')

    def pricelistbox_selected(self):
        self.raise_buttons()

    def get_pricelist_info(self, code):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM pricelist WHERE code = %s', [code])
        res = cur.fetchone()
        cur.close()
        return res

    def get_code_list(self):
        cur = self.conn.cursor()
        cur.execute('SELECT code FROM pricelist;')
        res = [i[0] for i in cur.fetchall()]
        cur.close()
        return res
