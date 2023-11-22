from typing import List
import tkinter as tk
from tkinter import scrolledtext
from abc import ABC, abstractmethod
from datetime import datetime

class Memento(ABC):
    @abstractmethod
    def get_state(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass

class ConcreteMemento(Memento):
    def __init__(self, state: str) -> None:
        self.state: str = state
        self.date: str = str(datetime.now())[:19]

    def get_state(self) -> str:
        return self.state

    def get_name(self) -> str:
        return f'{self.date};({self.state[0:17]}...)'

    def get_date(self) -> str:
        return self.date

class Originator:
    state: str = ""

    def __init__(self, state: str) -> None:
        self.state = state

    def set_state(self, state: str) -> None:
        self.state = state

    def save(self) -> Memento:
        return ConcreteMemento(self.state)

    def restore(self, memento: Memento) -> None:
        self.state = memento.get_state()

    def get_state(self) -> str:
        return self.state

class Caretaker:
    def __init__(self, originator: Originator) -> None:
        self.mementos: List[Memento] = []
        self.originator: Originator = originator

    def backup(self) -> None:
        self.mementos.append(self.originator.save())

    def undo(self) -> None:
        if not len(self.mementos): return None
        
        memento = self.mementos.pop()
        self.originator.restore(memento)

    def show_history(self) -> None:
        print('History:')
        for memento in self.mementos:
            print(memento.get_name())

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('VSTE: Very Simple Text Editor')
        
        self.text_area: scrolledtext.ScrolledText = scrolledtext.ScrolledText(self.window, wrap = tk.WORD, width = 47, height = 27)
        self.text_area.pack(padx = 10, pady = 10, expand = True, fill = 'both')
        self.text_area.config(font=('TkDefaultFont', 18))
        
        self.originator: Originator = Originator("")
        self.caretaker: Caretaker = Caretaker(self.originator)
        
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        menu.add_command(label='Save state', command = self.save_state)
        menu.add_command(label='Restore state', command = self.restore_state)
        menu.add_command(label='Show history', command = self.show_history)

        self.text_area.bind('<Control-s>', self.save_state)
        self.text_area.bind('<Control-r>', self.restore_state)
        self.text_area.bind('<Control-h>', self.show_history)
        
        self.window.mainloop()

    def save_state(self, event = None):
        state = self.text_area.get('1.0', tk.END)
        self.originator.set_state(state)
        self.caretaker.backup()
        print('Saved state.')

    def restore_state(self, event = None):
        self.caretaker.undo()
        state = self.originator.get_state().rstrip('\n')
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, state)
        print('Restore state.')
        
    def show_history(self, event = None):
        self.caretaker.show_history()

if __name__ == '__main__':
    TextEditor()