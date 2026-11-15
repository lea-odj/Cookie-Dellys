from tkinter import*
from tkinter import messagebox
import json 

try: 
    with open ("user_data.json", "r", encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}

score = 0
username = ""
cookie_shop1 = 0 
cookie_shop2 = 0 
price_shop1 = 20
price_shop2 = 100 

# Fonctions pour connexion 
def signup():
    global username
    #réinitialisation 
    new_user.delete(0, END)
    new_pwd.delete(0, END)
    new_verif.delete(0, END)
    new_error.config(text='') 
    menu.forget()
    login_screen.forget()
    game.forget()

    if username != '':
        log_out()

    signup_screen.pack(expand = YES) 

def validate_new_account():
    global username, score

    if new_user.get() in user_data.keys():
        new_error.config(text="Pseudo déjà utilisé.")
    elif new_user.get().strip()== '' or len(new_user.get())<3:
        new_error.config(text="Pseudo trop court : minimum 4 caractères.")
    elif new_pwd.get().strip() == '' or len(new_pwd.get())<8:
        new_error.config(text='Mot de passe trop court : minimum 8 caractères.')
    elif new_pwd.get() != new_verif.get():
        new_error.config(text="Mot de passe non identique")
    else: 
        user_data[new_user.get().strip()] = {"pwd" : new_pwd.get(), "score": score, 'cookie_shop1' : cookie_shop1, 'cookie_shop2' : cookie_shop2, 'price_shop1' : price_shop1, "price_shop2": price_shop2}
        with open("user_data.json", "w", encoding="utf-8") as file: 
            json.dump(user_data, file)

        signup_screen.forget()
        score = user_data[new_user.get().strip()]["score"]
        username = new_user.get().strip()
        number_cookie.config(text=score)
        game.pack(expand = YES, fill=X, padx=0, pady=0)

def login():
    user.delete(0, END)
    user_pwd.delete(0, END)
    error.config(text='')
    menu.forget()
    signup_screen.forget()
    game.forget()
    login_screen.pack(expand=YES)

def validate_login():
    global score, username, price_shop1, price_shop2, cookie_shop1, cookie_shop2
    if user.get() in user_data.keys() and user_pwd.get() == user_data[user.get()]["pwd"]:
        score = user_data[user.get()]["score"]
        username = user.get()
        price_shop1 =  user_data[user.get()]["price_shop1"]
        price_shop2 =  user_data[user.get()]["price_shop2"]
        cookie_shop1 = user_data[user.get()]["cookie_shop1"]
        cookie_shop2 = user_data[user.get()]["cookie_shop2"]

        login_screen.forget()
        number_cookie.config(text=score)
        shop1_button.config(text=f"1 cookie/10 sec Prix: {price_shop1}\n En stock : {cookie_shop1}")
        shop2_button.config(text=f"1 cookie/sec Prix: {price_shop2}\n En stock : {cookie_shop2}")
        game.pack(expand=YES, fill=X, padx=0, pady=0)
    else: 
        error.config(text='Identifiant ou mot de passe faux.')

def guest_mode(): 
    global score, username, price_shop1, price_shop2, cookie_shop1, cookie_shop2
    log_out()
    number_cookie.config(text=score)
    login_screen.forget()
    signup_screen.forget()
    menu.forget()
    game.pack(expand=YES, fill=X, padx=0, pady=0)

def show_hide(pwd): 
    if pwd.cget("show")=='*':
        pwd.config(show="")
    else: 
        pwd.config(show='*')

def save():
    global score, username, price_shop1, price_shop2, cookie_shop1, cookie_shop2
    if username in user_data:
        user_data[username]["score"] = score
        user_data[username]["price_shop1"] = price_shop1
        user_data[username]["price_shop2"] = price_shop2
        user_data[username]["cookie_shop1"] = cookie_shop1
        user_data[username]["cookie_shop2"] = cookie_shop2

        with open ("user_data.json", "w", encoding="utf-8") as file: 
            json.dump(user_data, file)

    elif username == '':
        if messagebox.askyesno("Sauvegarde", "Créer un compte ?"):
            signup()

def log_out():
    global score, username, price_shop1, price_shop2, cookie_shop1, cookie_shop2
    score = 0 
    username = ""
    price_shop1 = 20 
    price_shop2 = 100
    cookie_shop1 = 0
    cookie_shop2 = 0 
    shop1_button.config(text=f"1 cookie/10 sec Prix: {price_shop1}\n En stock : {cookie_shop1}")
    shop2_button.config(text=f"1 cookie/sec Prix: {price_shop2}\n En stock : {cookie_shop2}")

# Fonctions du jeu 
def make_cookie():
    global score
    score += 1 
    number_cookie.config(text=score)

def shop1():
    global score, price_shop1, cookie_shop1
    if score >= price_shop1:
        score = score - price_shop1
        price_shop1 = round(price_shop1*1.15)
        cookie_shop1 += 1 
        shop1_button.config(text=f"1 cookie/10 sec Prix: {price_shop1}\n En stock : {cookie_shop1}")
        number_cookie.config(text=score)

def autocookie_shop1():
    global score, cookie_shop1
    score += cookie_shop1
    number_cookie.config(text=score)
    game.after(10000, autocookie_shop1)

def shop2():
    global score, price_shop2, cookie_shop2
    if score >= price_shop2:
        score -= price_shop2
        price_shop2 = round(price_shop2*1.15)
        cookie_shop2 += 1 
        shop2_button.config(text=f"1 cookie/sec Prix: {price_shop2}\n En stock : {cookie_shop2}") 
        number_cookie.config(text=score)

def autocookie_shop2():
    global score, cookie_shop2
    score += cookie_shop2
    number_cookie.config(text=score)
    game.after(1000, autocookie_shop2)

# Interface graphique 
window = Tk()
window.geometry("1100x700")
window.config(background="#EEDFC0")
window.title("Cookie Dellys")

#MENU BAR
menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff = 0)
file_menu.add_command(label='Quitter', command = window.destroy)
file_menu.add_command(label='Se connecter', command = login)
file_menu.add_command(label="Créer un compte", command = signup )
file_menu.add_command(label="Sauvegarder", command = save)
file_menu.add_command(label="Mode Invité", command = guest_mode)
file_menu.add_command(label="Déconnexion", command= log_out)
menu_bar.add_cascade(label="Menu", menu=file_menu)
window.config(menu=menu_bar)

#MENU ENTRÉE
menu = Frame(window, bg="#EEDFC0")
Label(menu, bg='#EEDFC0', fg="#945729", text = "Cookie Dellys", font=("Century Gothic", 55)).pack(pady = 40)

Button(menu, text ='Se Connecter', font=("verdana", 20), width = 14, bg="#F4B88B", fg="#513118", command=login).pack(pady = 5)
Button(menu, text ='Créer un compte', font=("verdana", 20), width=14, bg="#CC936F", fg='#513118', command=signup).pack(pady = 5)
Button(menu, text ='Mode Invité', font=("verdana", 20), width = 14, bg="#ECC09F", fg='#513118', command=guest_mode).pack(pady= 5)
Button(menu, text ='Quitter', font=("verdana", 20), width = 14, bg="#DEAD88", fg='#513118', command=window.destroy).pack(pady= 5)

menu.pack(expand = YES)

#CREATION DE COMPTE ----------------------------
signup_screen = Frame(window, bg ='#EEDFC0')
Label(signup_screen, text = "Créer un compte", font=("verdana", 40), bg ='#EEDFC0', fg='#513118').pack(pady=10)

#Identifant
new_user_box = Frame(signup_screen, bg="#eedfc0")
new_user_box.pack()
Label(new_user_box, text='Identifiant : ', font=('verdana', 15), bg="#eedfc0", fg="#513118").pack(anchor="w")
new_user = Entry(new_user_box, font=('verdana', 15), bg="#eac89b", fg="#513118", width=20)
new_user.pack(side=LEFT)

#Mot de passe 
new_pwd_box = Frame(signup_screen, bg="#eedfc0")
new_pwd_box.pack()

Label(new_pwd_box, text='Mot de passe : ', font=('verdana', 15), bg="#eedfc0", fg="#513118").pack(anchor="w")

new_pwd_show=Frame(new_pwd_box, bg='#eedfc0')
new_pwd = Entry(new_pwd_show, font=('verdana', 15), bg="#eac89b", fg="#513118", width=17, show="*")
new_pwd.pack(side=LEFT)
show_new_pwd = Button(new_pwd_show, text="Voir", font=("verdana", 10), width=3, bg='#eac89b', fg='#513118', command=lambda :show_hide(new_pwd)).pack(side=LEFT)
new_pwd_show.pack()

#Vérification mot de passe 
new_verif_box = Frame(signup_screen, bg="#eedfc0")
new_verif_box.pack()

Label(new_verif_box, text='Confirmer : ', font=('verdana', 15), bg="#eedfc0", fg="#513118").pack(anchor="w")

new_verif_show=Frame(new_verif_box, bg="#eedfc0")
new_verif = Entry(new_verif_show, font=('verdana', 15), bg='#eac89b', fg="#513118", width=17, show="*")
new_verif.pack(side=LEFT)
new_verif_show.pack()
Button(new_verif_show, text="Voir", font=("verdana", 10), width=3, bg='#eac89b', fg='#513118', command=lambda :show_hide(new_verif)).pack(side=LEFT)

#Validation
Button(signup_screen, text='Créer le compte', font=('verdana', 15), bg="#b97c53", fg="#FFE9D6", width= 20, command= validate_new_account).pack(pady=20)
new_error=Label(signup_screen, text='', font=("verdana", 10), bg='#eedfc0', fg='#513118')
new_error.pack()

#CONNEXION ------------------------------ 
login_screen = Frame(window, bg="#eedfc0")

Label(login_screen, text="Connexion", font=("verdana", 40), bg ='#EEDFC0', fg='#513118').pack(pady=10)

#Identifiant
user_box = Frame(login_screen, bg="#eedfc0")
Label(user_box, text='Identifiant : ', font=('verdana', 15), bg="#eedfc0", fg="#513118").pack(anchor="w")
user = Entry(user_box, font=('verdana', 15), bg="#eac89b", fg="#513118", width=20)
user.pack(side=LEFT)
user_box.pack()

#mot de passe 
pwd_box = Frame(login_screen, bg='#eedfc0')
Label(pwd_box, text='Mot de passe : ', font=('verdana', 15), bg="#eedfc0", fg="#513118").pack(anchor="w")
pwd_show = Frame(pwd_box, bg='#eedfc0')
user_pwd = Entry(pwd_show, font=('verdana', 15), bg='#eac89b', fg="#513118", width=17, show="*")
user_pwd.pack(side=LEFT)
Button(pwd_show, text="Voir", font=("verdana", 10), width=3, bg='#eac89b', fg='#513118', command=lambda :show_hide(user_pwd)).pack(side=LEFT)
pwd_show.pack()
pwd_box.pack()

#Validation
Button(login_screen, text='Se connecter', font=('verdana', 15), bg="#b97c53", fg="#FFE9D6", width= 20, command= validate_login).pack(pady=20)
error=Label(login_screen, text='', font=("verdana", 10), bg='#eedfc0', fg='#513118')
error.pack()


#JEU -------------------------------
game = Frame(window, bg='#eedfc0')

Label(game, text="Nombre de cookies :", font=("verdana", 20), bg="#c38264", fg="#3C210D").pack(fill=X)
number_cookie = Label(game, text=score, font=("verdana", 20), bg="#c38264", fg="#3C210D") 
number_cookie.pack(fill=X, padx=0, pady=0)


game_underbox = Frame(game, bg="#eedfc0")

cookie_frame = Frame(game_underbox, bg ='#eedfc0')
cookie_img = PhotoImage(file="cutecookie.png").subsample(2)
cookie_label = Label(cookie_frame, image=cookie_img, bg="#EEDFC0", cursor = "hand2")
cookie_label.pack(pady=20)
cookie_label.bind('<Button-1>', lambda event: make_cookie())
cookie_frame.pack(side= LEFT, padx=50, pady=20, anchor='n')

option_box = Frame(game_underbox, bg='#eedfc0')
Label(option_box, text="Boutique",font=("verdana", 30), bg="#eedfc0", fg="#513118").pack(padx= 50)
shop1_button= Button(option_box, text=f"1 cookie/10 sec Prix: {price_shop1}\n En stock : {cookie_shop1}", font=("verdana", 10), bg="#CC936F", fg="#513118", width = 25, command=shop1)
shop1_button.pack(pady = 8)

shop2_button = Button(option_box, text=f"1 cookie/sec Prix: {price_shop2}\n En stock : {cookie_shop2}", font=("verdana", 10), bg="#B57F5D", fg="#513118", width =25, command=shop2)
shop2_button.pack(pady = 3)

option_box.pack(side=LEFT, anchor="n", pady=40)

game_underbox.pack()

save_button = Button(game, text='Sauvegarder', font=("verdana", 20), bg="#ECC09F", fg="#513118", command=save)
save_button.pack()

autocookie_shop1()
autocookie_shop2()

window.mainloop()