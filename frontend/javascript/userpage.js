/* ============================================================
   INITIALIZATION - Menjamin script jalan setelah HTML siap
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    console.log("JS Explore Page Siap!");

    // 1. DEFINISI ELEMEN UI
    const cartIcon = document.getElementById('cartIcon');
    const cartDropdown = document.getElementById('cartDropdown');
    const cartBadge = document.querySelector('.cart-badge');

    /* ============================================================
       2. LOGIKA DROPDOWN KERANJANG (NAVBAR)
       ============================================================ */
    if (cartIcon && cartDropdown) {
        // Toggle (Buka/Tutup) dropdown saat icon diklik
        cartIcon.addEventListener('click', (e) => {
        // ikon cart di klik :
            e.stopPropagation(); // Mencegah event 'bubbling' agar dropdown tidak langsung tertutup
            cartDropdown.classList.toggle('show');
        });


        // Menutup dropdown otomatis jika user klik di area mana pun di luar keranjang
        window.addEventListener('click', (e) => {
            if (!cartIcon.contains(e.target) && !cartDropdown.contains(e.target)) {
                cartDropdown.classList.remove('show');
            }
        });
        // lik di luar icon dan dropdown → tutup dropdown
        // Klik di dalam icon atau dropdown → biarkan tetap terbuka
    }

    /* ============================================================
       3. LOGIKA ADD TO CART (FETCH API)
       ============================================================ */
    const addButtons = document.querySelectorAll('.btn-add');

    addButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Mengambil metadata dari atribut data-* di HTML
            // Cari semua tombol dengan class btn-add → pasang listener di tiap tombol

            const packageId = this.getAttribute('data-id');
            const packageName = this.getAttribute('data-name');
            // ambil data dari atribut di HTML

            // LOGIKA : Mencari kontainer paket terdekat (Parent) agar tidak salah ambil data input
            const card = this.closest('.package-block');
            const dateInput = card.querySelector('.input-date');
            const qtyInput = card.querySelector('.input-qty');
            // Closest() = cari elemen parent terdekat dengan class .package-block.
            // karena di page kan kartunya banyak

            // Validasi Input di sisi Client (UX)
            if (!dateInput.value) {
                alert("Pilih tanggal keberangkatan dulu ya!");
                return;
            }
            // biar tanggal ga kosong

            // Membungkus data ke dalam Objek JSON
            const dataPemesanan = {
                package_id: packageId,
                qty: qtyInput.value,
                start_date: dateInput.value
            };

            console.log("Mengirim data pemesanan...", dataPemesanan);

            /* LOGIKA : Fetch API dengan metode POST dan Headers Application/JSON */
            fetch('/add-to-cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataPemesanan)
            })
            // kirim data as JSON ke route /add-to-cart di flask

                .then(response => {
                    // Proteksi jika user belum login (Status 401 Unauthorized)
                    if (response.status === 401) {
                        alert("Kamu harus login dulu untuk memesan.");
                        window.location.href = "/login-user";
                        return;
                    }
                    return response.json();
                })
                .then(res => {
                    if (res && res.status === 'success') {
                        alert(`${packageName} berhasil masuk keranjang!`);

                        // Update angka di Badge keranjang secara reaktif (tanpa reload)
                        if (cartBadge) {
                            let currentCount = parseInt(cartBadge.innerText) || 0;
                            cartBadge.innerText = currentCount + 1;
                            // update badge cart
                        }
                    } else if (res) {
                        alert("Gagal: " + res.message);
                    }
                })
                .catch(err => {
                    console.error("Fetch Error:", err);
                    alert("Gagal terhubung ke server. Pastikan Flask kamu menyala!");
                });
        });
    });
});