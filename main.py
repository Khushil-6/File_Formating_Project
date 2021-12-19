# importing appropriate library
import pandas as pd
try:
    import Tkinter as Tk
    import tkFileDialog as fileDialog
    from tkinter import *
    from Tkinter import *
except ImportError:
    import tkinter as Tk
    from tkinter import filedialog as fileDialog


#Applying XML format
def applyXML(row):
    xml = ['<point>']
    for field in row.index:
        xml.append('  <{0}>{1}</{0}>'.format(field, row[field]))
    xml.append('</point>')
    return '\n'.join(xml)


#Processing XML for the file
def processXML(df):
    file1 = open('file.xml', 'w')
    file1.write('<?xml version="1.0" encoding="UTF-8" ?>\n<points>\n')
    file1.writelines('\n'.join(df.apply(applyXML, axis=1)))
    file1.write('\n</points>')
    file1.close()

# Opening File
def openFile():
    filename = fileDialog.askopenfilename()
    # Reading the file and adding appropriate headers
    df = pd.read_csv(filename, sep='\t', names=['Date', 'Time', 'Speed', 'Distance', 'Description'])

    # Changing format for date and time
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
    df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%H:%M:%S')
    df['Date'] = df['Date'].dt.strftime('%Y.%d.%m')

    # Changing speed and distance format
    for i in df.index:
        tmp = '.'.join((df["Distance"][i].split(',')))
        df["Speed"][i] *= 1.94385
        df["Distance"][i] = float(tmp) / 1.852

    selc = selection()
    if selc == 1:
        df.to_csv('file.csv')
    elif selc == 2:
        processXML(df)
    txt = "Completed!!!"
    textVar.set(txt)
    alert('Completed', 'The formated file is placed in the application folder')


#Choosing the right format to update
def selection():
   if radio.get() == 1:
        return 1
   elif radio.get() == 2:
        return 2

#Alert box
def alert(title, message, kind='info', hidemain=True):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')
    show_method = getattr(Tk.messagebox, 'show{}'.format(kind))
    show_method(title, message)


# Main
root = Tk.Tk()
radio = Tk.IntVar()
root.geometry("300x200")
pd.options.mode.chained_assignment = None

#Header of the APP
lbl = Tk.Label(text = "Converting file to?", font=("Helvetica", 11))
lbl.grid(row=0, sticky='w')

#CSV radio button
radio1 = Tk.Radiobutton(root, text="CSV", variable=radio, value=1, command=selection, font=("Helvetica", 11))
radio1.grid(row=2, padx=3 ,sticky='w')

#XML Radio button
radio2 = Tk.Radiobutton(root, text="XML", variable=radio, value=2, command=selection, font=("Helvetica", 11))
radio2.grid(row=2,column=3)

#Submit button
button = Tk.Button(root, text="Open", command=openFile, font=("Helvetica", 11))
button.grid(row=7, pady=8 ,sticky='w')

#Sucess message
textVar = Tk.StringVar(root)
label = Tk.Label(root, textvariable=textVar, font=("Helvetica", 11))
label.grid(row=10 )

root.mainloop()
