// 🔍 PREVERJANJE GESLA
async function preveriGeslo() {
    const geslo = document.getElementById('preveri-geslo').value.trim().toUpperCase();

    if (!geslo) {
        alert("Najprej vpiši geslo!");
        return;
    }

    try {
        const response = await fetch('/preveri', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({geslo: geslo})
        });

        const data = await response.json();

        if (response.ok) {
            prikaziZadetke(data.rezultati);
            alert(data.sporocilo);
        } else {
            alert(data.sporocilo);
        }

    } catch (e) {
        alert("Napaka pri komunikaciji s strežnikom!");
    }
}

// ➕ DODAJANJE GESLA
async function dodajGeslo() {
    const geslo = document.getElementById('novo-geslo').value.trim().toUpperCase();
    const opis = document.getElementById('opis-geslo').value.trim();

    if (!geslo || !opis) {
        alert("Vnesi geslo in opis!");
        return;
    }

    try {
        const response = await fetch('/dodaj', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({geslo: geslo, opis: opis})
        });

        const data = await response.json();

        if (response.ok) {
            alert("Geslo uspešno dodano!");
            document.getElementById('novo-geslo').value = '';
            document.getElementById('opis-geslo').value = '';
            stevecGesel();
        } else {
            alert(data.sporocilo);
        }

    } catch (e) {
        alert("Napaka pri dodajanju gesla!");
    }
}

// 📋 PRIKAZ ZADETKOV V TABELI
function prikaziZadetke(zadetki) {
    const tabela = document.querySelector('#tabela-gesel tbody');
    tabela.innerHTML = '';

    zadetki.forEach(z => {
        const vrstica = document.createElement('tr');

        vrstica.innerHTML = `
            <td>${z.id}</td>
            <td>${z.geslo}</td>
            <td>
                <span contenteditable="true" id="opis-${z.id}" style="padding:4px;">${z.opis}</span>
                <button onclick="shraniOpis(${z.id})">💾</button>
            </td>
            <td><button onclick="izbrisiGeslo(${z.id})">🗑</button></td>
        `;

        tabela.appendChild(vrstica);
    });
}

// 💾 SHRANJEVANJE SPREMEMBE OPISA
async function shraniOpis(id) {
    const opisSpan = document.getElementById(`opis-${id}`);
    const noviOpis = opisSpan.innerText.trim();

    try {
        const response = await fetch('/uredi_geslo', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: id, novi_opis: noviOpis})
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.napaka || "Napaka pri shranjevanju opisa.");
        } else {
            // Vizualna potrditev
            opisSpan.style.backgroundColor = '#d4edda';
            opisSpan.title = "Posodobljeno!";
            setTimeout(() => {
                opisSpan.style.backgroundColor = '';
                opisSpan.title = '';
            }, 1500);
        }
    } catch (e) {
        alert("Napaka pri komunikaciji s strežnikom.");
    }
}

// 🗑 BRISANJE GESLA
async function izbrisiGeslo(id) {
    if (!confirm("Ali res želiš izbrisati to geslo?")) return;

    try {
        const response = await fetch('/izbrisi_geslo', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: id})
        });

        const data = await response.json();

        if (response.ok) {
            alert("Geslo izbrisano.");
            ponastaviRezultate();
            stevecGesel();
        } else {
            alert(data.napaka || "Napaka pri brisanju.");
        }

    } catch (e) {
        alert("Napaka pri komunikaciji s strežnikom.");
    }
}

// 🔄 PONASTAVI REZULTATE
function ponastaviRezultate() {
    document.getElementById('preveri-geslo').value = '';
    document.querySelector('#tabela-gesel tbody').innerHTML = '';
}

// 📊 PRIDOBI ŠTEVEC GESEL
async function stevecGesel() {
    try {
        const response = await fetch('/stevilo_gesel');
        const data = await response.json();
        document.getElementById('stevec').textContent = `📊 Število gesel: ${data.stevilo}`;
    } catch (e) {
        console.error('Napaka pri pridobivanju števila gesel');
    }
}
