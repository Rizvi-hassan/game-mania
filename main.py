#TODO: TKINTER INIIALIZATION
from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as tkFont
root = Tk()
root.title("Game Mania")


#TODO: Mysql initializaton
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", 
    password = "",
    database = "game-mania"
)
mycursor = mydb.cursor()


# TODO: VARIABLES
win_width = 1000
win_height = 700
uservalue = StringVar()
passvalue = StringVar()

new_uservalue = StringVar()
new_passvalue = StringVar()
re_passvalue = StringVar() 

font1 = tkFont.Font(family = "Rockwell Extra Bold", size = 40, weight = "bold", underline = 1)
font2 = tkFont.Font(family = "Sans Serif", size = 14, weight = "bold")
font3 = tkFont.Font(family = "Rockwell Extra Bold", size = 20, weight = "bold", underline = 1)
current_user = ""

# Dimensions of the window 
root.geometry(f"{win_width}x{win_height}")
root.minsize(win_width, win_height)
root.maxsize(win_width, win_height)


#TODO: FUCNTIONS 

# to hide a widget
def hide_widget(*Widget):
    for item in Widget:
        item.place_forget()

# to show a widget
def show_widget(*Widget):
    for item in Widget:
        item.place(anchor = "c", relx = 0.5, rely = 0.5)

# function to clear the entry area after user inputs
def clear_entry(*boxes):
    for item in boxes:
        item.delete(0, END)

# To show register box and disappear login box: 
def appear_register(widget1, widget2, canvas):
    global change_button, change_text, change_message
    hide_widget(widget1)
    show_widget(widget2)
    canvas.delete(change_button, change_text, change_message)
    change_text = canvas.create_text(500, 200, text = "REGISTER", font = font3)
    change_message = canvas.create_text(400, 500, text = "Have an account? ", font = font2)
    change_button = canvas.create_window(550, 500, window = Button(canvas, text = "Login", font = font2, bg = "grey", command = lambda : appear_login(login_box, register_box, canvas)))

#To show login box and dissapearregister box
def appear_login(widget1, widget2, canvas):
    global change_button, change_text, change_message
    hide_widget(widget2)
    show_widget(widget1)
    canvas.delete(change_button, change_text, change_message)
    change_text = canvas.create_text(500, 200, text = "LOGIN", font = font3)
    change_message = canvas.create_text(400, 500, text = "New user, register: ", font = font2)
    change_button = canvas.create_window(550, 500, window = Button(canvas, text = "Reigster", font = font2, bg = "grey", command = lambda : appear_register(login_box, register_box, canvas)))

#Function to feed the information of register to the database 
def register():
    user, pas, re_pass = new_userentry.get().strip(), new_passentry.get().strip(), re_passentry.get().strip()
    invalid_register.grid_forget()
    if user and pas and re_pass:
        if pas != re_pass:
            invalid_register.grid(row = 2, column = 2)
            return
        else:
            sql = "SELECT username FROM user"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            result = [i[0] for i in myresult]
            if user not in result:
                sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
                val = (user, pas)
                mycursor.execute(sql, val)
                mydb.commit()
                current_user = user
                menu()
            else:
                invalid_register.grid(row = 0, column = 2)
    clear_entry(new_userentry, new_passentry, re_passentry)

# Funcion to Check Login related querry
def login():
    invalid_user.grid_forget()
    user, pas = userentry.get().strip(), passentry.get().strip()
    if user and pas:
        sql = "SELECT username, password FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        userlist = [i[0] for i in myresult]
        passwordlist = [i[1] for i in myresult]
        if user in userlist:
            index = userlist.index(user)
            if pas == passwordlist[index]:
                menu()
            else:
                invalid_user.grid(row = 1, column = 2)
        else:
            invalid_user.grid(row = 0, column = 2)
    clear_entry(userentry, passentry)

# menu box to display different games 
def menu():
    print("Successfull")
    canvas.pack_forget()
    hide_widget(login_box, register_box)

#Intro page
bg1 = Image.open("bg1.jpg")
# bg1 = bg1.resize((win_width, win_height), Image.ANTIALIAS)
bg1 = ImageTk.PhotoImage(bg1)
canvas = Canvas(root, width = win_width, height = win_height, bg = "black" )
canvas.pack(fill = "both")
canvas.create_image(0, 0, image = bg1, anchor = "nw")
canvas.create_text(500, 60, text = "Welcome to Game Mania", font = font1 )
change_text = canvas.create_text(500, 200, text = "LOGIN", font = font3)
change_message = canvas.create_text(400, 500, text = "New user, register: ", font = font2)
change_button = canvas.create_window(550, 500, window = Button(canvas, text = "Reigster", font = font2, bg = "grey", command = lambda : appear_register(login_box, register_box, canvas)))

#login box
login_box = Frame(root, width = 500, height = 200, borderwidth = 5, relief = SUNKEN)
login_box.place(anchor = "c", relx = 0.5, rely = 0.5)

username = Label(login_box, text = "Username", font = "Sans 15 bold", padx = 10, pady = 40)
password = Label(login_box, text = "Password", font = "Sans 15 bold", padx = 10 )
userentry = Entry(login_box, textvariable = uservalue, width = 40, fg = "#312e2e", font = "consolas 10")
passentry = Entry(login_box, textvariable = passvalue, width = 40, fg = "#312e2e", show = "*", font = "consolas 10" )

username.grid(row = 0, column = 0)
password.grid(row = 1, column = 0)
userentry.grid(row = 0, column = 1, padx = 10)
passentry.grid(row = 1, column = 1, padx = 10)

Button(login_box, text = "Enter", font = font2, bg = "grey", command = login ).grid(row = 2 , column = 2, pady = 10, padx = 2)
# TODO: TO PRINT INVALID MESSAGE WHEN USER INPUT WRONG DATA 
invalid_user = Label(login_box, text = "*invalid", font = "Sans 10", fg = "red")
# invalid.grid(row = 0, column = 2)



# Register box
register_box = Frame(root, width = 500, height = 200, borderwidth = 5, relief = SUNKEN)
# register_box.place(anchor = "c", relx = 0.5, rely = 0.5)

new_username = Label(register_box, text = "Username", font = "Sans 15 bold", padx = 10, pady = 40)
new_password = Label(register_box, text = "Password", font = "Sans 15 bold", padx = 10 )
re_password = Label(register_box, text = "Confirm password", font = "Sans 15 bold", padx = 10)

new_userentry = Entry(register_box, textvariable = new_uservalue, width = 40, fg = "#312e2e", font = "consolas 10")
new_passentry = Entry(register_box, textvariable = new_passvalue, width = 40, fg = "#312e2e",  show = "*", font = "consolas 10" )
re_passentry = Entry(register_box, textvariable = re_passvalue, width = 40, fg = "#312e2e", show = "*", font = "consolas 10" )

new_username.grid(row = 0, column = 0)
new_password.grid(row = 1, column = 0)
new_userentry.grid(row = 0, column = 1, padx = 10)
new_passentry.grid(row = 1, column = 1, padx = 10)
re_password.grid(row = 2, column = 0)
re_passentry.grid(row = 2, column = 1)

Button(register_box, text = "Enter", font = font2, bg = "grey", command = lambda : register()).grid(row = 3 , column = 2, pady = 10, padx = 2)
# TODO: TO PRINT INVALID MESSAGE WHEN USER INPUT WRONG DATA 
invalid_register = Label(register_box, text = "*invalid", font = "Sans 10", fg = "red")
# invalid.grid(row = 0, column = 2)




root.mainloop()