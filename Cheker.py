import tkinter as tk
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pickle
from PIL import Image, ImageTk

class Main(tk.Frame):
    classes_dict = None

    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        '''
        Инициализация интерфейса
        '''
        # ----------------Рамка с кнопками управления
        buttonFrame = tk.Frame(width=920, height=100, bg='#d7d8e0', bd=2)
        buttonFrame.place(x=0, y=0)
        buttonFrame.pack_propagate(False)

        self.add_image = Image.open("img/add.png")
        self.res_add = self.add_image.resize((80, 80))
        self.final_add = ImageTk.PhotoImage(self.res_add)
        btn_open_folder = tk.Button(buttonFrame, text='Открыть', command=self.folder_open, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.final_add)
        btn_open_folder.pack(side=tk.LEFT)

        self.add_image2 = Image.open("img/start.png")
        self.res_add2 = self.add_image2.resize((80, 80))
        self.final_add2 = ImageTk.PhotoImage(self.res_add2)
        btn_start = tk.Button(buttonFrame, text='Старт', command=self.start, bg='#d7d8e0', bd=0,
                              compound=tk.TOP, image=self.final_add2)
        btn_start.pack(side=tk.LEFT)

        self.add_image3 = Image.open("img/change.png")
        self.res_add3 = self.add_image3.resize((80, 80))
        self.final_add3 = ImageTk.PhotoImage(self.res_add3)
        btn_change = tk.Button(buttonFrame, text='Изменить', command=self.open_changer_child, bg='#d7d8e0', bd=0,
                               compound=tk.TOP, image=self.final_add3)
        btn_change.pack(side=tk.LEFT)

        self.add_image4 = Image.open("img/info.png")
        self.res_add4 = self.add_image4.resize((80, 80))
        self.final_add4 = ImageTk.PhotoImage(self.res_add4)
        btn_about = tk.Button(buttonFrame, text='Справка', command=self.help, bg='#d7d8e0', bd=0,
                              compound=tk.TOP, image=self.final_add4)
        btn_about.pack(side=tk.LEFT)

        self.add_image5 = Image.open("img/quit.png")
        self.res_add5 = self.add_image5.resize((80, 80))
        self.final_add5 = ImageTk.PhotoImage(self.res_add5)
        btn_quit = tk.Button(buttonFrame, text='Выход', command=self.byebye, bg='#d7d8e0', bd=0,
                             compound=tk.TOP, image=self.final_add5)
        btn_quit.pack(side=tk.LEFT)

        # ----------------Рамка с радиокнопками
        self.radioFrame = tk.Frame(width=120, height=480, bg='#d7d8e0', bd=2)
        self.radioFrame.place(x=920, y=0)
        self.radioFrame.pack_propagate(False)

        # ----------------Рамка с текстовым полем и скроллом
        textFrame = tk.Frame(width=920, height=380, bg='#d7d8e0', bd=2)
        textFrame.place(x=0, y=100)
        textFrame.pack_propagate(False)

        self.textbox = tk.Text(textFrame, font='Arial 14', wrap='word')

        vscroll = Scrollbar(textFrame, orient=VERTICAL, command=self.textbox.yview)
        self.textbox['yscroll'] = vscroll.set
        vscroll.pack(side='right', fill=Y)

        self.textbox.pack()

    def update_radioframe(self):
        '''
        Инициализация радиокнопок с классами на фрейме
        '''
        self.radioFrame = tk.Frame(width=120, height=480, bg='#d7d8e0', bd=2)
        self.radioFrame.place(x=920, y=0)
        self.radioFrame.pack_propagate(False)

        self.radioText = Label(self.radioFrame, text="Классы:", bg='#d7d8e0')
        self.radioText.pack(anchor=W)

        with open('class_dict.pickle', 'rb') as pickle_file:
            pickle_in = pickle.load(pickle_file)
            self.keysfrompickle = pickle_in.keys()

        self.names = []
        for x in self.keysfrompickle:
            self.names.append(str(x))

        self.radionames = []
        for i in range(len(self.names)):
            self.radionames.append((self.names[i], self.names[i]))

        self.choice = StringVar()
        self.choice.set(None)

        for text, mode in self.radionames:
            self.b = Radiobutton(self.radioFrame, text=text, variable=self.choice,
                            command=self.update_textbox, value=mode, bg='#d7d8e0')
            self.b.pack(anchor=W)

        self.names.clear()
        self.radionames.clear()

    def folder_open(self):
        '''
        Диалоговое окно выбора папки с описанием выборки
        '''
        self.folder = filedialog.askdirectory()

    def help(self):
        messagebox.showinfo('Справка', 'Программа для работы с описанием выборки')

    @staticmethod
    def byebye():
        '''
        Выход из программы
        '''
        try:
            os.remove('class_dict.pickle')
        except:
            root.destroy()
        else:
            root.destroy()

    def update_dictionary(self, class_dict, key, value):
        '''
        Добавление новых значений в словарь
        '''
        if key in class_dict:
            if value not in class_dict[key]:
                class_dict[key].append(value)
        else:
            class_dict[key] = [value]

    def save_by_pickle(self, class_dict):
        '''
        Сохранение полученных данных в pickle для дальнейших действий
        '''
        with open('class_dict.pickle', 'wb') as f:
            pickle.dump(class_dict, f)

    def cheking_files(self, folder, class_dict):
        '''
        Рекурсивный обход всех файлов .xml в каталоге
        '''
        for path, folders, files in os.walk(folder):
            for file in files:
                filename = os.path.join(path, file)
                if '.xml' in filename:
                    with open(filename) as f:
                        for line in f:
                            if '<name>' in line:
                                line = line.strip()
                                key = line.split('name')[-2][1:-2]
                                value = filename
                                self.update_dictionary(class_dict, key, value)
        self.save_by_pickle(class_dict)
        class_dict.clear()
        del class_dict

    def start(self):
        '''
        Запуск поиска классов
        '''
        self.textbox.delete(0.0, 'end')
        try:
            self.classes_dict = {}
            print(self.folder)
            try:
                self.cheking_files(self.folder, self.classes_dict)
            except:
                 messagebox.showinfo('Error', 'Выберете папку с описанием выборки')
            else:
                self.update_radioframe()
                self.files = None
        except:
            messagebox.showinfo('Error', 'Выберете папку с описанием выборки')

    def update_textbox(self):
        '''
        Вывод в textbox
        '''
        self.textbox.delete(0.0, 'end')
        with open('class_dict.pickle', 'rb') as pickle_file:
            pickle_in = pickle.load(pickle_file)
            self.textbox.insert(1.0, pickle_in.get(str(self.choice.get())))

    def open_changer_child(self):
        Child()

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        try:
            with open('class_dict.pickle', 'rb') as pickle_file:
                pickle_in = pickle.load(pickle_file)
                self.keysfrompickle = pickle_in.keys()
        except:
            self.destroy()
            messagebox.showinfo('Error', 'Выберете папку с описанием выборки')
        else:
            self.title('Изменить')
            self.geometry('400x100')
            self.resizable(False, False)

            self.combonames = []
            for x in self.keysfrompickle:
                self.combonames.append(str(x))

            self.choice_className = ttk.Combobox(self, values=self.combonames)
            self.choice_className.current(0)
            self.choice_className.place(x=20, y=20)

            self.add_image6 = Image.open("img/arrow.png")
            self.res_add6 = self.add_image6.resize((60, 40))
            self.final_add6 = ImageTk.PhotoImage(self.res_add6)
            tk.Label(self, image=self.final_add6).place(x=170, y=8)

            self.commentEntryVar = tk.StringVar()
            #self.commentEntryVar.set("default text")

            self.entry_className = ttk.Entry(self, textvariable=self.commentEntryVar)
            self.entry_className.place(x=240, y=20)

            btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
            btn_cancel.place(x=210, y=55)

            btn_changeStart = ttk.Button(self, text='Изменить', command=self.sdfsdfs)
            btn_changeStart.place(x=120, y=55)

            self.grab_set()
            self.focus_set()

    def ReplaceLineInFile(self, fileName, sourceText, replaceText):
        print(fileName)
        print(sourceText)
        print(replaceText)
        self.file = open(fileName, 'r', encoding='utf-8')  
        self.text = self.file.read()  
        self.file.close()  
        self.file = open(fileName, 'w', encoding='utf-8')  
        self.file.write(self.text.replace(sourceText, replaceText))  
        self.file.close()  
        print('yo!')

    def sdfsdfs(self):
        print(self.commentEntryVar.get())
        print(self.choice_className.get())
        try:
            print('try in sasadsada')
            with open('class_dict.pickle', 'rb') as pickle_file:
                pickle_in = pickle.load(pickle_file)
                self.fileNames = pickle_in.get(str(self.choice_className.get()))
            #print(self.fileNames)
        except:
            print('exept in sasasas')
        else:
            print('else in sdsdsd')
            print(self.fileNames)
            for files in self.fileNames:
                self.ReplaceLineInFile(files, self.choice_className.get(), self.commentEntryVar.get())

if __name__ == '__main__':
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title('Class Checker')
    root.geometry('1024x480')
    root.resizable(False, False)
    root.mainloop()


"""
1) + исключить добавление одинаковых имен файлов, если в нем встречаются несколько одинаковых классов
2) - вывод в текстовое поле по одному значению в строке без фигурных скобок
3) +/- добавить перерисовку фрейма с радиокнопками перед новым поиском 
4) +/- добавить кнопку справки
5) - добавить прогресс бар
6) +/- переименование классов
7) +/- лейбл "Классы: "
8) - добавить проверку есть ли у изображения описание, необходимо, если описаний меньше чем картинок
"""
