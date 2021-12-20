import tkinter as tk
from tkinter import ttk
from tkinter import font,colorchooser,filedialog,messagebox
import os

mainapp = tk.Tk()
mainapp.geometry('800x400')
mainapp.title('vpad text editor')
mainapp.wm_iconbitmap('icon.ico')

##################################   main menu   ##############################
mainmenu = tk.Menu()

file = tk.Menu(mainmenu , tearoff = False)
newicon = tk.PhotoImage(file ='icons2/new.png')
openicon = tk.PhotoImage(file ='icons2/open.png')
saveicon = tk.PhotoImage(file ='icons2/save.png')
saveasicon = tk.PhotoImage(file ='icons2/save_as.png')
exiticon = tk.PhotoImage(file ='icons2/exit.png')
# file.add_command(label = 'New' , image = newicon , compound = tk.LEFT)

# new file functionality
url = ''
def newfile(event = None):
    global url
    url = ''
    texteditor.delete(1.0,tk.END)
file.add_command(label = 'New',image = newicon , compound = tk.LEFT, accelerator = 'Ctrl+N',command = newfile)

# open functionality
def openfile(event = None):
    global url
    url = filedialog.askopenfilename(initialdir = os.getcwd(),title = 'Select File : ',filetypes = (('Text File','*.txt'),('All Files','*.*')))
    try:
        with open(url,'r') as fr:
            texteditor.delete(1.0,tk.END)
            texteditor.insert(1.0,fr.read())
    except FileNotFoundError:
        return
    except :
        return
    mainapp.title(os.path.basename(url))
file.add_command(label = 'Open',image = openicon , compound = tk.LEFT, accelerator = 'Ctrl+O',command = openfile)

# save functionality
def savefile(event = None):
    global url
    try:
        if url:
            content = str(texteditor.get(1.0,tk.END))
            with open(url , 'w' , encoding='utf-8') as fw:
                fw.write(content)
        else:
            url = filedialog.asksaveasfile(mode = 'w',defaultextension = '.txt',filetypes = (('Text File','*.txt'),('All Files','*.*')))
            content2 = texteditor.get(1.0,tk.END)
            url.write(content2)
            url.close()
    except:
        return

file.add_command(label = 'Save',image = saveicon ,compound = tk.LEFT, accelerator = 'Ctrl+S',command = savefile)

# save as functionality
def saveasfile(event = None):
    global url
    try:
        content2 = texteditor.get(1.0,tk.END)
        url = filedialog.asksaveasfile(mode = 'w',defaultextension = '.txt',filetypes = (('Text File','*.txt'),('All Files','*.*')))
        url.write(content2)
        url.close()
    except:
        return
file.add_command(label = 'Save As',image = saveasicon , compound = tk.LEFT, accelerator = 'Ctrl+Alt+S',command = saveasfile)

# exit functionality
def exitfunc(event = None):
    global url,textchanged
    try:
        if textchanged:
            mbox = messagebox.askyesnocancel('Warning','Do You want to save this File ? ')
            if mbox is True:
                if url:
                    content = texteditor.get(1.0,tk.END)
                    with open(url,'w',encoding='utf-8') as fw:
                        fw.write(content)
                        mainapp.destroy()
                else:
                    content2 = str(texteditor.get(1.0,tk.END))
                    url = filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes = (('Text File','*.txt'),('All Files','*.*')))
                    url.write(content2)
                    url.close()
                    mainapp.destroy() 
            elif mbox is False:
                mainapp.destroy()
        else:
            mainapp.destroy()
    except:
        return

file.add_command(label = 'Exit',image = exiticon, compound = tk.LEFT, accelerator = 'Ctrl+Q',command = exitfunc)


edit = tk.Menu(mainmenu , tearoff = False)
copyicon = tk.PhotoImage(file = 'icons2/copy.png') 
pasteicon = tk.PhotoImage(file = 'icons2/paste.png') 
cuticon = tk.PhotoImage(file = 'icons2/cut.png') 
findicon = tk.PhotoImage(file = 'icons2/find.png') 
edit.add_command(label = 'Copy',image = copyicon , compound = tk.LEFT,accelerator = 'Ctrl+C',command=lambda:texteditor.event_generate("<Control c>"))
edit.add_command(label = 'Paste', image = pasteicon , compound = tk.LEFT,accelerator = 'Ctrl+V',command=lambda:texteditor.event_generate("<Control v>"))
edit.add_command(label = 'Cut', image = cuticon , compound = tk.LEFT,accelerator = 'Ctrl+X',command=lambda:texteditor.event_generate("<Control x>"))

# find functionality
def findfunc(event = None):
    def findfunc(event=None):
        word = findinput.get()
        texteditor.tag_remove('match','1.0',tk.END)
        matches = 0
        if word:
            startpos = '1.0'
            while True:
                startpos = texteditor.search(word,startpos,stopindex=tk.END)
                if not startpos:
                    break
                endpos = f'{startpos}+{len(word)}c'
                texteditor.tag_add('match',startpos,endpos)
                matches += 1
                startpos = endpos
                texteditor.tag_config('match',foreground = 'red' , background = 'yellow')
    def replacefunc(event = None):
        word = findinput.get()
        replacetext = replaceinput.get()
        content = texteditor.get(1.0,tk.END)
        newcontent = content.replace(word,replacetext)
        texteditor.delete(1.0,tk.END)
        texteditor.insert(1.0,newcontent)

    finddialogue = tk.Toplevel()
    finddialogue.geometry('450x250+500+200')
    finddialogue.title('Find')
    finddialogue.resizable(0,0)

    # frame
    findframe = ttk.LabelFrame(finddialogue,text = 'Find/Replace')
    findframe.pack(pady = 50)

    #labels
    findlabel = ttk.Label(findframe,text = 'Find : ')
    replacelabel = ttk.Label(findframe,text = 'Replace : ')
    findlabel.grid(row = 0,column = 0 , padx = 5 , pady = 4)
    replacelabel.grid(row = 1,column = 0 , padx = 5 , pady = 4)
    
    # entry
    findinput = ttk.Entry(findframe,width = 30)
    replaceinput = ttk.Entry(findframe,width = 30)
    findinput.grid(row = 0,column = 1 , padx = 5 , pady = 5)
    replaceinput.grid(row = 1,column = 1 , padx = 5 , pady = 5)

    # buttons
    findbtn = ttk.Button(findframe,text = 'Find',command = findfunc)
    replacebtn = ttk.Button(findframe,text = 'Replace',command = replacefunc)
    findbtn.grid(row = 2 , column = 0 , padx = 10 , pady = 5)
    replacebtn.grid(row = 2 , column = 1 , padx = 10 , pady = 5)

    finddialogue.mainloop()

edit.add_command(label = 'Find', image = findicon , compound = tk.LEFT,accelerator = 'Ctrl+F',command=findfunc)

view = tk.Menu(mainmenu , tearoff = False)
toolbaricon = tk.PhotoImage(file = 'icons2/tool_bar.png')
statusbaricon = tk.PhotoImage(file = 'icons2/status_bar.png')

showtoolbar = tk.BooleanVar()
showstatusbar = tk.BooleanVar()
showtoolbar.set(True)
showstatusbar.set(True)

def hidetoolbar():
    global showtoolbar
    if showtoolbar:
        toolbar.pack_forget()
        showtoolbar = False
    else:
        texteditor.pack_forget()
        statusbar.pack_forget()
        toolbar.pack(side = tk.TOP, fill = tk.X)
        texteditor.pack(fill = tk.BOTH, expand = True)
        statusbar.pack(side = tk.BOTTOM)
        showtoolbar = True

def hidestatusbar():
    global showstatusbar
    if showstatusbar:
        statusbar.pack_forget()
        showstatusbar = False
    else:
        statusbar.pack(side = tk.BOTTOM)
        showstatusbar = True

view.add_checkbutton(label = 'Tool bar',onvalue = 1 , offvalue = 0 ,variable = showtoolbar ,image = toolbaricon,compound = tk.LEFT,command = hidetoolbar)
view.add_checkbutton(label = 'Status bar',onvalue = 1 , offvalue = 0 ,variable = showstatusbar ,image = statusbaricon,compound = tk.LEFT,command = hidestatusbar)


colortheme = tk.Menu(mainmenu , tearoff = False)
lightdefault = tk.PhotoImage(file = 'icons2/light_default.png')
lightplus = tk.PhotoImage(file = 'icons2/light_plus.png')
dark = tk.PhotoImage(file = 'icons2/dark.png')
red = tk.PhotoImage(file = 'icons2/red.png')

themechoice = tk.StringVar()
coloricons = (lightdefault,lightplus,dark,red) 
colordict = {
    'Light Default' : ('#000000' , '#ffffff'),
    'Light Plus' : ('#474747' , '#e0e0e0'),
    'Dark' : ('#c4c4c4' , '#2d2d2d'),
    'Red' : ('#2d2d2d' , '#ffe8e8')
}

def changetheme():
    chosentheme = themechoice.get()
    colortuple = colordict.get(chosentheme)
    fgcolor , bgcolor = colortuple[0] , colortuple[1]
    texteditor.config(background=bgcolor , foreground=fgcolor)

count = 0
for i in colordict:
    colortheme.add_radiobutton(label = i , image = coloricons[count],variable = themechoice , compound = tk.LEFT,command = changetheme)
    count += 1
mainmenu.add_cascade(label = 'File' , menu = file)
mainmenu.add_cascade(label = 'Edit' , menu = edit)
mainmenu.add_cascade(label = 'View' , menu = view)
mainmenu.add_cascade(label = 'Color Theme' , menu = colortheme)

######################## toolbar... ################################
toolbar = ttk.Label(mainapp)
toolbar.pack(side = tk.TOP , fill =tk.X)
#font box
fonttuple = tk.font.families()
fontfamily = tk.StringVar()
fontbox = ttk.Combobox(toolbar , width = 30,textvariable = fontfamily,state = 'readonly')
fontbox['values'] = fonttuple
fontbox.current(fonttuple.index('Arial'))
fontbox.grid(row = 0 , column = 0 , padx = 5)
#size box
sizevar = tk.IntVar()
fontsize = ttk.Combobox(toolbar,width=5,textvariable = sizevar,state = 'readonly')
fontsize['values'] = tuple(range(0,100,2))
fontsize.current(8)
fontsize.grid(row = 0 , column = 1 , padx = 5)
#bold button
boldicon = tk.PhotoImage(file = 'icons2/bold.png')
boldbtn = ttk.Button(toolbar , image = boldicon)
boldbtn.grid(row = 0 , column = 2 , padx = 5)
#italic
italicicon = tk.PhotoImage(file = 'icons2/italic.png')
italicbtn = ttk.Button(toolbar , image = italicicon)
italicbtn.grid(row = 0,column = 3 , padx = 5)
#underline
underlineicon = tk.PhotoImage(file = 'icons2/underline.png')
underlinebtn = tk.Button(toolbar , image = underlineicon)
underlinebtn.grid(row = 0 , column = 4 , padx = 5)
#font color button
fontcoloricon = tk.PhotoImage(file = 'icons2/font_color.png')
fontcolorbtn = ttk.Button(toolbar , image = fontcoloricon)
fontcolorbtn.grid(row = 0 , column = 5 , padx = 5)
#align left
alignlefticon = tk.PhotoImage(file = 'icons2/align_left.png')
alignleftbtn = ttk.Button(toolbar , image = alignlefticon)
alignleftbtn.grid(row = 0 , column = 6 , padx = 5)
#align center
aligncentericon = tk.PhotoImage(file = 'icons2/align_center.png')
aligncenterbtn = ttk.Button(toolbar , image = aligncentericon)
aligncenterbtn.grid(row = 0 , column = 7 , padx = 5)
#align right
alignrighticon = tk.PhotoImage(file = 'icons2/align_right.png')
alignrightbtn = ttk.Button(toolbar , image = alignrighticon)
alignrightbtn.grid(row = 0 , column = 8 , padx = 5)

########################## text editor #################################
texteditor = tk.Text(mainapp)
texteditor.config(wrap = 'word',relief = tk.FLAT)
scrollbar = tk.Scrollbar(mainapp)
texteditor.focus_set()
scrollbar.pack(side = tk.RIGHT,fill = tk.Y)
texteditor.pack(fill = tk.BOTH,expand = True)
scrollbar.config(command = texteditor.yview)
texteditor.config(yscrollcommand = scrollbar.set)

#font and size
currentfontfamily = 'Arial'
currentfontsize = 12

def changefont(mainapp):
    global currentfontfamily
    currentfontfamily = fontfamily.get()
    texteditor.configure(font = (currentfontfamily,currentfontsize))

def changefontsize(mainapp):
    global currentfontsize
    currentfontsize = sizevar.get()
    texteditor.configure(font = (currentfontfamily,currentfontsize))


fontbox.bind("<<ComboboxSelected>>",changefont)
fontsize.bind("<<ComboboxSelected>>",changefontsize)

# buttons functionality..
#bold
def changebold():
    textpropety = tk.font.Font(font = texteditor['font'])
    if textpropety.actual()['weight'] == 'normal':
        texteditor.configure(font=(currentfontfamily,currentfontsize,'bold'))

    if textpropety.actual()['weight'] == 'bold':
        texteditor.configure(font=(currentfontfamily,currentfontsize,'normal'))
  
boldbtn.configure(command = changebold)

#italic
def changeitalic():
    textpropety = tk.font.Font(font = texteditor['font'])
    if textpropety.actual()['slant'] == 'roman':
        texteditor.configure(font=(currentfontfamily,currentfontsize,'italic'))

    if textpropety.actual()['slant'] == 'italic':
        texteditor.configure(font=(currentfontfamily,currentfontsize,'roman'))
  
italicbtn.configure(command = changeitalic)

# underline
def changeunderline():
    textpropety = tk.font.Font(font = texteditor['font'])
    if textpropety.actual()['underline'] == 0:
        texteditor.configure(font=(currentfontfamily,currentfontsize,'underline'))

    if textpropety.actual()['underline'] == 1:
        texteditor.configure(font=(currentfontfamily,currentfontsize,'normal'))
  
underlinebtn.configure(command = changeunderline)

#font color functionality
def changefontcolor():
    colorvar = tk.colorchooser.askcolor()
    texteditor.configure(fg = colorvar[1])

fontcolorbtn.configure(command = changefontcolor)

#align functionality
def alignleft():
    textcontent = texteditor.get(1.0,'end')
    texteditor.tag_config('left' , justify = tk.LEFT)
    texteditor.delete(1.0,tk.END)
    texteditor.insert(tk.INSERT,textcontent,'left')

alignleftbtn.configure(command = alignleft)

def alignright():
    textcontent = texteditor.get(1.0,'end')
    texteditor.tag_config('right' , justify = tk.RIGHT)
    texteditor.delete(1.0,tk.END)
    texteditor.insert(tk.INSERT,textcontent,'right')

alignrightbtn.configure(command = alignright)

def aligncenter():
    textcontent = texteditor.get(1.0,'end')
    texteditor.tag_config('center' , justify = tk.CENTER)
    texteditor.delete(1.0,tk.END)
    texteditor.insert(tk.INSERT,textcontent,'center')

aligncenterbtn.configure(command = aligncenter)

texteditor.configure(font = ('Arial' , 12))

############################## status bar #############################
statusbar = ttk.Label(mainapp , text = 'Status Bar')
statusbar.pack(side = tk.BOTTOM)

textchanged = False
def changed(event = None):
    global textchanged
    if texteditor.edit_modified():
        textchanged = True
        words = len(texteditor.get(1.0,'end - 1c').split())
        characters = len(texteditor.get(1.0,'end - 1c'))
        statusbar.config(text = f'Characters : {characters}   &&   Words : {words}')
    texteditor.edit_modified(False)

texteditor.bind("<<Modified>>",changed)

mainapp.config(menu = mainmenu)

# bind shortcut keys
mainapp.bind("<Control-n>",newfile)
mainapp.bind("<Control-o>",openfile)
mainapp.bind("<Control-s>",savefile)
mainapp.bind("<Control-Alt-s>",saveasfile)
mainapp.bind("<Control-q>",exitfunc)
mainapp.bind("<Control-f>",findfunc)

mainapp.mainloop()