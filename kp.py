from collections import OrderedDict
import json
from operator import itemgetter
import tkinter as tk
from tkinter import ttk


# 50戦した結果

class MainFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("kp")
        self.pack()
        self.load()
        self.arrange()

    def load(self):
        with open("kp.json", "r") as f:
            od = json.load(
                f,
                object_pairs_hook=OrderedDict,
            )
        self.games = od["games"]
        self.kp = od["kp"]

    def save(self):
        self.kp = OrderedDict(
            sorted(
                sorted(
                    self.kp.items(),
                    key=itemgetter(0),
                ),
                key=itemgetter(1),
                reverse=True,
            )
        )
        with open("kp.json", "w") as f:
            json.dump(
                {"games": self.games, "kp": self.kp},
                f,
                indent=4,
            )

    def arrange(self):
        self.leftframe = ttk.Frame(self)
        self.leftframe.pack(side=tk.LEFT)
        self.entrys = [ttk.Entry(
            self.leftframe,
            width=13,
        ) for _ in range(6)]
        for e in self.entrys:
            e.pack()
        self.submit = ttk.Button(
            self.leftframe,
            text="submit",
            command=self.increment
        )
        self.submit.pack()

        self.rightframe = ttk.Frame(self)
        self.rightframe.pack(side=tk.LEFT)
        self.bouts = ttk.Label(
            self.rightframe,
            text=f"{self.games} games",
        )
        self.bouts.pack()
        self.tree = ttk.Treeview(
            self.rightframe,
        )
        self.tree["columns"] = (1, 2)
        self.tree["show"] = "headings"
        self.tree.column(1, width=100)
        self.tree.column(2, width=35)
        self.tree.heading(1, text="Name")
        self.tree.heading(2, text="kp")
        for i, v in enumerate(self.kp.items()):
            self.tree.insert("", tk.END, tags=i%2, values=v)
        self.tree.tag_configure(1, background="#EEFFFF")
        self.tree.pack()

    def increment(self):
        self.games += 1
        for e in self.entrys:
            k = e.get()
            if k:
                self.kp[k] = self.kp.get(k, 0)+1
            e.delete(0, tk.END)
        self.save()
        self.tree.delete(*self.tree.get_children())
        for i, v in enumerate(self.kp.items()):
            self.tree.insert("", tk.END, tags=i%2, values=v)


if __name__ == "__main__":
    root = tk.Tk()
    mf = MainFrame(master=root)
    mf.mainloop()
    