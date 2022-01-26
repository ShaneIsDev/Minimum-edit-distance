from tkinter import *
from tkinter.font import Font
# pip install pillow
from PIL import ImageTk, Image
#   pip install numpy 
import numpy as np
# change color for the box when back tracking:
def Box_updater(b, c, t):
    j,i = c
    box_size = 50
    padding = 20
    box_gap = 10
    y = (box_gap + box_size)*(j+1) + padding
    x = (box_gap + box_size)*(i+1) + padding
    arrow = {
        'd':'←',
        'r':'↖',
        'n':'↖',
        'i':'↑',

    }
    # create boxes and write text in the box:
    b.create_rectangle(x, y, x + box_size, y + box_size, fill = '#7d5fff', outline = "")
    if i == 0 and j == 0:
        text = t[j,i][:-1]
    else:
        text = t[j,i].replace(t[j,i][-1], arrow[t[j,i][-1]])
    b.create_text(x+box_size/2, y+box_size/2, text = text, font = mFont)
    rt.update()
# write txt in a location x,y
def write_xy(x, y, c, bg):
    bg.create_text(x, y, text = c, font = mFont)
    rt.update()
# Display result distance:
def Show_Edit_Distance(distance, bg):
    bg.create_text(w/2 + 360, h/2 - 300, text = "Total Steps: " + str(distance), font = mFont)
    rt.update()
# Check input if it's legal or not
def Input_Handler(a, b):
    s1 = a.get()
    s2 = b.get()
    if s1 == '' or s2 == '': 
        #empty input case:
        Error_Handler = Toplevel(rt)
        Error_Handler.geometry("250x90")
        Error_Handler.title("Warning!")
        Label(Error_Handler, text = "Please enter both strings").pack()
        Button(Error_Handler, text = "OK", command = Error_Handler.destroy).pack()
    elif not(s1.isalpha()) or not(s2.isalpha()):
        # non-alphabet case:
        Error_Handler = Toplevel(rt)
        Error_Handler.geometry("250x90")
        Error_Handler.title("Warning!")
        Label(Error_Handler, text = "Both should be Strings only.").pack()
        Button(Error_Handler, text = "OK", command = Error_Handler.destroy).pack()
    else:
        ## display the table on screen:
        init_Table(s1.lower(), s2.lower())
def calc_table(a, b):
    ## init table
    tb = np.zeros([len(a)+1, len(b)+1], dtype=np.dtype('U3'))
    ## base cases:
    for i in range(len(a)+1):
        tb[i,0] = str(i) + 'i'
    for j in range(len(b)+1):
        tb[0,j] = str(j) + 'd'
    #use formula dp[i][j]:
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            if a[i-1] == b[j-1]:
                tb[i, j] = tb[i-1, j-1][:-1] + 'n'
            else:
                if min(int(tb[i-1, j-1][:-1]), int(tb[i-1, j][:-1]), int(tb[i, j-1][:-1])) == int(tb[i-1, j-1][:-1]):
                    tb[i,j] = str(int(tb[i-1, j-1][:-1]) + 1) + 'r'
                elif min(int(tb[i-1, j-1][:-1]), int(tb[i-1, j][:-1]), int(tb[i, j-1][:-1])) == int(tb[i, j-1][:-1]):
                    tb[i,j] = str(int(tb[i, j-1][:-1]) + 1) + 'd'
                elif min(int(tb[i-1, j-1][:-1]), int(tb[i-1, j][:-1]), int(tb[i, j-1][:-1])) == int(tb[i-1, j][:-1]):
                    tb[i,j] = str(int(tb[i-1, j][:-1]) + 1) + 'i'

    # show total edit distance:
    return tb
def calc_changes_str(table, str1, str2):
    i = len(str1)
    j = len(str2)
    #init changes list:
    changes_list = []
    #init path list
    path_list = []
    #set guardian:
    guard = 0
    changing_str = list(str2)
    while i >= 0:
        if guard == 1:
            break
        while j >= 0:
            if table[i,j][-1] == 'n':
                path_list.append([i,j])
                j-=1
                i-=1
            elif table[i,j][-1] == 'r':
                statement1 = str(str2[j-1]).upper() + ' changed to ' + str(str1[i-1]).upper()
                changing_str[j-1] = str1[i-1]
                statement2 = 'New string: ' + ''.join(changing_str)
                changes_list.append([statement1,statement2])
                path_list.append([i,j])
                i-=1
                j-=1
            elif table[i,j][-1] == 'i':
                statement1 = 'Insert ' + str(str1[i-1]).upper() + ' at position ' + str(j+1) + ' in string'
                changing_str.insert(j, str1[i-1])
                statement2 = 'New string: ' + ''.join(changing_str)
                changes_list.append([statement1,statement2])
                path_list.append([i,j])
                i-=1
            elif table[i,j][-1] == 'd':
                statement1 = 'Remove ' + str(str2[j-1]).upper()
                del changing_str[j-1]
                statement2 = 'New string: ' + ''.join(changing_str)
                changes_list.append([statement1,statement2])
                path_list.append([i,j])
                j-=1
            if len(changes_list) == int(table[len(str1), len(str2)][:-1]):
                guard = 1
                break
    return changes_list, path_list

# create input screen to input 2 strings:
def init_landing_screen():
    #background
    bg = Canvas(rt, bg = "#c242f5", width = w, height = h)
    bg.grid(row=0, column=0)
    bg.create_text(w/2, h/2 - 350, text = "Minimum Edit Distance", font = bFont)
    bg.create_text(w/2, h/2 - 300, text = "19127558 - Bùi Phú Thịnh", font = mFont)
    bg.create_text(w/2, h/2 - 275, text = "19CNTT - NLP", font = mFont)
    #Create boxes for input:
    bg.create_text(w/2 - 150, h/2 - 200, text = "Enter 1st string: ", font = mFont)
    str1 = Entry(bg)
    bg.create_window(w/2 + 120, h/2 - 200, window = str1, width = w/4)
    bg.create_text(w/2 - 150, h/2 - 100, text = "Enter 2nd string: ", font = mFont)
    str2 = Entry(bg)
    bg.create_window(w/2 + 120, h/2 - 100, window = str2, width = w/4)
    # Button
    b1 = Button(bg, text = "Confirm", bg = 'green', activebackground = '#7842f5', command=lambda:Input_Handler(str1, str2))
    bg.create_window(w/2, h/2, window = b1, width = w/8)
#create full table with elements:
def init_Table(a, b):
    bg = Canvas(rt, bg = "#F6D529", width = w, height = h)
    bg.grid(row=0, column=0)
    b_size = 50
    b_gap = 10
    t_width = len(a) + 2
    t_height = len(b) + 2
    padding = 20
    animate_gap = 100
    pointer = {
        'n':'↖',
        'i':'↑',
        'd':'←',
        'r':'↖',}
    for i in range(t_height):
        for j in range(t_width):
            if (i,j) == (0,0) or (i,j) == (1,0) or (i,j) == (0,1):
                continue
            else:
                x = (b_gap + b_size)*i + padding
                y = (b_gap + b_size)*j + padding
                bg.create_rectangle(x, y, x + b_size, y + b_size, fill = '#c242f5', outline = "")
    for i in range(t_height-2):
        x = (b_gap + b_size)*(i+2) + padding + b_size/2
        bg.create_text(x, padding + b_size/2, text = b[i].upper(), font = mFont)
    for i in range(t_width-2):
        y = (b_gap + b_size)*(i+2) + padding + b_size/2
        bg.create_text(padding + b_size/2, y, text = a[i].upper(), font = mFont)
    formulaOnCanvas = bg.create_image(w/2 + 100, h/2 - 250, anchor=NW, image=formula)
    bg.update()

    edit_table = calc_table(a, b)
    for i in range(edit_table.shape[0]):
        for j in range(edit_table.shape[1]):
            if i == 0 or j == 0:
                x = (b_gap + b_size)*(j+1) + padding + b_size/2
                y = (b_gap + b_size)*(i+1) + padding + b_size/2
                if i == 0 and j == 0:
                    c = edit_table[i,j][:-1]
                else:
                    c = edit_table[i,j].replace(edit_table[i,j][-1], pointer[edit_table[i,j][-1]])
                bg.create_text(x, y, text = c, font = mFont)
    for i in range(edit_table.shape[0]):
        for j in range(edit_table.shape[1]):
            if not(i == 0 or j == 0):
                x = (b_gap + b_size)*(j+1) + padding + b_size/2
                y = (b_gap + b_size)*(i+1) + padding + b_size/2

                c = edit_table[i,j].replace(edit_table[i,j][-1], pointer[edit_table[i,j][-1]])
                bg.after(animate_gap, write_xy(x,y,c,bg))
    Show_Edit_Distance(edit_table[t_width-2, t_height-2][:-1], bg)
    b3 = Button(bg, text = "Show details!", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:Show_changes_list(bg, edit_table, a, b, formulaOnCanvas, button, animate_gap))
    button = bg.create_window(w/2 + 340, h/2 - 60, window = b3, width = w/8)

#Show changes:
def Show_changes_list(bg, ctable, str1, str2, formula, b3, a_gap):
    

    # Delete unnecessary things: 
    bg.delete(b3)
    bg.delete(formula)
    bg.update()
    bg.create_image(w/2 + 40, h/2 - 300, anchor=NW, image=table)
    changes, path = calc_changes_str(ctable, str1, str2)
    for cell in path:
        bg.after(a_gap, Box_updater(bg, cell, ctable))
    if len(changes) == 0:
        bg.create_text(w/2 + 350, h/2 - 30, text = "Same strings! No changes has been made", font = sFont)
        i=1
    else:
        bg.create_text(w/2 + 350, h/2 - 30, text = "Changes in '" + str2 + "' are:", font = mFont)
        for i in range(len(changes)):
            statement = str(i+1) + ". " + changes[i][0] + '. ' + changes[i][1]
            bg.create_text(w/2 + 370, h/2 + i*30, text = statement, font = sFont)
        i+=1
    b2 = Button(bg, text = "Do it again", bg = 'green', activebackground = '#7842f5', command=init_landing_screen)
    bg.create_window(w/2 + 250, h/2 + i*32, window = b2, width = w/8)
    b3 = Button(bg, text = "Exit", bg = 'gray75', activebackground = '#7842f5', command=lambda:rt.destroy())
    bg.create_window(w/2 + 450, h/2 + i*32, window = b3, width = w/8)
  

if __name__ == "__main__":
    rt = Tk()
    w = rt.winfo_screenwidth()
    h = rt.winfo_screenheight()
    #set title:
    rt.geometry("%dx%d" % (w, h))
    rt.title("19127558")
    #fonts:
    sFont = Font(family = 'Times New Roman', size = '12')
    mFont = Font(family = 'Times New Roman', size = '15')
    bFont = Font(family = 'Times New Roman', size = '30')
    #table:
    table = Image.open("edit-distance-square.png")
    table = table.resize((600, 300), Image.ANTIALIAS)
    table = ImageTk.PhotoImage(table)
    init_landing_screen()
    #formula picture:
    formula = Image.open("edit-distance-formula.png")
    formula = formula.resize((500, 128), Image.ANTIALIAS)
    formula = ImageTk.PhotoImage(formula)
    rt.mainloop()