from flask import Flask, render_template, request, jsonify, g
import sqlite3
import pandas as pd


app = Flask(__name__)

DATABASE = 'VUS.db'

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route("/home")
def home():
    return "<h1>Deluje – to je direktni response brez predloge!</h1>"



# povezava z bazo
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# uvoz Excel datotek

import os

if os.path.exists('izvoz_slovarja_z_ID.xlsx'):
    df = pd.read_excel('izvoz_slovarja_z_ID.xlsx')
    print("Excel datoteka naložena.")
else:
    print("Excel datoteka ni bila najdena – preskočena.")
import os

# DF STARA
if os.path.exists('izvoz_slovarja_z_ID.xlsx'):
    df_stara = pd.read_excel('izvoz_slovarja_z_ID.xlsx', header=None, dtype=str)
    df_stara.columns = ['ID', 'GESLO', 'OPIS']
    if 'ID' not in df_stara.columns:
        df_stara.insert(0, 'ID', range(1, 1 + len(df_stara)))
    print("Excel datoteka df_stara naložena.")
else:
    df_stara = None
    print("Excel datoteka df_stara ni bila najdena – preskočena.")

# DF NOVA
if os.path.exists('SLOVAR Excel.xlsx'):
    df_nova = pd.read_excel('SLOVAR Excel.xlsx', header=None, dtype=str)
    df_nova.columns = ['GESLO', 'OPIS']
    print("Excel datoteka df_nova naložena.")
else:
    df_nova = None
    print("Excel datoteka df_nova ni bila najdena – preskočena.")

# DF KONČNA (če je vsaj ena tabela na voljo)
if df_stara is not None and df_nova is not None:
    df_koncna = pd.concat([df_stara, df_nova]).drop_duplicates(subset=["GESLO", "OPIS"]).reset_index(drop=True)
elif df_stara is not None:
    df_koncna = df_stara
elif df_nova is not None:
    df_koncna = df_nova
else:
    df_koncna = None
    print("Nobena Excel datoteka ni na voljo – df_koncna je prazna.")




@app.route('/')
def index():
    return render_template('index.html')


# PREVERI GESLO

@app.route('/preveri', methods=['POST'])
def preveri_geslo():
    podatki = request.get_json()
    geslo = podatki.get('geslo')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT ID, GESLO, OPIS FROM slovar WHERE UPPER(GESLO) = ?", (geslo.upper(),))
    rezultat = cursor.fetchall()
    conn.close()

    if rezultat:
        gesla = [{"id": r["ID"], "geslo": r["GESLO"], "opis": r["OPIS"]} for r in rezultat]

        # Python sortiranje (izvleče in sortira po prvem imenu takoj za vezajem)
        gesla.sort(key=lambda x: (
            0 if '-' in x['opis'] else 1,
            x['opis'].split('-')[1].strip().split(' ')[0] if '-' in x['opis'] else x['opis']
        ))

        return jsonify({
            "sporocilo": f"Število zadetkov: {len(gesla)}",
            "rezultati": gesla
        }), 200
    else:
        return jsonify({"sporocilo": "Gesla ni v bazi!"}), 404


# DODAJ GESLO

@app.route('/dodaj', methods=['POST'])
def dodaj_geslo():
    podatki = request.get_json()
    geslo = podatki.get('geslo')
    opis = podatki.get('opis')

    if not geslo or not opis:
        return jsonify({"sporocilo": "Geslo in opis morata biti izpolnjena!"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO slovar (GESLO, OPIS) VALUES (?, ?)", (geslo.upper(), opis))
        conn.commit()

        # Ključni popravek tukaj:
        nov_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "sporocilo": "Geslo uspešno dodano!",
            "id": nov_id,
            "geslo": geslo.upper(),
            "opis": opis
        }), 200

    except sqlite3.Error as e:
        return jsonify({"sporocilo": f"Napaka pri dodajanju gesla: {e}"}), 500



# UREDI GESLO

@app.route('/uredi_geslo', methods=['POST'])
def uredi_geslo():
    podatki = request.get_json()
    geslo_id = podatki.get('id')
    novi_opis = podatki.get('novi_opis')

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE slovar SET OPIS=? WHERE ID=?", (novi_opis, geslo_id))
        conn.commit()
        conn.close()

        return jsonify({"sporocilo": "Opis gesla uspešno posodobljen!"}), 200
    except sqlite3.Error as e:
        return jsonify({"napaka": f"Napaka pri urejanju gesla: {e}"}), 500


# BRIŠI GESLO

@app.route('/izbrisi_geslo', methods=['POST'])
def izbrisi_geslo():
    podatki = request.get_json()
    geslo_id = podatki.get('id')

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM slovar WHERE ID=?", (geslo_id,))
        conn.commit()
        conn.close()

        return jsonify({"sporocilo": "Geslo uspešno izbrisano!"}), 200
    except sqlite3.Error as e:
        return jsonify({"napaka": f"Napaka pri brisanju gesla: {e}"}), 500




# ŠTEVEC GESEL

@app.route('/stevilo_gesel', methods=['GET'])
def stevec():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS st FROM slovar")
    stevilo = cur.fetchone()[0]
    conn.close()
    return jsonify({"stevilo": stevilo})



# Popravljena funkcija za iskanje po vzorcu

@app.route('/isci_po_vzorcu', methods=['POST'])
def isci_po_vzorcu():
    vzorec = request.form['vzorec'].strip().upper()
    dolzina = int(request.form['dolzina'])

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()

    # Pomembno: uporabimo TRIM(GESLO), če so v bazi presledki
    cur.execute("SELECT TRIM(GESLO), OPIS FROM slovar WHERE LENGTH(TRIM(GESLO)) = ? AND GESLO LIKE ?", (dolzina, vzorec))
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]

    return jsonify(gesla)






# Popravljena funkcija za iskanje po opisu

@app.route('/isci_po_opisu', methods=['POST'])
def isci_po_opisu():
    kljucna_beseda = request.form['opis'].strip().upper()

    if not kljucna_beseda:
        return jsonify({'error': 'Vnesi ključno besedo za iskanje po opisu.'}), 400

    conn = sqlite3.connect('VUS.db')
    cur = conn.cursor()

    besede = kljucna_beseda.split()

    pogoji = []
    params = []

    for beseda in besede:
        if beseda.isdigit():  # Če je številka (leto), išči prosto
            pogoji.append("UPPER(OPIS) LIKE ?")
            params.append(f"%{beseda}%")
        else:  # Če je beseda, išči kot celotno besedo
            pogoji.append("(UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ? OR UPPER(OPIS) LIKE ?)")
            params.extend([
                beseda + ' %',        # na začetku
                '% ' + beseda + ' %', # v sredini
                '% ' + beseda,        # na koncu
                beseda                # samo beseda
            ])

    sql = "SELECT GESLO, OPIS FROM slovar WHERE " + " AND ".join(pogoji)

    cur.execute(sql, params)
    rezultati = cur.fetchall()
    conn.close()

    gesla = [{'geslo': g, 'opis': o} for g, o in rezultati]

    return jsonify(gesla)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))



