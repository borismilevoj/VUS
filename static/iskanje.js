document.addEventListener('DOMContentLoaded', () => {
    const izbiraDolzine = document.getElementById('dolzina-gesla');
    izbiraDolzine.addEventListener('change', prikaziPoljaZaCrke);
});

function prikaziPoljaZaCrke(dolzina) {
    dolzina = parseInt(dolzina);
    const crkeInput = document.querySelectorAll('.crka-input');

    crkeInput.forEach((polje, index) => {
        if (index < dolzina) {
            polje.disabled = false;
            polje.style.backgroundColor = '#ffffff';
        } else {
            polje.disabled = true;
            polje.value = '';
            polje.style.backgroundColor = '#dddddd';
        }
    });

    if (dolzina > 0) crkeInput[0].focus();
}

        });
    });
}

// ✅ Preverjanje gesla v bazi
function preveriGeslo() {
    const geslo = document.getElementById('preveri-geslo-input').value.trim();

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
        if (data.zadetki && data.zadetki.length > 0) {
            prikaziZadetke(data.zadetki);
        } else {
            alert('Gesla ni v bazi.');
        }
    })
    .catch(err => console.error("Napaka: ", err));
}


function isciPoVzorcu() {
    const dolzina = document.getElementById('dolzina-gesla').value;
    const crkeInputs = document.querySelectorAll('.crka-input');

    let vzorec = '';
    crkeInputs.forEach(input => {
        vzorec += input.value.trim() || '_';
    });

    fetch('/isci_po_vzorcu', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vzorec })
    })
    .then(res => res.json())
    .then(data => {
        if (data.rezultati && data.rezultati.length > 0) {
            prikaziZadetke(data.rezultati);
        } else {
            alert('Ni zadetkov za vnešeni vzorec.');
        }
    })
    .catch(err => console.error("Napaka: ", err));
}



function isciPoOpisu() {
    const opis = document.getElementById('isci-input').value.trim();
    if (!opis) {
        alert('Vnesi nekaj za iskanje!');
        return;
    }

    fetch('/isci_po_opisu', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ iskanje: opis })
    })
    .then(res => res.json())
    .then(data => {
        if (data.rezultati && data.rezultati.length > 0) {
            prikaziZadetke(data.rezultati);
        } else {
            alert('Ni rezultatov za iskani niz.');
        }
    })
    .catch(err => console.error("Napaka: ", err));
}

function prikaziZadetke(rezultati) {
    const tabela = document.getElementById('rezultati').getElementsByTagName('tbody')[0];
    tabela.innerHTML = '';

    rezultati.forEach(({ geslo, opis }) => {
        const vrstica = tabela.insertRow();
        vrstica.insertCell(0).textContent = geslo;
        vrstica.insertCell(1).textContent = opis;
    });

    document.getElementById('stevec-zadetkov').textContent = `📊 Število zadetkov: ${rezultati.length}`;
}

function ponastaviRezultate() {
    document.getElementById('isci-input').value = '';
    document.getElementById('rezultati').getElementsByTagName('tbody')[0].innerHTML = '';
    document.getElementById('stevec-zadetkov').textContent = '📊 Število zadetkov: 0';
}

function ponastaviVnos() {
    document.querySelectorAll('.crka-input').forEach(input => input.value = '');
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("✅ iskanje.js naložen!");
});

function prikaziPoljaZaCrke() {
    const dolzina = parseInt(document.getElementById('dolzina-gesla').value);
    const crkeInput = document.querySelectorAll('.crka-input');

    crkeInput.forEach((polje, index) => {
        polje.value = '';  // sprazni polja ob spremembi
        polje.disabled = index >= dolzina;
    });

    if (dolzina > 0) crkeInput[0].focus();
}
