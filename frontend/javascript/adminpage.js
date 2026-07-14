/* ============================================================
   VARIABEL GLOBAL
   ============================================================ */
let totalDaysAdd = 2;
let totalDaysEdit = 2;

/* Dua variabel global to save JUMLAH HARI ITINERARY nilai awalnya 2 */

/* ============================================================
   1. FITUR PROFIL ADMIN
   ============================================================ */
function enableEdit() {
// akan dipanggil saat tombol edit profile di klik

    document.getElementById('display-nama').style.display = 'none';
    document.getElementById('display-email').style.display = 'none';
    // nama sama email nya di hide dulu
    // document tuh untuk akses html nya
    // cari yg id nya display-nama gitu

    document.getElementById('input-nama').style.display = 'block';
    document.getElementById('input-email').style.display = 'block';
    // baru di tampilin biar bisa di ketik

    document.getElementById('btn-edit').style.display = 'none';
    document.getElementById('edit-actions').style.display = 'block';
    // tombol edit awal di hide atau ya diganti jadi save or cancel
}

function disableEdit() {
    document.getElementById('display-nama').style.display = 'block';
    document.getElementById('display-email').style.display = 'block';
    // tampilin nama sama email

    document.getElementById('input-nama').style.display = 'none';
    document.getElementById('input-email').style.display = 'none';
    // hide input field

    document.getElementById('btn-edit').style.display = 'block';
    document.getElementById('edit-actions').style.display = 'none';
    // show edit button and hide action
}

function saveProfile() {
    const newNama = document.getElementById('input-nama').value;
    const newEmail = document.getElementById('input-email').value;
    // ambil nilai dari inputan nama dan email
    // const itu wadah nilai yang isinya gabisa digabnti

    const formData = new FormData();
    formData.append('nama', newNama);
    formData.append('email', newEmail);
    // buat formdata terus masukin nama email yang tadi 
    // formdata itu kaya dictionary tapi disini buat dikirim ke server

    fetch("/update-profile", { method: "POST", body: formData })
    // kirim ke server (fetch ini caranya) ke http/update-profile
    // fetch itu buat kirim terima data dari server

        .then(response => {
            if (response.ok) { window.location.reload(); }
            // kalau berhasil akan reload
            else { alert("Gagal memperbarui profil."); }
        })
        .catch(error => console.error("Error:", error));
        // kalau eror karena jaringan atau apa gitu kasitau console nya
}

/* ============================================================
   2. MANAJEMEN LOKASI (ADD & EDIT)
   ============================================================ */
function showEditSearch() { document.getElementById('editLocationModal').style.display = 'flex'; }
function closeEditSearch() { document.getElementById('editLocationModal').style.display = 'none'; }
function showAddLocationModal() { document.getElementById('addPackageLocationModal').style.display = 'flex'; }
function closeAddLocationModal() { document.getElementById('addPackageLocationModal').style.display = 'none'; }
function showEditPackageLocationModal() { document.getElementById('editPackageLocationModal').style.display = 'flex'; }
function closeEditPackageLocationModal() { document.getElementById('editPackageLocationModal').style.display = 'none'; }
function confirmEditPackageLocation() {
    const select = document.getElementById('locationSelectEditPackage');
    const selectedOption = select.options[select.selectedIndex];
    if (selectedOption && selectedOption.value !== "") {
        document.getElementById('edit_selected_loc_text').innerText = "📍 Location: " + selectedOption.getAttribute('data-nama');
        document.getElementById('edit_package_location_id').value = selectedOption.value;
        closeEditPackageLocationModal();
    }
}
// buka tutup modal dan atur itu kalau muncul pake flex kalau ga muncul hide

function confirmLocationForAdd() {
    const select = document.getElementById('locationSelectAdd');
    const selectedOption = select.options[select.selectedIndex];
    // ambil elemen nya dan opsi yg dipilih itu
    // baca nya dari [] dulu

    if (selectedOption && selectedOption.value !== "") {
    // make sure pilihannya ada dan nilai nya ga kosong
        document.getElementById('selected_loc_text').innerText = "📍 Location: " + selectedOption.getAttribute('data-nama');
        // tampilin
        // jadi ini cari dulu di html kan lalu ubah pakai .innertext
        // and then gabungin teks sama nama lokasi yang dipilih
        // getAttribute itu ambil atribut data-nama dari optionnya
        // kan biasa bentuknya <option value ...></option>

        document.getElementById('add_package_location_id').value = selectedOption.value;
        // simpen id lokasinya ke hidden input (hidden karena yang dikirim ID bukan nama lokasinya)
        closeAddLocationModal();
    }
}

function selectLocationForEdit() {
    const select = document.getElementById('locationSelect');
    // element dropdownnya disimpen 

    const selectedOption = select.options[select.selectedIndex];
    // dari [nomor urut yang dipilih] ambil semua pilihannya

    if (selectedOption && selectedOption.value !== "") {
        const id = selectedOption.value;
        const nama = selectedOption.getAttribute('data-nama');
        const gambar = selectedOption.getAttribute('data-gambar');
        // ambil data nya

        document.getElementById('edit_name_input').value = nama;
        document.getElementById('edit_id_input').value = id;
        // isi dengan yang tadi diambil buat dikirim ke server

        const imgPreviewLoc = document.getElementById('edit-preview-img');
        // elemet tempat preview gambar

        if (imgPreviewLoc && gambar) {
            imgPreviewLoc.src = "/public/" + gambar;
            // sumber gambar nya diganti

            imgPreviewLoc.style.display = 'block';
            // tampilin karena awalnya kan hide gambarnya

            document.getElementById('edit-label-text').style.display = 'none';
            // text insert photo nya di hide karena udh ada gambarnya
        }
        document.getElementById('btn-delete-location').formAction = "/delete-location/" + id;
        // biar tombol hapusnya dinamis sesuai id yg dipilih

        closeEditSearch();
    }
}

/* ============================================================
   3. MANAJEMEN PAKET (ADD & EDIT)
   ============================================================ */
function showPackageSearch() {
    const modal = document.getElementById('editPackageModal');
    if (modal) modal.style.display = 'flex';
}

function closePackageSearch() {
    document.getElementById('editPackageModal').style.display = 'none';
}

function confirmPackageSelection() {
    const select = document.getElementById('packageSelect');
    if (!select) return;
    const selectedOption = select.options[select.selectedIndex];

    if (selectedOption && selectedOption.value !== "") {
        try {
            // Ambil data dasar
            const id = selectedOption.value;
            const nama = selectedOption.getAttribute('data-nama');
            const harga = selectedOption.getAttribute('data-harga');
            const gambar = selectedOption.getAttribute('data-gambar');
            const durasi = selectedOption.getAttribute('data-durasi');
            const locID = selectedOption.getAttribute('data-id-lokasi');
            const locNama = selectedOption.getAttribute('data-nama-lokasi');

            // --- BAGIAN : Ambil & Bersihkan JSON ---
            let rawItinerary = selectedOption.getAttribute('data-itinerary');
            
            // Mengisi field input teks
            document.getElementById('edit_nama_wisata').value = nama;
            document.getElementById('edit_package_id_input').value = id;
            document.getElementById('edit_package_location_id').value = locID;
            document.getElementById('edit_selected_loc_text').innerText = "📍 Location: " + (locNama || "-");

            // Format Harga
            const numHarga = parseInt(harga) || 0;
            // parseINT buat ganti sting jadi angka kalau gagal defaultnya 0

            const inputHarga = document.getElementById('edit-input-harga');
            if(inputHarga) inputHarga.value = numHarga.toLocaleString('id-ID');
            // di format sesuai kode IDN

            document.getElementById('edit_harga_asli').value = numHarga;
            // yg send to server yang ga di format karna yg pake titik justru gabisa dibaca

            // Preview Gambar
            const imgPreview = document.getElementById('edit-package-preview-img');
            if (imgPreview && gambar) {
                imgPreview.src = "/public/" + gambar;
                imgPreview.style.display = 'block';
                const label = document.getElementById('edit-package-label-text');
                if(label) label.style.display = 'none';
            }

            // PROSES ITINERARY
            totalDaysEdit = parseInt(durasi) || 2;
            let itineraryObj = {};

            if (rawItinerary && rawItinerary != 'None' && rawItinerary != null) {
                try {
                    itineraryObj = JSON.parse(rawItinerary);
                } catch (e) {
                    console.error("Failed to parse itinerary:", e);
                    itineraryObj = {};
                }
            }
                    
            // Panggil fungsi gambar (Biar list Day muncul)
            renderEditItinerary(totalDaysEdit, itineraryObj);

            // TUTUP MODAL
            closePackageSearch();

        } catch (globalError) {
            console.error("Error utama:", globalError);
            closePackageSearch();
        }
    }
}

/* ============================================================
   4. SISTEM ITINERARY DINAMIS
   ============================================================ */
function renderEditItinerary(durasi, dataItinerary) {
    const container = document.getElementById('edit_itinerary_container');
    if (!container) return;
    container.innerHTML = ""; 
    // innerHTML = "" → kosongkan isinya dulu sebelum digambar ulang. Kayak hapus papan tulis sebelum nulis lagi

    for (let i = 1; i <= durasi; i++) {
    // loop dari 1 sampai durasi nya
        const dayKey = `Day ${i}`;
        // Ambil data, kalau paket baru/kosong, tetap munculkan satu baris input kosong
        const activities = dataItinerary[dayKey] && dataItinerary[dayKey].length > 0 
                            // cek dlu apakah > 0
                           ? dataItinerary[dayKey] 
                           // kalau kondisinya bener pakai ini
                           : [""];
                           // else

        
        const dayBox = document.createElement('div');
        dayBox.className = 'day-box';
        // buat dulu elemen div tapi ini belum ditampilin di page
        
        let listItems = "";
        activities.forEach((act) => {
            listItems += `
                <li style="display: flex; align-items: center; gap: 5px; margin-bottom: 5px;">
                    <input type="text" name="day${i}[]" value="${act}" class="input-clear" placeholder="Activity">
                    <button type="button" onclick="this.parentElement.remove()" class="btn-remove">×</button>
                </li>`;
        });
        // string kosong dulu lalu loop tiap aktivitas-tambah <li></li> ke stringnya
        // tiap list isinya ada teks dan tombol hapus
        // thisparent mksdnya kalau remove li induk juga hapus

        dayBox.innerHTML = `
            <div class="day-header" style="display: flex; justify-content: space-between; align-items: center;">
                <span>Day ${i}</span>
                <button type="button" onclick="addActivityEdit(${i})" class="btn-mini">+</button>
            </div>
            <ul id="edit-list-day-${i}" style="list-style:none; padding:0;">${listItems}</ul>`;
        
        container.appendChild(dayBox);
        // baru ditarok ke page. appendChild add to container paling bawah
    }
    document.getElementById('edit_input_durasi').value = durasi;
}

function addActivityEdit(dayNum) {
 // terima input, hari mana yg mau di add activity nya

    const list = document.getElementById(`edit-list-day-${dayNum}`);
    // dayNum mksdnya ya kalau yg di klik 2 berarti nanti jadi edit-list-day-2

    const li = document.createElement('li');
    li.innerHTML = `<input type="text" name="day${dayNum}[]" class="input-clear" placeholder="Activity"><button type="button" onclick="this.parentElement.remove()" class="btn-remove">×</button>`;
    list.appendChild(li);
}

function manageDaysEdit(action) {

    if (!document.getElementById('edit_package_id_input').value) return;

    const container = document.getElementById('edit_itinerary_container');
    if (!container) return;

    // 1. Ambil data rincian yang ada di kotak input SEKARANG biar gak hilang
    let currentItinerary = {};
    for (let i = 1; i <= 4; i++) {
        const inputs = container.querySelectorAll(`input[name="day${i}[]"]`);
        if (inputs.length > 0) {
            currentItinerary[`Day ${i}`] = Array.from(inputs).map(input => input.value);
            // nilai tiap input dijadiin array
        }
    }

    // 2. Jalankan aksi tambah/kurang hari
    if (action === 'add' && totalDaysEdit < 4) {
        totalDaysEdit++;
        // Kasih baris kosong di hari baru
        if (!currentItinerary[`Day ${totalDaysEdit}`]) {
            currentItinerary[`Day ${totalDaysEdit}`] = [""];
        }
    } else if (action === 'remove' && totalDaysEdit > 1) {
        totalDaysEdit--;
    }

    // 3. Gambar ulang pakai data yang sudah kita amanin tadi
    renderEditItinerary(totalDaysEdit, currentItinerary);
}

function addActivity(dayNumber) {
// liat input nya day berapa yg di add activity

    const list = document.getElementById(`list-day-${dayNumber}`);
    const li = document.createElement('li');
    li.innerHTML = `<input type="text" name="day${dayNumber}[]" placeholder="Activity" class="input-clear"><button type="button" onclick="this.parentElement.remove()" class="btn-remove">×</button>`;
    list.appendChild(li);
}

function manageDays(action) {
// buat si add package

    if (action === 'add' && totalDaysAdd < 4) {
        totalDaysAdd++;
        document.getElementById(`day-box-${totalDaysAdd}`).style.display = 'block';
    // kalau tambah : naikin dlu hari nya baru show

    } else if (action === 'remove' && totalDaysAdd > 1) {
        document.getElementById(`day-box-${totalDaysAdd}`).style.display = 'none';
        totalDaysAdd--;
    // kalau kurang : hide dulu turunin hari nya

    }
    document.getElementById('input_durasi').value = totalDaysAdd;
    // tiap ini di call yg variabel global akan diedit. itulah yg akan dikirim ke server
}

/* ============================================================
   5. UTILS
   ============================================================ */
function formatRupiah(input) {
    let angka = input.value.replace(/[^0-9]/g, '');
    // selain 0-9 hapus (g:hapus semua)

    const hiddenHarga = document.getElementById('harga_asli') || document.getElementById('edit_harga_asli');
    // || else 

    if (hiddenHarga) hiddenHarga.value = angka;
    input.value = angka !== "" ? parseInt(angka).toLocaleString('id-ID') : "";
    // yang angka doang di simpan yang tampil yang di format
}

function showPackagePreview(input) { 
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = e => {
        // kalau file nya udah dibaca jalanin ini :
            const isEdit = input.name === 'package_photo_edit' || input.name === 'location_photo_edit';
            // isEdit itu bool. 

            const imgId = isEdit ? (input.name.includes('location') ? 'edit-preview-img' : 'edit-package-preview-img') : (input.name.includes('location') ? 'preview-img' : 'package-preview-img');
            const labelId = isEdit ? (input.name.includes('location') ? 'edit-label-text' : 'edit-package-label-text') : (input.name.includes('location') ? 'label-text' : 'package-label-text');
            // ini hadling :
            // isEdit=true  + location  → 'edit-preview-img'        / 'edit-label-text'
            // isEdit=true  + package   → 'edit-package-preview-img' / 'edit-package-label-text'
            // isEdit=false + location  → 'preview-img'              / 'label-text'
            // isEdit=false + package   → 'package-preview-img'      / 'package-label-text'

            const img = document.getElementById(imgId);
            const label = document.getElementById(labelId);
            // cari based id yang tadi udah ditentukan (handling)

            img.src = e.target.result;
            // hasil bacaan fileReadir (string panjang :data gambar) jadi src 

            img.style.display = 'block';
            if (label) label.style.display = 'none';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function showEditPackagePreview(input) { showPackagePreview(input); }

function deletePackageManual() {
    const packageId = document.getElementById('edit_package_id_input').value;
    if (!packageId) { alert("Pilih paket dulu lewat Search!"); return; }
    if (confirm("Hapus paket ini selamanya?")) {
        const form = document.createElement('form');
        // buat form kosong

        form.method = 'POST';
        // set method nya POST 

        form.action = '/delete-package/' + packageId;
        document.body.appendChild(form);
        form.submit();
    }
}

window.onclick = event => {
// listener klik
    if (event.target.classList.contains('modal-overlay') || event.target.classList.contains('modal-search')) {
        event.target.style.display = 'none';
    }
}
// event.target          // elemen yang diklik user
//       .classList      // daftar semua class elemen itu
//       .contains('modal-overlay')  // apakah punya class 'modal-overlay'?
// Hasilnya true atau false.
// || itu or

/* --- FUNGSI GLOBAL TOAST --- */
function showToast(message, type = "error") {
    // 1. Hapus toast lama jika masih ada (biar gak tumpuk)
    const oldToast = document.querySelector(".toast-popup");
    if (oldToast) oldToast.remove();

    // 2. Buat elemen toast baru
    const toast = document.createElement("div");
    toast.className = `toast-popup ${type}`;
    toast.innerText = message;

    document.body.appendChild(toast);

    // 3. Efek menghilang otomatis
    setTimeout(() => {
        toast.classList.add("hide");
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

// Taruh ini di dalam document.addEventListener('DOMContentLoaded', ...) atau di paling bawah
const formRegister = document.getElementById('form-register-admin');

if (formRegister) {
    formRegister.addEventListener('submit', function(e) {
        e.preventDefault(); // Mencegah pindah halaman

        const formData = new FormData(this);

        fetch("/signup-process", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                showToast(data.message, "success"); // Muncul kotak hijau
                formRegister.reset(); // Kosongkan input
            } else {
                showToast(data.message, "error"); // Muncul kotak merah (Email Duplikat)
            }
        })
        .catch(err => {
            console.error(err);
            showToast("Terjadi kesalahan koneksi!");
        });
    });
}