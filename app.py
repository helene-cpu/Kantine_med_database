from flask import Flask, render_template, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
import mysql.connector
from forms import RegisterForm, LoginForm

app= Flask(__name__)
app.secret_key = "hemmelig"

def get_conn():
    return mysql.connector.connect(
        host= "localhost",
        user="test",
        password="Mysql123!",
        database="eksempel_db"
    )

class RegisterForm(FlaskForm):
    username = StringField("Brukernavn", validators=[InputRequired()])
    password = PasswordField("Passord", validators=[InputRequired()])
    name = StringField("Navn", validators=[InputRequired()])
    address = StringField("Adresse", validators=[InputRequired()])
    submit = SubmitField("Registrer")

class LoginForm(FlaskForm):
    username = StringField("Brukernavn", validators=[InputRequired()])
    password = PasswordField("Passord", validators=[InputRequired()])
    submit = SubmitField("Logg inn")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/meny')
def meny():
    meny_kantine=[
        {"dag": "mandag", "rett": "Grønnsakssuppe", "bilde": "/static/images/suppe.jpg", "beskrivelse": "Grønnsaks suppe med gulrøtter, pølser og kjøttboller", "allergier": "Inneholder: Svin"},
        {"dag": "tirsdag", "rett": "Pastasalat", "bilde": "/static/images/pastasalat.jpg", "beskrivelse": "varm salat med pasta og masse næringsrike grønnsaker","allergier": "Inneholder: Gluten"},
        {"dag": "Onsdag", "rett": "Laks og potet", "bilde": "/static/images/laks.jpg", "beskrivelse": "En laksefilet per person, med potet og revet gulrot"},
        {"dag": "Torsdag", "rett": "Vegetarlasagne", "bilde": "/static/images/lasagne.jpg","beskrivelse": "Vegetar lasagne med ostesaus på toppen", "allergier": "Inneholder: Gluten, Laktose"},
        {"dag": "Fredag", "rett": "Wok", "bilde": "/static/images/wok.jpg", "beskrivelse": "nudler med grønnsaker og saus"}
        ]
    return render_template("meny.html", kantine=meny_kantine)

@app.route('/varer')
def varer():
    varer_kantine=[
        {"vare": "Litago", "pris": "26", "bilde": "/static/images/litago.png"},
        {"vare": "Iskaffe", "pris": "28", "bilde": "/static/images/iskaffe.png"},
        {"vare": "Coca Cola", "pris": "32", "bilde": "/static/images/coca-cola.png"},
        {"vare": "Iste", "pris": "30", "bilde": "/static/images/iste.png"},
        {"vare": "Påsmurte rundstykker", "pris": "29", "bilde": "/static/images/rundstykke.png"},
        {"vare": "Baguetter", "pris": "29", "bilde": "/static/images/baguette.png"},
        {"vare": "Knekkebrød", "pris": "18", "bilde": "/static/images/knekkebrod.png"},
        {"vare": "Sjokolade", "pris": "29", "bilde": "/static/images/sjokolade.png"}
    ]
    return render_template("varer.html", mat=varer_kantine, tekst="ugrwiuGV")

@app.route('/kontakt')
def kontakt():
    ansatte_kantine=[
        {"navn": "Thea", "stilling": "Sint kokk", "bilde": "/static/images/thea.jpg", "kommentar": "Alltid 2 sekunder fra å kaste sleiva, men maten er fantastisk", "epost": "matmedaggresjon@akademiet.no", "tlf": "+47 12345678"},
        {"navn": "Markus", "stilling": "Dessertdirektør", "bilde": "/static/images/markus.jpg", "kommentar": "Den virkelige maktpersonen i kantina", "epost": "sjefssukker@akademiet.no", "tlf": "+47 21436587"},
        {"navn": "Ebbe", "stilling": "Vaskedame", "bilde": "/static/images/ebbe.jpg", "kommentar": "Tar kampen mot støv- taper hver gang", "epost": "vaskedronning@akademiet.no", "tlf": "+47 87654321"},
        {"navn": "Ludvig", "stilling": "Matfilosof", "bilde": "/static/images/ludvig.jpg", "kommentar": "spør- hva er egentlig til lunsj?", "epost": "eksistensiellkokk@akademiet.no", "tlf": "+47 67676767"},
        {"navn": "Nikolai", "stilling": "Uhygenisk oppvaskmester", "bilde": "/static/images/nikolai.jpg", "kommentar": "Skyller tallerkner med optimisme og luft", "epost": "rentnok@akademiet.no", "tlf": "+47 76767676"},
        {"navn": "Audun", "stilling": "Usunn ernæringsfysiolog", "bilde": "/static/images/audun.jpg", "kommentar": "Anbefaler pommes frites som grønnsak", "epost": "usunnveileder@akademiet.no", "tlf": "+47 34561278"}
    ]
    return render_template("kontakt.html",ansatte=ansatte_kantine )

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        navn = form.name.data
        brukernavn = form.username.data
        passord = form.password.data
        adresse = form.address.data

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO brukere (navn, brukernavn, passord, adresse) VALUES (%s, %s, %s, %s)",
            (navn, brukernavn, passord, adresse)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/login")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        brukernavn = form.username.data
        passord = form.password.data

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT navn FROM brukere WHERE brukernavn=%s AND passord=%s",
            (brukernavn, passord)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['navn'] = user[0]  
            return redirect("/welcome")
        else:
            form.username.errors.append("Feil brukernavn eller passord")

    return render_template("login.html", form=form)

@app.route("/welcome")
def welcome():
    navn = session.get('navn')  # Hent navn fra session
    if not navn:
        return redirect("/login")  # send tilbake til login om ikke logget inn
    return render_template("welcome.html", name=navn)

if __name__ == "__main__":
    app.run(debug=True)