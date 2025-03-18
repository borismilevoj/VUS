document.addEventListener('DOMContentLoaded', () => {
    stevecGesel();
});

// 📊 ŠTEVEC GESEL
function stevecGesel() {
    fetch('/stevilo_gesel')
        .then(res => res.json())
        .then(data => {
            document.getElementById('stevec').innerText = `📊 Število gesel: ${data.stevilo}`;
        });
}

// ➕ DODAJ GESLO
function dodajGeslo() {
    const novoGeslo = document.getElementById('novo-geslo').value.trim();
    const opisGeslo = document.getElementById('opis-geslo').value.trim();

    if (!novoGeslo || !opisGeslo) {
        alert('Obvezno vnesi geslo in opis!');
        return;
    }

    fetch('/dodaj_geslo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ geslo: novoGeslo, opis: opisGeslo })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.sporocilo || data.napaka);
        preveriGeslo();
        stevecGesel();
        document.getElementById('novo-geslo').value = '';
        document.getElementById('opis-geslo').value = '';
    });
}

// 🔍 PREVERI GESLO
function preveriGeslo() {
    const gesloInput = document.getElementById('preveri-geslo');
    const geslo = gesloInput.value.trim();

    if (!geslo) {
        alert('Vnesi geslo za preverjanje!');
        return;
    }

    fetch('/preveri_geslo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ geslo })
    })
    .then(res => res.json())
    .then(data => {
        prikaziZadetke(data.zadetki);
    });
}

// ✅ PRIKAZI ZADETKE
function prikaziZadetke(zadetki) {
    const tabela = document.querySelector('#tabela-gesel tbody');
    tabela.innerHTML = '';

    zadetki.forEach(geslo => {
        tabela.innerHTML += `
            <tr>
                <td>${geslo.id}</td>
                <td>${geslo.geslo}</td>
                <td>${geslo.opis}</td>
                <td>
                    <button onclick="urediGeslo(${geslo.id}, '${geslo.geslo}', '${geslo.opis}')" class="btn-uredi">✏️ Uredi</button>
                    <button onclick="izbrisiGeslo(${geslo.id})" class="btn-brisi">🗑️ Briši</button>
                </td>
            </tr>`;
    });
}

// 🔄 PONASTAVI REZULTATE
function ponastaviRezultate() {
    document.getElementById('preveri-geslo').value = '';
    document.querySelector('#tabela-gesel tbody').innerHTML = '';
}

// ✏️ UREDI GESLO
function urediGeslo(id, geslo, opis) {
    let noviOpis = prompt(`Nov opis za geslo "${geslo}":`, opis);
    if (noviOpis && noviOpis !== opis) {
        fetch("/uredi_geslo", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ id, novi_opis: noviOpis })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.sporocilo || data.napaka);
            preveriGeslo();
        });
    }
}

// 🗑️ BRIŠI GESLO
function izbrisiGeslo(id) {
    if (!confirm('Ste prepričani, da želite izbrisati to geslo?')) return;

    fetch('/izbrisi_geslo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.sporocilo || data.napaka);
        ponastaviRezultate();
        stevecGesel();
    });
}

// 🔍 ISKANJE PO OPISU
function isciPoOpisu() {
    const opis = document.getElementById('isci-input').value.trim();

    fetch('/isci_po_opisu', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ iskanje: opis })
    })
    .then(res => res.json())
    .then(data => {
        prikaziZadetke(data.rezultati);
    });
}

// 🔄 PONASTAVI
function ponastaviRezultate() {
    document.getElementById('preveri-geslo').value = '';
    document.querySelector('#tabela-gesel tbody').innerHTML = '';
}
