from flask import Flask, render_template, request, redirect
import os
from time import time
from wallet import Wallet
from wallet import Account

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

myWallet =  Wallet()
account = None

@app.route("/", methods= ["GET", "POST"])
def home():
    global myWallet, account

    isConnected = myWallet.checkConnection()
    balance = "No Balance"

    if(account):
        # Call getBalance() method from myWallet object and pass it account.address to get balance
        balance = myWallet.getBalance(account.address)
        #balance = "No Balance"
   
    return render_template('index.html', isConnected=isConnected,  account= account, balance = balance)
   
@app.route("/createAccount", methods= ["GET", "POST"])
def createAccount(): 
    global myWallet, account
    account = Account()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, port=4000)
