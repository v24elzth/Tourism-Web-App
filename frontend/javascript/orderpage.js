/* ============================================================
   INITIALIZATION - Menunggu seluruh HTML dimuat sebelum jalan
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    console.log("JS Order Page Siap!");

    // 1. DEFINISI ELEMEN UI (Menangkap elemen HTML ke variabel JS)
    const btnEditProfile = document.getElementById('btn-edit-user');
    const btnCancel = document.getElementById('btn-cancel-edit');
    const btnLogout = document.getElementById('btn-logout');
    const bookingSection = document.querySelector('.booking-section');
    const cartContent = document.querySelector('.cart-content');
    const mainTitle = document.getElementById('cart-main-title');

    /* ============================================================
       2. LOGIKA PROFIL USER (EDIT-IN-PLACE)
       ============================================================ */
    // State management: untuk tahu apakah user sedang dalam mode edit atau tidak
    let isEditing = false;

    if (btnEditProfile) {
        btnEditProfile.addEventListener('click', function () {
            const displayNama = document.getElementById('display-nama');
            const editNama = document.getElementById('edit-nama');
            const displayEmail = document.getElementById('display-email');
            const editEmail = document.getElementById('edit-email');

            if (!isEditing) {
            // kebalikan dari false.
            // jadinya if true, jalan
            // Kalau sedang tidak editing → jalankan mode ini :
                // --- MODE EDIT ---
                // Sembunyikan elemen teks biasa, Munculkan input box (display block)
                displayNama.style.display = 'none';
                editNama.style.display = 'block';
                displayEmail.style.display = 'none';
                editEmail.style.display = 'block';

                // tombol change profile dijadiin save changes
                this.innerText = "Save Changes"; // Ubah teks tombol utama
                this.style.backgroundColor = "#4a3f35"; // Feedback visual (warna berubah)

                if (btnLogout) btnLogout.style.display = 'none'; // Sembunyikan Logout
                if (btnCancel) btnCancel.style.display = 'inline-block'; // Munculkan Cancel

                isEditing = true;
                // jadi pas klik lagi !isEditing jadi false kan
                // kalo false masuk ke else, simpan data

            } else {
                // --- MODE SAVE ---
                // Mengambil nilai terbaru dari input box untuk dikirim ke database
                const formData = new FormData();
                formData.append('nama', editNama.value);
                formData.append('email', editEmail.value);

                /* LOGIKA : Fetch API untuk Update Data ke Server (Flask) tanpa reload manual */
                fetch('/update-profile', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => {
                        if (response.ok) {
                            window.location.reload(); // Refresh halaman hanya jika database sukses update
                        } else {
                            alert("Gagal memperbarui profil.");
                        }
                    })
                    .catch(err => console.error("Fetch error:", err));
            }
        });
    }

    // Tombol Cancel: Mengembalikan tampilan ke semula dan membatalkan input
    if (btnCancel) {
        btnCancel.addEventListener('click', function () {
            document.getElementById('display-nama').style.display = 'inline-block';
            document.getElementById('edit-nama').style.display = 'none';
            document.getElementById('display-email').style.display = 'inline-block';
            document.getElementById('edit-email').style.display = 'none';

            btnEditProfile.innerText = "Change Profile";
            btnEditProfile.style.backgroundColor = "#a38171"; // Kembalikan warna asli

            btnCancel.style.display = 'none';
            if (btnLogout) btnLogout.style.display = 'inline-block';

            isEditing = false;
            // biar reset kan jadi bisa dipake lagi
        });
    }
});

/* ============================================================
   3. LOGIKA KERANJANG (CART) & MODAL EDIT
   ============================================================ */

/**
 * Fungsi untuk membuka modal edit item keranjang
 * @param {number} detailId - ID unik baris pemesanan
 * @param {string} currentDate - Nilai tanggal lama
 * @param {number} currentQty - Nilai jumlah peserta lama
 */

function editItem(detailId, currentDate, currentQty) {
    document.getElementById('editModal').style.display = 'block';

    // Memasukkan data lama ke dalam input modal agar user tidak ngetik dari nol
    document.getElementById('edit-detail-id').value = detailId;
    document.getElementById('edit-date').value = currentDate;
    document.getElementById('edit-qty').value = currentQty;
}

// Fungsi sederhana untuk menyembunyikan modal
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

/**
 * Fungsi Save Edit: Mengirim perubahan (Date & Qty) ke Flask route
 */
function saveEdit() {
    const detailId = document.getElementById('edit-detail-id').value;
    const newDate = document.getElementById('edit-date').value;
    const newQty = document.getElementById('edit-qty').value;

    /* LOGIKA : Data dikirim sebagai JSON (Objek JavaScript) ke Server */
    fetch('/update-cart-full', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // kasitau format data nya json
        body: JSON.stringify({
            id: detailId,
            date: newDate,
            qty: parseInt(newQty)
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload(); // Reload agar total harga di tabel terupdate otomatis
            } else {
                alert("Gagal: " + data.message);
            }
        })
        .catch(err => console.error("Error updating cart:", err));
}


// DOM = Document Object Model
// Artinya: representasi halaman HTML dalam bentuk yang bisa dibaca dan diubah oleh JS.
// Waktu browser buka halaman, dia baca HTML:

// <body>
//     <h1>Halo</h1>
//     <p>Ini paragraf</p>
// </body>
// Lalu browser ubah HTML itu jadi struktur pohon di memori:

// document
// └── body
//     ├── h1  → "Halo"
//     └── p   → "Ini paragraf"
// Struktur pohon inilah yang disebut DOM. JS bisa masuk ke pohon ini, cari elemennya, ubah isinya, hapus, tambah, dll.