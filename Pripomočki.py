# ŠTEVEC GESEL v app.py
@app.route("/stevilo_gesel", methods=["GET"])
def stevilo_gesel():
    con = sqlite3.connect("veliki_ugankarski_slovar.db")
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM slovar")
    stevilo = cur.fetchone()[0]
    con.close()
    return jsonify({"stevilo": stevilo})

