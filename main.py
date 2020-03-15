import requests
import json
from tkinter import *
from tkinter import messagebox ,Menu
import sqlite3

con=sqlite3.connect("portfolio.db")
obj=con.cursor()
obj.execute("create table if not exists coin(id integer primary key,symbol text,amount integer,price real)")
con.commit()

neha = Tk()
neha.title("Portfolio")
neha.iconbitmap("favicon.ico")

#obj.execute("insert into coin values(1,'BCH',2,3200)")
#con.commit()

#obj.execute("insert into coin values(2,'ETH',100,2.05)")
#con.commit()

#obj.execute("insert into coin values(3,'XRP',10,200)")
#con.commit()

#obj.execute("insert into coin values(4,'LTC',50,34)")
#con.commit()
def reset():
    Portfolio()
def app_nav():
    def clear_all():
        obj.execute("delete from coin")
        con.commit()
    def close_all():
        neha.destroy()
    menu=Menu(neha)
    file_item=Menu(menu)
    file_item.add_command(label="Clear Portfolio",command=clear_all,)
    file_item.add_command(label="Close app",command=close_all)
    menu.add_cascade(label="File",menu=file_item)
    neha.config(menu=menu)
def Portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=10&convert=USD&CMC_PRO_API_KEY=861266fb-1142-4baf-8b00-528341ccc147")
    api = json.loads(api_request.content)
    #coins = [{"symbol" : "BCH","amount_owned" :2,"price_per_coin": 3200},{"symbol" : "ETH","amount_owned":100,"price_per_coin": 2.05},
    #{"symbol" : "XRP","amount_owned" :10,"price_per_coin": 200},{"symbol" : "LTC","amount_owned":50,"price_per_coin": 34} ]
    def font_colour(amount):
        if amount>=0:
            return "green"
        else:
            return "red"
    obj.execute("select * from coin")
    coins=obj.fetchall()

    def insert_coin():
        a=symbol_txt.get()
        b=price_txt.get()
        c=amount_txt.get()
        obj.execute("insert into coin(symbol,price,amount) values(?,?,?)",(a,b,c))
        con.commit()
        messagebox.showinfo("Portfolio","Coin added successfully")

        reset()

    def update_coin():
        obj.execute("update coin set symbol=? ,price=? ,amount=? where id =?" ,(symbol_up.get(),price_up.get(),amount_up.get(),id_up.get()))
        messagebox.showinfo("Portfolio","Coin updated successfully")
        reset()
    def ddelete_coin():
        obj.execute("Delete from coin where id =?" ,(id_del.get(),))
        messagebox.showinfo("Portfolio","Coin deleted successfully")
        reset()

    coin_row = 1
    totn =0
    totc=0
    for i in range(0,10):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2]*coin[3]
                current_value = api["data"][i]["quote"]["USD"]["price"]*coin[2]
                PL_per_coin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_PL = PL_per_coin * coin[2]
                totn = totn + total_PL
                totc= totc + current_value

                portfolio_id = Label(neha , text=coin[0],bg="grey", fg="black",font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2)
                portfolio_id.grid(row=coin_row,column=0,sticky=N+S+E+W)
                name = Label(neha , text=api["data"][i]["symbol"] ,bg="grey", fg="black",font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2)
                name.grid(row=coin_row,column=1,sticky=N+S+E+W)
                price = Label(neha , text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]) ,bg="grey", fg="black",font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2 )
                price.grid(row=coin_row,column=2,sticky=N+S+E+W)
                no_of_coins= Label(neha , text=coin[2] ,bg="grey", fg="black",font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2 )
                no_of_coins.grid(row=coin_row,column=3,sticky=N+S+E+W)
                amount_spent = Label(neha , text="${0:.2f}".format(total_paid) ,bg="grey", fg="black",font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2)
                amount_spent.grid(row=coin_row,column=4,sticky=N+S+E+W)
                current_value = Label(neha , text="${0:.2f}".format(current_value),bg="grey", fg="black",font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2 )
                current_value.grid(row=coin_row,column=5,sticky=N+S+E+W)
                PL_per_coin = Label(neha , text="${0:.2f}".format(PL_per_coin) ,bg="grey", fg=font_colour(float(PL_per_coin)),font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2 )
                PL_per_coin.grid(row=coin_row,column=6,sticky=N+S+E+W)
                total_PL = Label(neha , text="${0:.2f}".format(total_PL) ,bg="grey", fg=font_colour(float(total_PL)),font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2 )
                total_PL.grid(row=coin_row,column=7,sticky=N+S+E+W)

                coin_row+=1


        total_c = Label(neha , text="${0:.2f}".format(totc) ,bg="grey", fg="black",font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2 )
        total_c.grid(row=coin_row,column=5,sticky=N+S+E+W)
        total_PL = Label(neha , text="${0:.2f}".format(totn) ,bg="grey", fg=font_colour(float(totn)),font="Lato 12",padx=2,pady=2,relief="groove",borderwidth=2 )
        total_PL.grid(row=coin_row,column=7,sticky=N+S+E+W)
        refresh = Button(neha , text="Refresh" ,bg="blue",fg="white",font="Lato 12 bold",command=reset,padx=2,pady=2,relief="groove",borderwidth=2 )
        refresh.grid(row=coin_row+1,column=7,sticky=N+S+E+W)

        symbol_txt = Entry(neha,borderwidth=2,relief="groove")
        symbol_txt.grid(row=coin_row+1 ,column=1)
        price_txt = Entry(neha,borderwidth=2,relief="groove")
        price_txt.grid(row=coin_row+1 ,column=2)
        amount_txt = Entry(neha,borderwidth=2,relief="groove")
        amount_txt.grid(row=coin_row+1 ,column=3)
        add_coin = Button(neha,text="Add coin",bg="blue",command=insert_coin, fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
        add_coin.grid(row=coin_row+1 ,column=4)

        id_up = Entry(neha,borderwidth=2,relief="groove")
        id_up.grid(row=coin_row+2 ,column=0)
        symbol_up = Entry(neha,borderwidth=2,relief="groove")
        symbol_up.grid(row=coin_row+2 ,column=1)
        price_up = Entry(neha,borderwidth=2,relief="groove")
        price_up.grid(row=coin_row+2 ,column=2)
        amount_up = Entry(neha,borderwidth=2,relief="groove")
        amount_up.grid(row=coin_row+2 ,column=3)
        update_coin = Button(neha,text="Update coin",bg="blue",command=update_coin, fg="black",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
        update_coin.grid(row=coin_row+2 ,column=4)

        id_del = Entry(neha,borderwidth=2,relief="groove")
        id_del.grid(row=coin_row+3 ,column=0)
        delete_coin = Button(neha,text="Delete coin",bg="red",command=ddelete_coin, fg="white",font="Lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
        delete_coin.grid(row=coin_row+3 ,column=1)


def header():
    portfolio_id = Label(neha , text="portfolio id" ,bg="dark blue", fg="white" ,font="Lato 12 bold", padx=5,pady=5,borderwidth=2,relief="groove")
    portfolio_id.grid(row=0,column=0,sticky=N+S+E+W)
    name = Label(neha , text="coin name" ,bg="dark blue", fg="white" ,font="Lato 12 bold", padx=5,pady=5,borderwidth=2,relief="groove")
    name.grid(row=0,column=1,sticky=N+S+E+W)
    price = Label(neha , text="Price" ,bg="dark blue", fg="white",font="Lato 12 bold", padx=5,pady=5,borderwidth=2,relief="groove" )
    price.grid(row=0,column=2,sticky=N+S+E+W)
    no_of_coins= Label(neha , text="coins owned" ,bg="dark blue", fg="white" ,font="Lato 12 bold", padx=5,pady=5,borderwidth=2,relief="groove")
    no_of_coins.grid(row=0,column=3,sticky=N+S+E+W)
    amount_spent = Label(neha , text="total amount paid" ,bg="dark blue", fg="white",font="Lato 12 bold", padx=5,pady=5,borderwidth=2,relief="groove")
    amount_spent.grid(row=0,column=4,sticky=N+S+E+W)
    current_value = Label(neha , text="current value" ,bg="dark blue", fg="white",font="Lato 12 bold", padx=5,pady=5,borderwidth=2,relief="groove" )
    current_value.grid(row=0,column=5,sticky=N+S+E+W)
    PL_per_coin = Label(neha , text="P/L per coin" ,bg="dark blue", fg="white", font="Lato 12 bold", padx=5,pady=5,borderwidth=2,relief="groove")
    PL_per_coin.grid(row=0,column=6,sticky=N+S+E+W)
    total_PL = Label(neha , text="total P/L per coin" ,bg="dark blue", fg="white" ,font="Lato 12 bold", padx=5,pady=5,borderwidth=2,relief="groove")
    total_PL.grid(row=0,column=7,sticky=N+S+E+W)

app_nav()
header()
Portfolio()
neha.mainloop()

con.close()
obj.close()
