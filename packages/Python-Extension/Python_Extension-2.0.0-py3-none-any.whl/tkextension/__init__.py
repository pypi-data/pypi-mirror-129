# -*- coding: utf-8  -*-

import os

def clear():
    try:
        for root, dirs, files in os.walk('__pycache__', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir('__pycache__')
    except OSError:
        pass
    try:
        for root, dirs, files in os.walk('tix/__pycache__', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir('tix/__pycache__')
    except OSError:
        pass
    try:
        os.remove('word bank.dat')
    except OSError:
        pass
    return True

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import pickle
import time

class AskValue():
    def __init__(self, tkinter_attribute, msg='', args=(0, 100), width=100, height=50):
        self.tk = tkinter_attribute
        self.frame = Frame(self.tk, width=width, height=height)
        # Tkinter
        if msg != '':
            self.label = Label(self.frame, text=msg)
            self.label.place(relx=0.5, rely=0.1, anchor='center')
        if type(args[0]) == type(0):
            self.sb = Scale(self.frame, from_=args[0], to=args[1], orient='horizontal')
        elif type(args[0]) == type('0'):
            self.sb = Spinbox(self.frame, values=args, wrap=True)
        else:
            raise TypeError('%s\'s items must be int or string')
        if msg != '':
            self.sb.place(relx=0.5, rely=0.55, relwidth=1, relheight=0.9, anchor='center')
        else:
            self.sb.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
        # Window
    def get_frame(self):
        return self.frame
    def config(self, msg=''):
        if msg != '':
            self.label = Label(self.frame, text=msg)
            self.label.place(relx=0.5, rely=0.1, anchor='center')
            self.sb.forget()
            self.sb.place(relx=0.5, rely=0.55, relwidth=1, relheight=0.9, anchor='center')
        else:
            self.label.forget()
    def get(self):
        return self.sb.get()

class AskItem():
    def __init__(self, tkinter_attribute, msg='', items=['a', 'b', 'c'], number=1, normal=0, width=100, height=100):
        self.items = items
        self.number = number
        self.normal = normal
        # Value
        self.tk = tkinter_attribute
        self.frame = Frame(self.tk, width=width, height=height)
        # Tkinter
        if msg != '':
            self.label = Label(self.frame, text=msg)
            self.label.place(relx=0.5, rely=0.05, relwidth=1, relheight=0.1, anchor='center')
        if width != None and height != None:
            self.lb = Listbox(self.frame, width=width, height=height)
        elif width != None:
            self.lb = Listbox(self.frame, width=width)
        elif height != None:
            self.lb = Listbox(self.frame, height=height)
        else:
            self.lb = Listbox(self.frame)
        if msg != '':
            self.lb.place(relx=0.5, rely=0.55, relwidth=1, relheight=0.9, anchor='center')
        else:
            self.lb.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
        self.lb.selection_set(normal)
        # Window
        for x in range(0, len(items)):
            self.lb.insert('end', items[x])
        # Load
    def get_frame(self):
        return self.frame
    def config(self, msg=''):
        if msg != '':
            self.label = Label(self.frame, text=msg)
            self.label.place(relx=0.5, rely=0.05, relwidth=1, relheight=0.1, anchor='center')
            self.sb.forget()
            self.sb.place(relx=0.5, rely=0.55, relwidth=1, relheight=0.9, anchor='center')
        else:
            self.label.forget()
    def get(self):
        finish = False
        get = []
        for x in range(0, len(self.items)):
            if self.lb.selection_includes(x) == 1:
                get.append(x)
        # Get
        if len(get) == self.number:
            finish = True
        else:
            get.append(self.normal)
        return get

class ControlBoard():
    def __init__(self, tkinter_attribute, msg='', item=[('scale', '', 1, 100), ('listbox', '', [1, 2, 3]), ('radiobutton', '', '1', 'IntVar()', 1)], width=100, height=100):
        self.item = item
        # Value
        self.tk = tkinter_attribute
        self.frame = Frame(self.tk, width=width, height=height)
        # Tkinter
        self.text = Text(self.frame, width=width, height=height)
        self.text.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
        # Text
        if msg != '':
            self.label = Label(self.frame, text=msg)
            self.text.window_create('end', window=self.label)
            self.text.insert('end', '\n')
        # Label
        self.window = []
        self.window_list = []
        self.value_list = []
        for x in item:
            if x[0] == 'scale':
                self.window.append(Scale(self.frame, from_=x[2], to=x[3], orient='horizontal'))
                self.window_list.append('scale')
            elif x[0] == 'listbox':
                self.window.append(Listbox(self.frame))
                self.window_list.append('listbox')
                for y in x[2]:
                    self.window[-1].insert('end', y)
            elif x[0] == 'radiobutton':
                self.value_list.append(x[3])
                self.window.append(Radiobutton(self.frame, text=x[2], variable=x[3], value=x[4]))
                self.window_list.append('radiobutton')
        for x in range(0, len(item)):
            if item[x][1] != '':
                self.text.insert('end', item[x][1])
            self.text.window_create('end', window=self.window[x])
            self.text.insert('end', '\n')
        # Scale & Listbox
        self.text.config(state='disabled')
        # Window
    def get_frame(self):
        return self.frame
    def config(self, msg=''):
        if msg != '':
            self.label = Label(self.frame, text=msg)
            self.text.window_create('1.0', window=self.label)
            self.text.insert('1.1', '\n')
        else:
            self.label.forget()
    def get(self):
        result = []
        for x in (0, len(self.window) - 1):
            if self.window_list[x] == 'scale':
                result.append(self.window[x].get())
            elif self.window_list[x] == 'listbox':
                for y in range(0, len(self.item[x][2])):
                    if self.window[x].selection_includes(y) == 1:
                        result.append(self.item[x][2][y])
                        break
                if len(result) < x + 1:
                    result.append(self.item[x][2][0])
            elif self.window_list[x] == 'radiobutton':
                result.append(self.item[x][3].get())
            else:
                raise SystemExit
        return result

class SingleChoices():
    def __init__(self, tkinter_attribute, msg='', msg_variable=None, args=(('a', 'b', 'c'), ('e', 'f', 'g')), width=100, height=100):
        self.tk = tkinter_attribute
        self.frame = Frame(self.tk, width=width, height=height)
        # Tkinter
        self.text = Text(self.frame, width=width, height=height)
        self.text.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
        # Text
        if msg != '' or msg_variable != None:
            if msg_variable != None:
                self.label = Label(self.frame, variable=msg_variable)
            else:
                self.label = Label(self.frame, text=msg)
            self.text.window_create('end', window=self.label)
            self.text.insert('end', '\n')
        # Label
        self.value_list = []
        lf_list = []
        times = 0
        for x in args:
            if type(x[0]) == type(1):
                self.value_list.append(IntVar())
            else:
                self.value_list.append(StringVar())
            # Value
            lf_list.append(LabelFrame(self.frame, text=str(times + 1)))
            self.text.window_create('end', window=lf_list[-1])
            self.text.insert('end', '\n')
            # LabelFrame
            for y in x:
                Radiobutton(lf_list[times], text=y, variable=self.value_list[times], value=y).pack(side='left')
            # Tkinter
            times += 1
        # Checkbutton
        self.text.config(state='disabled')
        # Window
    def get_frame(self):
        return self.frame
    def config(self, msg=''):
        if msg != '':
            self.label = Label(self.frame, text=msg)
            self.text.window_create('1.0', window=self.label)
            self.text.insert('1.1', '\n')
        else:
            self.label.forget()
    def get(self):
        get = []
        for x in self.value_list:
            get.append(x.get())
        return get

class AnswerSheet():
    def __init__(self, tkinter_attribute, msg='', msg_variable=None, args=[('a', 'b', 'c')], answer=['a'], points=[1], width=100, height=100):
        self.answer = answer
        self.points = points
        # Value
        self.tk = tkinter_attribute
        self.frame = Frame(self.tk, width=width, height=height)
        # Tkinter
        self.text = Text(self.frame, width=width, height=height)
        self.text.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
        # Text
        if msg != '' or msg_variable != None:
            if msg_variable != None:
                self.label = Label(self.frame, variable=msg_variable)
            else:
                self.label = Label(self.frame, text=msg)
            self.text.window_create('end', window=self.label)
            self.text.insert('end', '\n')
        # Label
        self.value_list = []
        lf_list = []
        times = 0
        for x in args:
            if type(x[0]) == type(1):
                self.value_list.append(IntVar())
            else:
                self.value_list.append(StringVar())
            # Value
            lf_list.append(LabelFrame(self.frame, text=str(times + 1)))
            self.text.window_create('end', window=lf_list[-1])
            self.text.insert('end', '\n')
            # LabelFrame
            for y in x:
                Radiobutton(lf_list[times], text=y, variable=self.value_list[times], value=y).pack(side='left')
            # Tkinter
            times += 1
        # Checkbutton
        self.text.config(state='disabled')
        # Window
    def get_frame(self):
        return self.frame
    def config(self, msg=''):
        if msg != '':
            self.label = Label(self.frame, text=msg)
            self.text.window_create('1.0', window=self.label)
            self.text.insert('1.1', '\n')
        else:
            self.label.forget()
    def get(self):
        get = []
        for x in self.value_list:
            get.append(x.get())
        # Get
        point = 0
        for x in range(0, len(get)):
            if get[x] == self.answer[x]:
                point += self.points[x]
        return [get, point]
