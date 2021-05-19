import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from presets_forms import *
import re

class DetailsForm(tk.Frame):

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
                                 text=' Форма деталей замовлення',
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

        #order code label
        label_order_code = tk.Label(entry_frame, label_args, text='Замовлення*:')
        label_order_code.grid(row=0, column=0)
        #order code entry
        self.order_code = ttk.Combobox(entry_frame, state='readonly')
        self.order_code.grid(row=1, column=0)
        #order code error field
        self.order_code_error = tk.Message(entry_frame, message_args)
        self.order_code_error.grid(row=1, column=1, sticky='W')

        #work code label
        label_work_code = tk.Label(entry_frame, label_args, text='Робота*:')
        label_work_code.grid(row=2, column=0)
        #work code entry
        self.work_code = ttk.Combobox(entry_frame, state='readonly')
        self.work_code.grid(row=3, column=0)
        #work code error field
        self.work_code_error = tk.Message(entry_frame, message_args)
        self.work_code_error.grid(row=3, column=1, sticky='W')

        #master code label
        label_master_code = tk.Label(entry_frame, label_args, text='Майстер*:')
        label_master_code.grid(row=4, column=0)
        #master code entry
        self.master_code = ttk.Combobox(entry_frame, state='readonly')
        self.master_code.grid(row=5, column=0)
        #master code error field
        self.master_code_error = tk.Message(entry_frame, message_args)
        self.master_code_error.grid(row=5, column=1, sticky='W')

        #submit button
        submit_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.submit(),
                                  text='Зберегти')
        submit_button.grid(row=6, column=0, pady=10)
        self.submit_message = tk.Message(entry_frame, message_args, fg='green')
        self.submit_message.grid(row=6, column=1, sticky='W')

        #return to menu button
        back_button= tk.Button(entry_frame,
                                  button_args,
                                  command=lambda:self.return_clicked(),
                                  text='Повернутись до меню')
        back_button.grid(row=7, column=0, pady=20)

    def edit_mode(self, code):
        (order_code, work_code, master_code) = code
        self.order_code.set(order_code)
        self.work_code.set(work_code)
        self.master_code.set(master_code)
        self.order_code.config(state='disabled')
        self.work_code.config(state='disabled')
        self.editmode = True

    def return_clicked(self):
        self.controller.show_frame('StartPage')

    def clear_entries(self):
        self.order_code.set('')
        self.work_code.set('')
        self.master_code.set('')
        self.order_code.config(state='readonly')
        self.work_code.config(state='readonly')
        self.clear_messages()

    def clear_messages(self):
        self.order_code_error.config(text='')
        self.master_code_error.config(text='')
        self.work_code_error.config(text='')
        self.submit_message.config(text='')

    def validate(self, order_code, work_code, master_code):
        res = True
        if not order_code:
            self.order_code_error.config(text='Оберіть код!')
            res = False
        if not work_code:
            self.work_code_error.config(text='Оберіть код!')
            res = False
        if not master_code:
            self.master_code_error.config(text='Оберіть код!')
            res = False
        if order_code and work_code and self.exists(order_code, work_code):
            self.submit_message.config(fg='red', text='Деталі для таких замовлення та роботи вже існують')
            res = False
        return res

    def exists(self, order_code, work_code):
        cur = self.conn.cursor()
        cur.execute('SELECT order_code, work_code FROM order_details;')
        if (int(order_code), int(work_code)) in cur.fetchall():
            cur.close()
            return True
        else:
            cur.close()
            return False

    def submit(self):
        self.clear_messages()
        order_code = re.findall("\d+", self.order_code.get())[0] if self.order_code.get() else ''
        work_code = re.findall("\d+", self.work_code.get())[0] if self.work_code.get() else ''
        master_code = re.findall("\d+", self.master_code.get())[0] if self.master_code.get() else ''
        cur = self.conn.cursor()
        if not self.editmode:
            if not self.validate(order_code, work_code, master_code):
                return
            command = '''INSERT INTO order_details (master_code, order_code, work_code)
                    VALUES ( %s, %s, %s);'''
        else:
            command = '''UPDATE order_details SET master_code = %s
                        WHERE order_code = %s and work_code = %s;'''
            self.editmode = False
        cur.execute(command,
                    (master_code, order_code, work_code))
        self.conn.commit()
        cur.close()
        self.clear_entries()
        self.clear_messages()
        self.submit_message.config(fg='green', text='Успішно збережено!')

    def update_data(self):
        self.clear_entries()
        self.order_code['values'] = self.get_order_codes()
        self.work_code['values'] = self.get_work_codes()
        self.master_code['values'] = self.get_master_codes()

    def get_order_codes(self):
        cur = self.conn.cursor()
        cur.execute('SELECT code, client_phone FROM orders;')
        res = cur.fetchall()
        cur.close()
        return res

    def get_work_codes(self):
        cur = self.conn.cursor()
        cur.execute('SELECT code, work_name FROM pricelist;')
        res = cur.fetchall()
        cur.close()
        return res

    def get_master_codes(self):
        cur = self.conn.cursor()
        cur.execute('SELECT code, lastname FROM masters;')
        res = cur.fetchall()
        cur.close()
        return res

class DetailsInfo(tk.Frame):

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
                                 text=' Деталі замовлень',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack()

        #label bellow main label
        selection_label = tk.Label(self,
                                   text='Оберіть рядок:',
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
        info = re.findall("\d+", self.code_listbox.get(selected))
        self.controller.show_frame('DetailsForm', info)

    def return_clicked(self):
        self.controller.show_frame('StartPage')

    def update_data(self):
        self.disable_buttons()
        self.code_listbox.delete(0, tk.END)
        code_list = self.get_info_list()
        self.code_listbox.config(height=len(code_list))
        for code in code_list:
            order_code = str(code[0]) + ' ' * (5-len(str(code[0])))
            work_code = str(code[1]) + ' ' * (5-len(str(code[1])))
            master_code = str(code[2]) + ' ' * (5-len(str(code[2])))
            self.code_listbox.insert(tk.END, f'Код замовлення: {order_code} | Код роботи: {work_code} | Код майстра: {master_code}')

    def delete_order(self):
        answer = tk.messagebox.askyesno(title='Увага!',
                                        message='Це видалить замовлення та його деталі. Продовжити?')
        if answer:
            cur = self.conn.cursor()
            selected = self.code_listbox.curselection()
            code = re.findall("\d+", self.code_listbox.get(selected))
            cur.execute('DELETE FROM order_details WHERE order_code = %s and work_code = %s', code[:2])
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
        self.raise_buttons()

    def get_info_list(self):
        cur = self.conn.cursor()
        cur.execute('SELECT order_code, work_code, master_code FROM order_details;')
        res = cur.fetchall()
        cur.close()
        return res

