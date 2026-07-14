/* ============================================================
   DOM ELEMENTS - Mengambil elemen-elemen Carousel
   ============================================================ */
const track = document.getElementById('track');        // Wadah kartu (jalur carousel)
const btnLeft = document.getElementById('moveLeft');   // Tombol panah kiri
const btnRight = document.getElementById('moveRight'); // Tombol panah kanan
const dots = document.querySelectorAll('.dot');        // Titik-titik indikator di bawah

// Ambil semua elemen yang dibutuhkan di awal:

// track → wadah/jalur tempat kartu-kartu berjejer
// btnLeft / btnRight → tombol panah kiri & kanan
// dots → semua titik indikator di bawah carousel (querySelectorAll karena banyak)

/* ============================================================
   LOGIKA NAVIGASI CAROUSEL
   ============================================================ */

// 1. Fungsi klik tombol Kanan (Geser Maju)
btnRight.addEventListener('click', () => {
    // Menghitung lebar 1 kartu + gap (25px) agar pergeserannya pas di tengah kartu berikutnya
    const cardWidth = track.querySelector('.destination-card').offsetWidth + 25;

    // Perintah scrollBy: menggeser kontainer ke kanan (positif) sebanyak lebar kartu
    track.scrollBy({ left: cardWidth, behavior: 'smooth' });
    // geser ke kiri
});

// 2. Fungsi klik tombol Kiri (Geser Mundur)
btnLeft.addEventListener('click', () => {
    const cardWidth = track.querySelector('.destination-card').offsetWidth + 25;

    // Perintah scrollBy: menggeser kontainer ke kiri (negatif) sebanyak lebar kartu
    track.scrollBy({ left: -cardWidth, behavior: 'smooth' });
});

/* ============================================================
   SISTEM INDIKATOR (DOTS) OTOMATIS
   ============================================================ */

// 3. Fungsi "Scroll Listener": Mendeteksi posisi scroll untuk mengaktifkan titik (dots)
track.addEventListener('scroll', () => {
    const cardWidth = track.querySelector('.destination-card').offsetWidth + 25;

    /* LOGIKA : Menentukan Index Kartu
       Mengambil posisi scroll horizontal (scrollLeft) dibagi lebar satu kartu.
       Math.round() digunakan untuk membulatkan ke angka terdekat supaya titik 
       berubah tepat saat kartu melewati titik tengah.
    */
    const index = Math.round(track.scrollLeft / cardWidth);

    // Update class 'active' pada dots sesuai dengan kartu yang terlihat
    dots.forEach((dot, i) => {
        // Jika index titik (i) sama dengan index kartu aktif, tambahkan class 'active'
        // Jika tidak sama, hapus class 'active'-nya
        dot.classList.toggle('active', i === index);
    });
});

// Alur singkatnya:
// user klik → → →
// → hitung lebar kartu
// → geser carousel ke kanan
// → event scroll terpicu
// → hitung kartu mana yang tampil
// → dot yang sesuai menyala, sisanya mati