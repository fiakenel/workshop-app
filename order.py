import datetime
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
from presets_forms import *
import re

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
        label_code = tk.Label(entry_frame, label_args, text='Код*:')
        label_code.grid(row=0, column=0)
        #code entry
        self.code = tk.Entry(entry_frame)
        self.code.insert(0, self.get_next_code())
        self.code.config(state='disabled')
        self.code.grid(row=1, column=0)

        #date label
        label_date = tk.Label(entry_frame, label_args, text='Дата:*')
        label_date.grid(row=2, column=0)
        #date entry
        self.date = DateEntry(entry_frame,
                              background='#7C4DFF',
                              maxdate=datetime.datetime.now(),
                              locale='uk',
                              selectbackground='#7C4DFF')
        self.date.grid(row=3, column=0)

        #phone label
        label_phone = tk.Label(entry_frame, label_args, text='Замовник:*')
        label_phone.grid(row=4, column=0)
        #phone combobox
        self.phone = ttk.Combobox(entry_frame, state='readonly')
        self.phone.grid(row=5, column=0)
        #phone error field
        self.phone_error = tk.Message(entry_frame, message_args)
        self.phone_error.grid(row=5, column=1, sticky='W')

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
                                  command=lambda:self.return_clicked(),
                                  text='Повернутись до меню')
        back_button.grid(row=7, column=0, pady=20)

    def get_next_code(self):
        cur = self.conn.cursor()
        cur.execute("SELECT nextval('orders_code_seq')")
        res = cur.fetchone()[0]
        cur.execute("SELECT setval('orders_code_seq', %s)", [int(res)-1])
        self.conn.commit()
        cur.close()
        return int(res)

    def get_phone_list(self):
        cur = self.conn.cursor()
        cur.execute('SELECT phone, lastname FROM clients;')
        res = cur.fetchall()
        cur.close()
        return tuple(res)

    def edit_mode(self, code):
        (code, date, phone) = self.get_order_info(code)
        self.code.config(state='normal')
        self.code.delete(0, 'end')
        self.code.insert(0, code)
        self.code.config(state='disabled')
        self.date.set_date(date)
        self.phone.set(phone)
        self.editmode = True

    def get_order_info(self, code):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM orders WHERE code = %s', [code])
        res = cur.fetchone()
        cur.close()
        return res

    def return_clicked(self):
        self.controller.show_frame('StartPage')
        self.editmode = False
        self.clear_entries()
        self.clear_messages()

    def clear_entries(self):
        self.phone.set('')
        self.date.set_date(datetime.datetime.now())
        self.code.config(state='normal')
        self.code.delete(0, 'end')
        self.code.insert(0, self.get_next_code())
        self.code.config(state='disabled')
        self.clear_messages()

    def clear_messages(self):
        self.phone_error.config(text='')
        self.submit_message.config(text='')

    def submit(self):
        date = self.date.get_date()
        phone = re.findall("\d+", self.phone.get())[0] if self.phone.get() else ''
        code = self.code.get()
        if phone == '':
            self.phone_error.config(text='Оберіть номер!')
            return
        cur = self.conn.cursor()
        if not self.editmode:
            command = '''INSERT INTO orders (date, client_phone)
                    VALUES ( %s, %s);'''
            cur.execute(command,
                    (date, phone))
        else:
            command = '''UPDATE orders SET date  = %s, client_phone = %s
                        WHERE code = %s;'''
            cur.execute(command,
                    (date, phone, code))
            self.editmode = False
        self.conn.commit()
        cur.close()
        self.clear_entries()
        self.submit_message.config(fg='green', text='Успішно збережено!')
        self.phone_error.config(text='')


    def update_data(self):
        self.clear_entries()
        self.phone['values'] = self.get_phone_list()


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
                                 text=' Інформація про замовлення',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack()

        #label bellow main label
        selection_label = tk.Label(self,
                                   text='Оберіть замовлення:',
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
                                  command=lambda: self.delete_order(),
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

        self.code_listbox = tk.Listbox(text_frame,
                                        selectmode='single',
                                       width=60,
                                        font=('dejavu sans mono', 12))
        self.code_listbox.grid(row=0, column=0, padx=10, pady=10, sticky='NW')
        self.code_listbox.bind('<<ListboxSelect>>', lambda x : self.code_listbox_selected())

        self.update_data()

    def call_edit(self):
        selected = self.code_listbox.curselection()
        code = re.findall("\d+", self.code_listbox.get(selected))[0]
        self.controller.show_frame('OrderForm', code)

    def return_clicked(self):
        self.controller.show_frame('StartPage')

    def update_data(self):
        self.disable_buttons()
        self.code_listbox.delete(0, tk.END)
        code_list = self.get_code_list()
        self.code_listbox.config(height=len(code_list))
        for code in code_list:
            (code, date, phone) = self.get_order_info(code)
            code = str(code) + ' ' * (5 - len(str(code)))
            date = str(date) + ' '
            phone = str(phone) + ' ' * (10 - len(str(phone)))
            self.code_listbox.insert(tk.END, f'Код: {code} | Дата: {date} | Номер клієнта: {phone}')

    def delete_order(self):
        answer = tk.messagebox.askyesno(title='Увага!',
                                        message='Це видалить замовлення та його деталі. Продовжити?')
        if answer:
            cur = self.conn.cursor()
            selected = self.code_listbox.curselection()
            code = re.findall("\d+", self.code_listbox.get(selected))[0]
            cur.execute('DELETE FROM orders WHERE code = %s', [code])
            self.conn.commit()
            cur.close()
            self.code_listbox.delete(selected)

    def disable_buttons(self):
        self.delete_button.config(state='disabled')
        self.edit_button.config(state='disabled')

    def raise_buttons(self):
        self.delete_button.config(state='normal')
        self.edit_button.config(state='normal')

    def code_listbox_selected(self):
        self.raise_buttons()

    def get_order_info(self, code):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM orders WHERE code = %s', [code])
        res = cur.fetchone()
        cur.close()
        return res

    def get_code_list(self):
        cur = self.conn.cursor()
        cur.execute('SELECT code FROM orders;')
        res = [i[0] for i in cur.fetchall()]
        cur.close()
        return res
