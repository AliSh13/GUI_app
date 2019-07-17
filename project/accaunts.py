from tkinter import *
import tkinter.ttk as ttk
import sqlite3
import re
from create_pas import *

class Main(Frame):
    def __init__(self, root, db):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = Frame(bg='#FFFFE0',bd=2)
        toolbar.pack(side=TOP, fill=X)

        add_new_acc = Button(toolbar, text='Добавить', command= lambda:Child())
        add_new_acc.pack(side=LEFT)

        edit_acc = Button(toolbar, text='Редактировать',
                                command= lambda:Update())
        edit_acc.pack(side=LEFT)

        delet_acc = Button(toolbar, text='Очистить',command= self.clear)
        delet_acc.pack(side=RIGHT)
        delet_acc = Button(toolbar, text='Удалить',command= self.del_acc)
        delet_acc.pack(side=RIGHT)



        treeScroll = ttk.Scrollbar()
        treeScroll.pack(side=RIGHT, fill=Y)
        self.tree = ttk.Treeview(root, columns=('id', 'name', 'password', 'email',
                                'app'), height=15, show='headings',yscrollcommand = treeScroll.set)

        treeScroll.configure(command=self.tree.yview)
        self.tree.column('id',width=30, anchor=CENTER)
        self.tree.column('name',width=160, anchor=CENTER)
        self.tree.column('password',width=140, anchor=CENTER)
        self.tree.column('email',width=140, anchor=CENTER)
        self.tree.column('app',width=170, anchor=CENTER)

        self.tree.heading('id',text='№')
        self.tree.heading('name',text='Имя')
        self.tree.heading('password',text='Пароль')
        self.tree.heading('email',text='Почта')
        self.tree.heading('app',text='Приложение')

        self.tree.pack(side=LEFT)

    def records(self, name, password, email, app):
        self.db.insert_data(name, password, email, app)
        self.view_records()

    def update_records(self, name, password, email, app):
        self.db.c.execute('UPDATE account SET name=?, password=?, email=?, app=? WHERE id=?',
                            ( name, password, email, app,
                            self.tree.set(self.tree.selection()[0], '#1'))
                            )
        self.db.conn.commit()
        self.view_records()

    def del_acc(self):
        values = self.tree.set(self.tree.selection()[0], "#1")
        self.db.c.execute('DELETE FROM account WHERE id=?',
                                    values.split())
        self.db.conn.commit()
        self.view_records()

    def clear(self):
        self.db.c.execute('DELETE FROM account')
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('SELECT * FROM account')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row) for row in self.db.c.fetchall()]


class Child(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = appl

        self.grab_set()
        self.focus_set()



    def init_child(self):
        self.title('Добавить аккаунт')
        self.geometry("350x250")
        self.resizable(width=False, height=False)

        self.lbl_name = ttk.Label(self,text='Имя:')
        self.lbl_name.place(x=75, y=10)
        self.add_name = ttk.Entry(self, width=24)
        self.add_name.place(x=75, y=30)
        self.add_name.focus()

        self.lbl_password = ttk.Label(self,text='Пароль:')
        self.lbl_password.place(x=75, y=50)
        self.add_password = ttk.Entry(self, width=24)
        self.add_password.place(x=75, y=70)

        self.lbl_email = ttk.Label(self,text='Почту:')
        self.lbl_email.place(x=75, y=90)
        self.add_email = ttk.Entry(self, width=24)
        self.add_email.place(x=75, y=110)

        self.lbl_app = ttk.Label(self,text='Название приложения:')
        self.lbl_app.place(x=75, y=130)
        self.add_app = ttk.Entry(self, width=24)
        self.add_app.place(x=75, y=150)

        self.add_acc = ttk.Button(self, text= 'Добавить')
        self.add_acc.place(x=75, y=180)
        self.add_acc.bind('<Button-1>', lambda event: self.view.records(self.add_name.get(),
                                                      self.add_password.get(),
                                                      self.add_email.get(),
                                                      self.add_app.get()))

        self.cancel = ttk.Button(self, text= 'Отмена', command= self.destroy)
        self.cancel.place(x=190, y=180)
        self.create_pass = ttk.Button(self, text='Придумать пароль')
        self.create_pass.bind('<Button-1>', lambda event: CreatePassword())
        self.create_pass.place(x=105, y=210)

class CreatePassword(Toplevel):
        def __init__(self):
            super().__init__(root)
            self.init_create()
            self.view = appl

            self.wait_visibility()
            self.grab_set()
            self.focus_set()


        def init_create(self):
            self.title('Создать пароль')
            self.geometry("300x150+700+500")
            self.resizable(width=False, height=False)


            self.lbl_create_pass = ttk.Label(self, text= 'Пароль:')
            self.lbl_create_pass.place(x=50, y=10)
            self.create_pswrd = ttk.Entry(self, width=24)
            self.create_pswrd.place(x=50, y=30)

            var = IntVar()
            var.set(1)
            self.num_and_text = Radiobutton(self, text="Буквы и цифры",
                                            variable= var, value=0)
            self.num_and_text.place(x=30, y=50)

            self.all_characters = Radiobutton(self, text="Любые символы",
                                              variable= var, value=1)
            self.all_characters.place(x=30, y=70)


            self.lbl_len_pass = Label(self, text= 'Длина пароля:')
            self.lbl_len_pass.place(x=180, y=50)
            self.len_pass = Spinbox(self, width=3, from_=6, to=24)
            self.len_pass.place(x=190, y=70)

            self.create = Button(self, text="Создать")
            self.create.bind('<Button-1>',lambda event: self.choice(self.create_pswrd,
                                                            self.len_pass.get(),
                                                            var.get()))
            self.create.place(x=90, y=90)

        def choice(self,entry, len_pass, var):
            len_pass = int(len_pass)

            if var == 0:
                entry.delete(0, END)
                entry.insert(0, create_password_(len_pass))
            elif var == 1:
                entry.delete(0, END)
                entry.insert(0,creat_pass_all_char(len_pass))



class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = appl


    def init_edit(self):
        self.add_acc.destroy()
        self.title('Редактировать аккаунт')
        self.add_name = self.add_name.get()
        self.add_password.get()
        self.add_email.get()
        self.add_app.get()
        edit = ttk.Button(self, text='Сохранить')
        edit.place(x=75, y=180)
        edit.bind('<Button-1>', lambda event: self.view.update_records(
                                                    self.add_name.get(),
                                                    self.add_password.get(),
                                                    self.add_email.get(),
                                                    self.add_app.get()))


class DB():
    def __init__(self):
        self.conn = sqlite3.connect('project/acc.db')
        self.c = self.conn.cursor()
        self.c.execute(
                '''CREATE TABLE IF NOT EXISTS account(id integer primary key,
                name text, password text, email text, app text)'''
                )
        self.conn.commit()

    def insert_data(self, name, password, email, app):
        self.c.execute('''INSERT INTO account(name, password, email, app)
                        VALUES(?,?,?,?)''', (name, password, email, app)
        )
        self.conn.commit()


if __name__ == "__main__":
    root = Tk()
    db = DB()
    appl = Main(root, db)
    root.geometry("650x400")
    root.resizable(width=False, height=False)
    __version__="0.0.1 Beta"
    root.title("MyAcc " + __version__)
    root.mainloop()
