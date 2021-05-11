import tkinter as tk
from labels_buttons import *
class StartPage(tk.Frame):

    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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
                                 text=' Майстерня "ПрацівничОк"',
                                 font=('dejavu sans mono',40),
                                 pady=15,
                                 fg='#212121',
                                 bg='#9E9E9E')
        heading_label.pack(side="top")

        #label bellow main label
        selection_label = tk.Label(self,
                                   text='Переглянути дані:',
                                   font=('dejavu sans mono',20),
                                   bg='#BDBDBD',
                                   fg='white',
                                   anchor='w')
        selection_label.pack(fill='x')

        #frame for buttons
        button_frame = tk.Frame(self, bg='#F5F5F5')
        button_frame.pack(fill='both', expand=True)

        #client button
        button_client = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('ClientInfo'),
                                  text='Клієнти')
        button_client.grid(row=0, column=0, pady=5)

        #order button
        button_order = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('OrderInfo'),
                                  text='Замовлення')
        button_order.grid(row=1, column=0, pady=5)

        #details button
        button_details = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('DetailsInfo'),
                                  text='Деталі замовлення')
        button_details.grid(row=2, column=0, pady=5)

        #priselist button
        button_pricelist = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('PricelistInfo'),
                                  text='Прайс-листи')
        button_pricelist.grid(row=3, column=0, pady=5)

        #master button
        button_master = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('MasterInfo'),
                                  text='Майстри')
        button_master.grid(row=4, column=0, pady=5)

        #empty label
        tk.Label(button_frame, bg='#F5F5F5').grid(row=5, column=0, pady=5)

        #request button
        button_requests = tk.Button(button_frame,
                                  button_args,
                                  command=lambda:controller.show_frame('RequestsPage'),
                                  text='Запити')
        button_requests.grid(row=6, column=0, pady=5)

    def update_data(self):
        pass
