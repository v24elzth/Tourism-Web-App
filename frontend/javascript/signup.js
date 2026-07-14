/* ============================================================
   FUNGSI GLOBAL TOAST 
   ============================================================ */
function showToast(message, type = "error") {
    // Hapus toast lama kalau ada
    const oldToast = document.querySelector(".toast-popup");
    if (oldToast) oldToast.remove();

    // Buat elemen div baru
    const toast = document.createElement("div");
    toast.className = `toast-popup ${type}`;
    toast.innerText = message;

    document.body.appendChild(toast);

    // Animasi menghilang
    setTimeout(() => {
        toast.classList.add("hide");
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

/* ============================================================
   LOGIKA SIGNUP (USER & ADMIN)
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    // Kita cari form berdasarkan ID yang sudah kita sepakati tadi
    const formSignup = document.getElementById('form-signup-user') || 
                       document.getElementById('form-register-admin');
    // Cari form signup user atau form register admin — karena file JS ini dipakai di 2 halaman berbeda.
    // || = kalau yang pertama tidak ketemu, coba yang kedua

    if (formSignup) {
        formSignup.addEventListener('submit', function(e) {
            e.preventDefault(); // don't go

            const formData = new FormData(this);

            fetch("/signup-process", {
                method: "POST",
                body: formData
            })
            // fetch dari web ke flask

            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    showToast(data.message, "success");
                    this.reset(); // Kosongkan form
                    
                    // Kalau ini di halaman signup user, arahkan ke login setelah sukses
                    if (this.id === 'form-signup-user') {
                        setTimeout(() => {
                            window.location.href = "/login-user";
                        }, 2000);
                    }
                } else {
                    // Munculin pesan "Email sudah terdaftar!" dari Python
                    showToast(data.message, "error");
                }
            })
            .catch(err => {
                console.error(err);
                showToast("Koneksi gagal atau database mati.");
            });
        });
    }
});