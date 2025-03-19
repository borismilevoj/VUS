from flask import Flask, render_template, request, jsonify, g
import sqlite3

app = Flask(__name__)

# Pravilna povezava z bazo za Flask

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('veliki_ugankarski_slovar.db', check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Glavna stran

@app.route('/')
def index():
    return render_template('index.html')

# Administracija

@app.route("/admin")
def admin():
    return render_template("admin.html")

# Števec gesel

@app.route('/stevilo_gesel', methods=['GET'])
def stevilo_gesel():
    baza = get_db()
    cur = baza.cursor()
    cur.execute("SELECT COUNT(*) FROM gesla")
    stevilo = cur.fetchone()[0]
    return jsonify({"stevilo": stevilo})

# Dodaj geslo

@app.route('/dodaj_geslo', methods=['POST'])
def dodaj_geslo():
    baza = get_db()
    data = request.json
    novo_geslo = data["geslo"]
    nov_opis = data["opis"]
    cur = baza.cursor()
    cur.execute("INSERT INTO gesla (geslo, opis) VALUES (?, ?)", (novo_geslo, nov_opis))
    baza.commit()
    return jsonify({"sporocilo": "Geslo uspešno dodano!"})

# Preveri geslo

@app.route('/preveri_geslo', methods=['POST'])
def preveri_geslo():
    baza = get_db()
    geslo = request.json["geslo"]
    cur = baza.cursor()
    cur.execute("SELECT * FROM gesla WHERE geslo = ?", (geslo,))
    rezultat = cur.fetchone()
    if rezultat:
        return jsonify({
            "sporocilo": "Geslo je v bazi!",
            "geslo": geslo,
            "opis": {col[0]: rezultat[ix] for ix, col in enumerate(cur.description) for ix, rezultat in
                     enumerate(rezultat)}
        })
    else:
        return jsonify({"sporocilo": "Gesla ni v bazi!"})

# Uredi geslo

@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    baza = get_db()
    data = request.json
    cur = baza.cursor()
    cur.execute("UPDATE gesla SET geslo = ?, opis = ? WHERE id = ?",
                (data["geslo"], data["opis"], data["id"]))
    baza.commit()
    return jsonify({"sporocilo": "Geslo uspešno urejeno!"})

# Izbriši geslo

@app.route('/izbrisi_geslo', methods=['POST'])
def izbrisi_geslo():
    baza = get_db()
    geslo_id = request.json["id"]
    cur = baza.cursor()
    cur.execute("DELETE FROM gesla WHERE id = ?", (geslo_id,))

    baza.commit()
    return jsonify({"sporocilo": "Geslo je bilo izbrisano."})

# Išči po opisu

@app.route('/isci_po_opisu', methods=['POST'])
def isci_po_opisu():
    baza = get_db()
    opis = request.json['iskanje']
    cur = baza.cursor()
    cur.execute("SELECT * FROM gesla WHERE opis LIKE ?", ('%' + opis + '%',))
    rezultati = cur.fetchall()
    return jsonify({"rezultati": rezultati_v_slovar(cur, rezultati)})

# Pretvori rezultat v slovar

def rezultati_v_slovar(cur, rezultati):
    stolpci = [desc[0] for desc in cur.description]
    return [dict(zip(stolpci, vrstica)) for vrstica in rezultati]

# Obvezno za sprostitev baze ob koncu zahteve

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
