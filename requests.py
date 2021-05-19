import tkinter as tk
from tkinter import ttk
from presets_forms import *
from tkcalendar import Calendar, DateEntry
import datetime
import re

new_btn_args = {**button_args, **{'width': 10, 'height': 1, 'text': 'Обробити'}}
new_lbl_args = {**label_args, **{'width': 80, 'font': ('dejavu sans mono', 13), 'anchor': 'w'}}

class RequestsPage(tk.Frame):

    def __init__(self, parent, controller, conn, **kwargs):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.conn = conn
        self.controller.title('Майстерня "ПрацівничОк"')
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
                                 text=' Запити',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack(side="top")

        #label bellow main label
        selection_label = tk.Label(self,
                                   text='Оберіть запит та введіть дані:',
                                   font=('dejavu sans mono',20),
                                   bg='#BDBDBD',
                                   fg='white',
                                   anchor='w')
        selection_label.pack(fill='x')

        #frame for requests
        requests_frame = tk.Frame(self, bg='#F5F5F5')
        requests_frame.pack(fill='both', expand=True)

        self.answer_message = tk.Message(requests_frame,
                                         width=600,
                                         font=('dejavu sans mono', 12),
                                         anchor='n',
                                         fg='#212121',
                                         bg='#F5F5F5')
        self.answer_message.grid(row=0, column=3, padx=10, pady=10, sticky='N', rowspan=20)

        req1_label = tk.Label(requests_frame,
                              new_lbl_args,
                              text='1) Телефони та прізвища клієнтів, що замовили роботу, що коштує більше ніж X$')
        req1_label.grid(row=0, column=0, columnspan=2)

        self.req1_entry = tk.Entry(requests_frame)
        self.req1_entry.grid(row=1, column=0)

        req1_button = tk.Button(requests_frame,
                                new_btn_args,
                                command=self.proccess_req1)
        req1_button.grid(row=1, column=1, sticky='E')

        req2_label = tk.Label(requests_frame,
                              new_lbl_args,
                              text='2) Коди та назви роботи, яку виконують майстри, винагорода яких менша за Х%')
        req2_label.grid(row=2, column=0, columnspan=2)

        self.req2_entry = tk.Entry(requests_frame)
        self.req2_entry.grid(row=3, column=0)

        req2_button = tk.Button(requests_frame,
                                new_btn_args,
                                command=self.proccess_req2)
        req2_button.grid(row=3, column=1, sticky='E')

        req3_label = tk.Label(requests_frame,
                              new_lbl_args,
                              text='3) Коди та прізвища майстрів, що прийняли замовлення не раніше за день Х')
        req3_label.grid(row=4, column=0, columnspan=2)

        self.req3_entry = DateEntry(requests_frame,
                              background='#7C4DFF',
                              locale='uk',
                              selectbackground='#7C4DFF')
        self.req3_entry.grid(row=5, column=0)

        req3_button = tk.Button(requests_frame,
                                new_btn_args,
                                command=self.proccess_req3)
        req3_button.grid(row=5, column=1, sticky='E')

        req4_label = tk.Label(requests_frame,
                              new_lbl_args,
                              text='4) Телефони та прізвища клієнтів, що замовили Х виробів')
        req4_label.grid(row=6, column=0, columnspan=2)

        self.req4_entry = tk.Entry(requests_frame)
        self.req4_entry.grid(row=7, column=0)

        req4_button = tk.Button(requests_frame,
                                new_btn_args,
                                command=self.proccess_req4)
        req4_button.grid(row=7, column=1, sticky='E')

        req5_label = tk.Label(requests_frame,
                              new_lbl_args,
                              text='5) Код та прізвище майстрів, що не виконують виріб Х')
        req5_label.grid(row=8, column=0, columnspan=2)

        self.req5_entry = ttk.Combobox(requests_frame, state='readonly')
        self.req5_entry.grid(row=9, column=0)

        req5_button = tk.Button(requests_frame,
                                new_btn_args,
                                command=self.proccess_req5)
        req5_button.grid(row=9, column=1, sticky='E')

        req6_label = tk.Label(requests_frame,
                              new_lbl_args,
                              text='6) Код та прізвища майстрів, що виконують такі ж роботи, що й майстер Х')
        req6_label.grid(row=10, column=0, columnspan=2)

        self.req6_entry = ttk.Combobox(requests_frame, state='readonly')
        self.req6_entry.grid(row=11, column=0)

        req6_button = tk.Button(requests_frame,
                                new_btn_args,
                                command=self.proccess_req6)
        req6_button.grid(row=11, column=1, sticky='E')

        req7_label = tk.Label(requests_frame,
                              new_lbl_args,
                              text='7) Телефони та прізвища клієнтів, що зробили замовлення раніше, за клієнта Х')
        req7_label.grid(row=12, column=0, columnspan=2)

        self.req7_entry = ttk.Combobox(requests_frame, state='readonly')
        self.req7_entry.grid(row=13, column=0)

        req7_button = tk.Button(requests_frame,
                                new_btn_args,
                                command=self.proccess_req7)
        req7_button.grid(row=13, column=1, sticky='E')

        req8_label = tk.Label(requests_frame,
                              new_lbl_args,
                              text='8) Код та назва роботи, що замовив тільки клієнт Х')
        req8_label.grid(row=14, column=0, columnspan=2)

        self.req8_entry = ttk.Combobox(requests_frame, state='readonly')
        self.req8_entry.grid(row=15, column=0)

        req8_button = tk.Button(requests_frame,
                                new_btn_args,
                                command=self.proccess_req8)
        req8_button.grid(row=15, column=1, sticky='E')

        #return to menu button
        back_button= tk.Button(requests_frame,
                                  button_args,
                                  command=lambda:self.return_clicked(),
                                  text='Повернутись до меню')
        back_button.grid(row=16, column=0, pady=20)

    def return_clicked(self):
        self.controller.show_frame('StartPage')
        self.clear_entries()
        self.clear_message()

    def clear_message(self):
        pass

    def clear_entries(self):
        self.req1_entry.delete(0, 'end')
        self.req2_entry.delete(0, 'end')
        self.req3_entry.set_date(datetime.datetime.now())
        self.req4_entry.delete(0, 'end')
        self.req5_entry.set('')
        self.req6_entry.set('')
        self.req7_entry.set('')
        self.req8_entry.set('')

    def proccess_req8(self):
        x = re.findall("\d+", self.req8_entry.get())[0] if self.req8_entry.get() else ''
        if not x:
            self.update_text('')
            return
        command = '''
SELECT p1.code, p1.work_name
FROM pricelist AS p1 INNER JOIN order_details AS d2
ON p1.code = d2.work_code
WHERE NOT EXISTS (
SELECT d1.work_code
FROM order_details AS d1 INNER JOIN (
orders AS o1 INNER JOIN clients AS c1 ON o1.client_phone = c1.phone )
ON d1.order_code = o1.code
WHERE p1.code = d1.work_code AND c1.phone != %s);'''
        self.proccess_query(x, command)

    def proccess_req7(self):
        x = re.findall("\d+", self.req7_entry.get())[0] if self.req7_entry.get() else ''
        if not x:
            self.update_text('')
            return
        command = '''
SELECT c1.phone, c1.lastname
FROM clients AS c1 INNER JOIN orders AS o1
ON c1.phone = o1.client_phone WHERE EXISTS (
SELECT 1
FROM clients AS c2 INNER JOIN orders AS o2
ON c2.phone = o2.client_phone WHERE c2.phone = %s AND o2.date > o1.date );'''
        self.proccess_query(x, command)

    def get_client_info(self):
        cur = self.conn.cursor()
        cur.execute('SELECT phone, lastname FROM clients;')
        res = cur.fetchall()
        cur.close()
        return tuple(res)

    def proccess_req6(self):
        x = re.findall("\d+", self.req6_entry.get())[0] if self.req6_entry.get() else ''
        if not x:
            self.update_text('')
            return
        command = '''
SELECT m1.code, m1.lastname
FROM masters AS m1
WHERE NOT EXISTS (
    (SELECT DISTINCT d1.work_code
    FROM order_details AS d1 INNER JOIN masters AS m2
    ON m2.code = d1.master_code
    WHERE m2.code = %s)
    EXCEPT (
        SELECT DISTINCT d2.work_code
        FROM order_details AS d2
        WHERE m1.code = d2.master_code)
    );
'''
        self.proccess_query(x, command)

    def get_master_info(self):
        cur = self.conn.cursor()
        cur.execute('SELECT code, lastname FROM masters;')
        res = cur.fetchall()
        cur.close()
        return res

    def get_work_info(self):
        cur = self.conn.cursor()
        cur.execute('SELECT code, work_name FROM pricelist;')
        res = cur.fetchall()
        cur.close()
        return res

    def proccess_req5(self):
        x = re.findall("\d+", self.req5_entry.get())[0] if self.req5_entry.get() else ''
        if not x:
            self.update_text('')
            return
        command = '''
SELECT m1.code, m1.lastname
FROM masters AS m1
WHERE m1.code NOT IN (
SELECT m2.code
FROM masters AS m2 INNER JOIN order_details AS d1
ON m2.code = d1.work_code
WHERE d1.work_code = %s);'''
        self.proccess_query(x, command)

    def proccess_req4(self):
        x = self.req4_entry.get()
        if not x.isdigit():
            self.update_text('')
            return
        command = '''
SELECT c1.phone, c1.lastname
FROM clients AS c1 INNER JOIN (
        orders AS o1 INNER JOIN order_details AS d1
        ON o1.code = d1.order_code)
    ON c1.phone = o1.client_phone
GROUP BY c1.phone
HAVING COUNT(d1.work_code) = %s;
'''
        self.proccess_query(x, command)


    def proccess_req3(self):
        x = self.req3_entry.get_date()
        command = '''
SELECT DISTINCT masters.code, masters.lastname
FROM masters INNER JOIN
        (order_details INNER JOIN orders
        ON order_details.order_code = orders.code
        )
ON masters.code = order_details.master_code
WHERE orders.date >= %s'''
        self.proccess_query(x, command)

    def proccess_req2(self):
        x = self.req2_entry.get()
        if not x.isdigit():
            self.update_text('')
            return
        command = '''
SELECT DISTINCT pricelist.code, pricelist.work_name
FROM pricelist INNER JOIN
            ( order_details INNER JOIN masters
            ON order_details.master_code = masters.code
            )
ON pricelist.code = order_details.work_code
WHERE masters.reward_percent < %s'''
        self.proccess_query(x, command)

    def proccess_req1(self):
        x = self.req1_entry.get()
        if not x.isdigit():
            self.update_text('')
            return
        command = '''
SELECT DISTINCT clients.phone, clients.lastname
 FROM clients INNER JOIN (
                          orders INNER JOIN (
                                             order_details INNER JOIN pricelist
                                             ON order_details.work_code = pricelist.code
                                            )
                          ON orders.code = order_details.order_code
                         )
ON clients.phone = orders.client_phone
WHERE pricelist.price > %s'''
        self.proccess_query(x, command)

    def proccess_query(self, x, command):
        cur = self.conn.cursor()
        cur.execute(command, [x])
        res = cur.fetchall()
        cur.close()
        self.update_text(res)


    def update_text(self, info):
        if info == '':
            message = 'Неправильне введення'
        elif info == []:
            message = 'Порожній результат'
        else:
            message = '\n'.join([ ' '.join([str(j) for j in i]) for i in info])
        self.answer_message.config(text=message)


    def update_data(self):
        self.req5_entry['values'] = self.get_work_info()
        self.req6_entry['values'] = self.get_master_info()
        self.req7_entry['values'] = self.get_client_info()
        self.req8_entry['values'] = self.get_client_info()
