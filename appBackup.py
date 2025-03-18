from flask import Flask, render_template, request, jsonify
import sqlite3
import locale

locale.setlocale(locale.LC_ALL, 'sl_SI.UTF-8')

app = Flask(__name__, static_folder='static')

# Posebna sortirna funkcija
def posebna_sortirna_funkcija(opis):
    deli = opis.split('-')
    if len(deli) >= 2:
        return deli[1].strip().lower()
    else:
        return 'žžžžž' + opis.lower()

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/iskanje")
def iskanje():
    return render_template("iskanje.html")

# PREVERI GESLO (neodvisno od velikosti črk)
@app.route('/preveri_geslo', methods=['POST'])
def preveri_geslo():
    podatki = request.json
    geslo = podatki.get("geslo", "").strip().upper()

    if not geslo:
        return jsonify({"napaka": "Vnesi geslo za preverjanje!"}), 400

    con = sqlite3.connect("veliki_ugankarski_slovar.db")
    cur = con.cursor()

    cur.execute("SELECT id, geslo, opis FROM slovar WHERE UPPER(geslo) = ?", (geslo,))
    rezultati = cur.fetchall()
    con.close()

    sortirani_rezultati = sorted(
        [{'id': id, 'geslo': ges, 'opis': op} for id, ges, op in rezultati],
        key=lambda x: posebna_sortirna_funkcija(x['opis'])
    )

    return jsonify({'zadetki': sortirani_rezultati})

# DODAJ GESLO
@app.route("/dodaj_geslo", methods=["POST"])
def dodaj_geslo():
    podatki = request.json
    geslo = podatki.get("geslo").upper()
    opis = podatki.get("opis")

    if not geslo or not opis:
        return jsonify({"napaka": "Geslo in opis sta obvezna!"}), 400

    con = sqlite3.connect("veliki_ugankarski_slovar.db")
    cur = con.cursor()

    cur.execute("INSERT INTO slovar (geslo, opis) VALUES (?, ?)", (geslo, opis))
    con.commit()

    cur.execute("SELECT id, geslo, opis FROM slovar WHERE geslo = ? ORDER BY opis", (geslo,))
    rezultati = cur.fetchall()
    con.close()

    sortirani_rezultati = sorted(
        [{'id': id, 'geslo': ges, 'opis': op} for id, ges, op in rezultati],
        key=lambda x: posebna_sortirna_funkcija(x['opis'])
    )

    return jsonify({
        "sporocilo": "Geslo je bilo uspešno dodano.",
        "zadetki": sortirani_rezultati
    })

# ŠTEVEC GESEL
@app.route("/stevilo_gesel", methods=["GET"])
def stevilo_gesel():
    con = sqlite3.connect("veliki_ugankarski_slovar.db")
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    con.close()
    return jsonify({"stevilo": stevilo})

# ✏️ UREDI GESLO
@app.route("/uredi_geslo", methods=["POST"])
def uredi_geslo():
    podatki = request.json
    id = podatki.get("id")
    novi_opis = podatki.get("novi_opis")

    if not id or not novi_opis:
        return jsonify({"napaka": "ID in novi opis sta obvezna!"}), 400

    con = sqlite3.connect("veliki_ugankarski_slovar.db")
    cur = con.cursor()
    cur.execute("UPDATE slovar SET opis = ? WHERE id = ?", (novi_opis, id))
    con.commit()
    con.close()

    return jsonify({"sporocilo": "Geslo uspešno urejeno!"}), 200

# 🗑️ IZBRISI GESLO
@app.route("/izbrisi_geslo", methods=["POST"])
def izbrisi_geslo():
    podatki = request.json
    id = podatki.get("id")

    if not id:
        return jsonify({"napaka": "ID je obvezen!"}), 400

    con = sqlite3.connect("veliki_ugankarski_slovar.db")
    cur = con.cursor()
    cur.execute("DELETE FROM slovar WHERE id = ?", (id,))
    con.commit()
    con.close()

    return jsonify({"sporocilo": "Geslo je bilo izbrisano."})

if __name__ == "__main__":
    app.run(debug=True)
