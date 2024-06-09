from flask import *
from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address
import re

app = Flask(__name__)

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract_address, abi=abi)


def pay(account, value):
    try:
        tx_hash = contract.functions.pay().transact({
            'from': account,
            'value': value,
        })
    except Exception as ex:
        pass


def get_balance(account):
    balanc = contract.functions.GetBalance().call({
        "from": account,
    })
    return balanc


def withdraw(account, amount):
    try:
        tx_hash = contract.functions.Withdraw(amount).transact({
            'from': account,
        })
    except Exception as ex:
        pass


def create_Estate(account, size, estateAdres, typeEs):
    tx_hash = contract.functions.createEstate(size, estateAdres, typeEs).transact({
        'from': account,
    })


def get_esates(account):
    estates = contract.functions.GetEstates().call({
        "from": account,
    })
    return estates


def get_ads(account):
    ads = contract.functions.GetAds().call({
        "from": account,
    })
    return ads


def buy_estate(account, nomerAd):
    try:
        tx_hash = contract.functions.BuyEstate(nomerAd).transact({
            'from': account,
        })
    except:
        pass


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        public_key = request.form.get('username')
        password = request.form.get('pasword')
        button = request.form.get('reg')
        if button is not None:
            return redirect(url_for('register', name="register.html"))
        try:
            w3.geth.personal.unlock_account(public_key, password)
            return redirect(url_for('about', name="Vibor.html", public_key=public_key))
        except:
            return render_template("main.html", error=False)
    else:
        return render_template("main.html", error=False)


@app.route('/<public_key>/<name>', methods=['GET', 'POST'])
def about(name, public_key):
    button = request.form.get('exit')
    if name == "Estate.html":
        return redirect(url_for('Estete', public_key=public_key))
    elif name == "Balance.html":
        return redirect(url_for('BalancePage', public_key=public_key))
    elif name == "Add.html":
        return redirect(url_for('BuyAdd', public_key=public_key))
    elif name == "Bue.html":
        return render_template("Bue.html", name=name)
    elif button is not None:
        return redirect(url_for('index'))
    else:
        return render_template("Vibor.html", name=name)


@app.route('/<public_key>/Balance.html', methods=['GET', 'POST'])
def BalancePage(public_key):
    button = request.form.get('exit')
    if button is None:
        if request.method == 'POST':
            try:
                scolko = request.form.get('colSen-vo')
                scolko = int(scolko)
            except:
                scolko = 0
            but = request.form.get("send_btn")
            if but is not None:
                pay(public_key, scolko)
                return redirect(url_for('BalancePage', public_key=public_key))
            try:
                snyt = request.form.get("colWith-vo")
                snyt = int(snyt)
            except:
                snyt = 0
            withDr = request.form.get("withDraw")
            if withDr is not None:
                withdraw(public_key, snyt)
                return redirect(url_for('BalancePage', public_key=public_key))
        else:
            balanc_smart = get_balance(public_key)
            balsnc_acc = w3.eth.get_balance(public_key)
            return render_template("Balance.html", Smart_bal=balanc_smart, Acc_balnce=balsnc_acc)
    else:
        return redirect(url_for('index'))


@app.route('/<public_key>/PayAdd.html', methods=['GET', 'POST'])
def BuyAdd(public_key):
    button = request.form.get('exit')
    if button is None:
        if request.method == 'POST':
            try:
                scolko = request.form.get('nomer')
                scolko = int(scolko)
            except:
                scolko = 0
            but = request.form.get("buyEs")
            if but is not None:
                buy_estate(public_key, scolko)
                return redirect(url_for('BuyAdd', public_key=public_key))
            ads = get_ads(public_key)
            addes = []
            for es in ads:
                if (es[5] != 1):
                    addes.append(es)
            return render_template("PayAdd.html", estates=addes)
        else:
            ads = get_ads(public_key)
            addes = []
            for es in ads:
                if (es[5] != 1):
                    addes.append(es)
            return render_template("PayAdd.html", estates=addes)
    else:
        return redirect(url_for('index'))


@app.route('/<public_key>/Estate.html', methods=['GET', 'POST'])
def Estete(public_key):
    button = request.form.get('exit')
    if button is None:
        if request.method == "POST":
            adress = request.form.get('adres')
            size = request.form.get('Size')
            size = int(size)
            type = request.form.get('Type')
            typeInt = 1
            if type == "House":
                typeInt = 0
            elif type == "Flat":
                typeInt = 1
            elif type == "Loft":
                typeInt = 2
            AdEs = request.form.get('AddEstate')
            if AdEs is not None:
                create_Estate(public_key, size, adress, typeInt)
                esteteTrue = vivodEs(public_key)
                return render_template("Estate.html", estates=esteteTrue)
            else:
                esteteTrue = vivodEs(public_key)
                return render_template("Estate.html", estates=esteteTrue)
        else:
            try:
                esteteTrue = vivodEs(public_key)
                return render_template("Estate.html", estates=esteteTrue)
            except:
                null_estates = [
                    ("Тут будут объявления", 1),
                    ("Тут будут объявления", 2),
                    ("Тут будут объявления", 3),
                ]
                return render_template("Estate.html", estates=null_estates)
    else:
        return redirect(url_for('index'))


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    button = request.form.get('vhod')
    if button is not None:
        passw = request.form['password']
        if len(passw) >= 12:
            if bool(re.search('[!"#$%&\'()*+,-./:;<=>?@[\]^_{|}~]', passw)):
                if bool(re.search('[0-9]', passw)):
                    if bool(re.search('[A-Z]', passw)):
                        acc = w3.geth.personal.new_account(passw)
                        return render_template("register.html", error=False, acc=acc)
                    else:
                        error = request.form.get('error')
                        error = "Пароль не содержит заглавные английские буквы"
                        return render_template("register.html", error=False)
                else:
                    error = request.form.get('error')
                    error = "Пароль не содержит цифры"
                    return render_template("register.html", error=False)
            else:
                error = request.form.get('error')
                error = "Пароль не содержит специальные символы"
                return render_template("register.html", error=False)
        else:
            error = request.form.get('error')
            error = "Пароль меньше 12 символов"
            return render_template("register.html", error=False)
    else:
        return render_template("register.html", error=False)


def vivodEs(public_key):
    estates = get_esates(public_key)
    esteteTrue = []
    for es in estates:
        if (es[4] != False):
            esteteTrue.append(es)
    return esteteTrue

if __name__ == '__main__':
    app.run(debug=True)
