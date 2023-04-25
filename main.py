import tkinter as tk
from tkinter import messagebox
import pathlib
# import os

# Application Window Variables:
WIN_BG = "dim grey"
WIN_HEADING = "dark red"
WIN_BODY = "white"
WIN_FONT = "arial 12 bold"

# Widget Variables:
ENT_WIDTH = 50
FR_BORDER = 3
LBL_FONT = "arial 12"
FR_RELIEF = tk.GROOVE
# widgets = []
results = []
lbl_list = [
    ("path", "Enter folder path: "), 
    ("delim", "Enter delimiter filter: "), 
    ("ext", "Enter extension type: ")
    ]


# Widget Object:
class QueryWidget:
    def __init__(self, window, widget, query):
        self.widget = widget
        self.query = query

        # Draw 
        self.frame = tk.Frame(master=window, relief=FR_RELIEF, borderwidth=FR_BORDER, bg=WIN_BG)
        self.label = tk.Label(master=self.frame, text=self.query, fg=WIN_BODY, bg=WIN_BG, font=(LBL_FONT))
        self.entry = tk.Entry(master=self.frame, width=ENT_WIDTH, justify="center")
        self.frame.pack(fill=tk.X, padx=2, pady=2)
        self.label.pack()
        self.entry.pack(fill=tk.X)

    def getEntry(self):
        return self.entry.get()

    def clearEntry(self):
        return self.entry.delete(0, tk.END)
         

def main(widgets):
    if getInputs(widgets):
        path = results[0]
        delim = results[1]
        ext = results[2]

        rename_func(path, delim, ext)


def rename_func(path, delim, ext):
    print("== File-Renamer ==")
    p = pathlib.Path(path)
    files = p.iterdir()

    for filenames in files:
        if ext in str(filenames):
            print("Original:", filenames) ## Check original filename
            new = getNewFileName(str(filenames), delim, ext)
            # print("first", new) ## Check new filename
            if new != None:
                newPath = p / new
                newFile = pathlib.Path(newPath)
                print("Renamed:", newFile) ## Check renamed filename
                pathlib.Path.rename(filenames, newFile)


def getNewFileName(filename, delim, ext):
    file = filename.split("\\")[-1]
    filteredName = file.split(delim)[0]
    if filteredName != file:
        newName = filteredName + ext
        return newName


# Retrieve Entry Inputs:
def getInputs(widgets):
    # Get Widget Inputs:
    if bool(results) == False: # If empty list append input
        for widget in widgets:
            results.append(widget.getEntry())
    else: # If not empty list update entries only if modified
        for i, widget in enumerate(widgets):
            currentEntry = widget.getEntry()
            if results[i] != currentEntry:
                    results[i] = currentEntry

    # Handle Blank Inputs:
    if results[0] == "": # Path
        results[0] = pathlib.Path(__file__).parent.absolute()
    if results[1] == "": # Delim
        results[1] = " - "
    if results[2] == "": # Ext
        results[2] = "txt"
    if "." not in results[2]:
       results[2] = "".join((".", results[2]))

    # Confirm Inputs with User:
    message = ""
    for i in range(0, len(lbl_list)):
        tempmessage = f"{lbl_list[i][0].upper()}: \"{results[i]}\"\n"
        message += tempmessage
    confirm = messagebox.askokcancel("Confirm Input", message)
    return confirm

def clearInputs(widgets):
    for widget in widgets:
        widget.clearEntry()
    results.clear()

def gui():
    # Window
    window = tk.Tk()
    window.geometry("400x260")
    title = "Batch File Renamer"
    window.configure(bg=WIN_BG)
    window.title(title)
    
    # Title
    fr_title = tk.Frame(master=window).pack()
    lbl_title = tk.Label(master=fr_title, text=title, fg=WIN_HEADING, bg=WIN_BG, font=("arial 16 bold")).pack()

    # Query Widgets
    widgets = []
    for widget, query in lbl_list:
        widgets.append(QueryWidget(window, widget, query))

    # Buttons
    fr_btn = tk.Frame(master=window).pack(padx=3, pady=3)
    btn_run = tk.Button(master=fr_btn, text="Run", width=10, height=1, fg=WIN_HEADING, font=WIN_FONT, command=lambda: main(widgets)).pack()
    btn_clear = tk.Button(master=fr_btn, text="Clear", width=5, height=1, font="arial 10 bold", command=lambda: clearInputs(widgets)).pack()
    window.bind("<Return>", lambda event: eventHandler(event, widgets))
    
    window.mainloop()

def eventHandler(event, widgets):
    key = event.keysym
    if key == "Return":
        main(widgets)

if __name__ == "__main__":
    gui()
    # tester()