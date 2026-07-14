import os
import json
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
)
from database import connect_db
from werkzeug.utils import secure_filename
# buat rapiin nama file yg di upload

from datetime import datetime, timedelta

wisata_bp = Blueprint("wisata", __name__)

# ==========================================
# --- 1. UNTUK USER (EXPLORE PAGE) ---
# ==========================================

@wisata_bp.route("/explore")
def explore():
    """Fungsi untuk menampilkan katalog wisata dan menghitung jumlah item di keranjang."""
    conn = connect_db()
    if conn is None:
        return "Database mati!"
    cursor = conn.cursor(dictionary=True)

    # 1. Mengambil data semua lokasi untuk ditampilkan di grid atas
    cursor.execute("SELECT * FROM lokasi")
    daftar_lokasi = cursor.fetchall()

    # 2. Mengambil semua paket wisata dan menggabungkan (JOIN) dengan nama lokasi terkait
    query_paket = """
        SELECT wisata.*, lokasi.nama_lokasi 
        FROM wisata 
        JOIN lokasi ON wisata.id_lokasi = lokasi.id
        ORDER BY lokasi.nama_lokasi ASC, wisata.created_at DESC
    """
    cursor.execute(query_paket)
    daftar_paket = cursor.fetchall()

    # 3. LOGIKA BADGE: Menghitung total quantity (QTY) item yang masih berstatus 'cart'
    cart_count = 0
    if "user_id" in session:
        query_count = """
            SELECT SUM(pd.qty) as total 
            FROM pemesanan_detail pd
            JOIN pemesanan p ON pd.id_pemesanan = p.id
            WHERE p.id_user = %s AND p.status = 'cart'
        """
        cursor.execute(query_count, (session["user_id"],))
        result = cursor.fetchone()
        if result and result["total"]:
            cart_count = result["total"]

    cursor.close()
    conn.close()

    # 4. Mengirim data lokasi, paket, dan jumlah keranjang ke halaman user
    return render_template(
        "page_user.html",
        locations=daftar_lokasi,
        packages=daftar_paket,
        cart_count=cart_count,
    )


# ==========================================
# --- 2. UNTUK ADMIN (LOGIKA LOKASI) ---
# ==========================================


@wisata_bp.route("/add-location", methods=["POST"])
def add_location():
    """Fungsi Admin untuk menambah lokasi baru beserta upload gambar."""
    nama_baru = request.form.get("new_location_name")
    file = request.files.get("location_photo")

    if nama_baru and file:
        # Mengamankan nama file dan menentukan jalur penyimpanan
        filename = secure_filename(file.filename)
        upload_path = os.path.join(os.getcwd(), "frontend", "public", filename)
        # getcwd() Get Current Working Directory — mengambil path folder tempat program Python sedang berjalan.

        file.save(upload_path)

        conn = connect_db()
        cursor = conn.cursor()
        # Memasukkan nama lokasi dan nama file gambar ke database
        query = "INSERT INTO lokasi (nama_lokasi, gambar) VALUES (%s, %s)"
        cursor.execute(query, (nama_baru, filename))

        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for("admin_page"))


@wisata_bp.route("/edit-location", methods=["POST"])
def edit_location():
    """Fungsi Admin untuk mengubah data lokasi (Nama/Gambar)."""
    loc_id = request.form.get("location_id")
    nama_baru = request.form.get("edit_location_name")
    file = request.files.get("location_photo_edit")

    conn = connect_db()
    cursor = conn.cursor()

    # Logika pengecekan: Jika admin mengupload file baru, perbarui gambar. Jika tidak, cukup perbarui nama.
    if file and file.filename != "":
    # kalau ada foto baru
        filename = secure_filename(file.filename)
        upload_path = os.path.join(os.getcwd(), "frontend", "public", filename)
        file.save(upload_path)

        query = "UPDATE lokasi SET nama_lokasi = %s, gambar = %s WHERE id = %s"
        cursor.execute(query, (nama_baru, filename, loc_id))
    else:
        query = "UPDATE lokasi SET nama_lokasi = %s WHERE id = %s"
        cursor.execute(query, (nama_baru, loc_id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("admin_page"))


@wisata_bp.route("/delete-location/<int:loc_id>", methods=["POST"])
def delete_location(loc_id):
    """Fungsi Admin untuk menghapus lokasi dan membersihkan file gambar fisiknya."""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # 1. Mengambil nama file gambar sebelum data di database dihapus
    cursor.execute("SELECT gambar FROM lokasi WHERE id = %s", (loc_id,))
    target = cursor.fetchone()

    if target:
        nama_file = target["gambar"]
        file_path = os.path.join(os.getcwd(), "frontend", "public", nama_file)

        # 2. Menghapus file secara fisik dari folder agar penyimpanan tidak penuh (sampah data)
        if (
            nama_file
            and nama_file != "default_lokasi.jpg"
            and os.path.exists(file_path)
        ):
            try:
                os.remove(file_path)
                print(f"✅ File {nama_file} berhasil dihapus.")
            except Exception as e:
                print(f"❌ Gagal menghapus file: {e}")

        # 3. Menghapus baris data lokasi dari database
        cursor.execute("DELETE FROM lokasi WHERE id = %s", (loc_id,))
        conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("admin_page"))


# ==========================================
# --- 3. UNTUK ADMIN (LOGIKA PAKET) ---
# ==========================================


@wisata_bp.route("/add-package", methods=["POST"])
def add_package():
    """Fungsi Admin untuk menambah paket wisata baru dengan Itinerary format JSON."""
    id_lokasi = request.form.get("id_lokasi")
    nama_wisata = request.form.get("nama_wisata")
    harga = request.form.get("harga")
    durasi = int(request.form.get("durasi", 2))
    file = request.files.get("package_photo")

    # Mengolah input dinamis kegiatan per hari menjadi struktur Dictionary (Map)
    itinerary_map = {}
    for i in range(1, durasi + 1):
    # loop tiap hari sesuai durasi

        kegiatan = request.form.getlist(f"day{i}[]")
        # Ambil list kegiatan per hari dari form
        # .getlist() dipakai kalau satu name HTML bisa punya lebih dari satu nilai — seperti itinerary per hari yang bisa diisi banyak kegiatan.

        itinerary_map[f"Day {i}"] = [k for k in kegiatan if k.strip() != ""]
        # simpen ke map tadi yg kosong di buang

    # Mengonversi Dictionary ke format string JSON untuk disimpan di database
    deskripsi_json = json.dumps(itinerary_map)

    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(os.getcwd(), "frontend", "public", filename)
        file.save(upload_path)
        # upload foto ke folder trs file foto nya simpan ke server

        conn = connect_db()
        cursor = conn.cursor()
        query = """
            INSERT INTO wisata (id_lokasi, nama_wisata, harga, durasi, deskripsi, gambar) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query, (id_lokasi, nama_wisata, harga, durasi, deskripsi_json, filename)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for("admin_page"))


@wisata_bp.route("/edit-package", methods=["POST"])
def edit_package():
    """Fungsi Admin untuk mengubah detail paket wisata dan Itinerary."""
    p_id = request.form.get("package_id")
    id_lokasi = request.form.get("id_lokasi")
    nama_wisata = request.form.get("nama_wisata")
    harga = request.form.get("harga")  # Mengambil angka murni tanpa format ribuan
    durasi = int(request.form.get("durasi", 2))
    file = request.files.get("package_photo_edit")

    # Memproses ulang daftar kegiatan per hari menjadi JSON
    itinerary_map = {}
    for i in range(1, durasi + 1):
        kegiatan = request.form.getlist(f"day{i}[]")
        itinerary_map[f"Day {i}"] = [k for k in kegiatan if k.strip() != ""]

    deskripsi_json = json.dumps(itinerary_map)

    conn = connect_db()
    cursor = conn.cursor()

    if file and file.filename != "":
        # Update data lengkap termasuk mengganti foto lama dengan yang baru
        filename = secure_filename(file.filename)
        upload_path = os.path.join(os.getcwd(), "frontend", "public", filename)
        file.save(upload_path)

        query = """
            UPDATE wisata 
            SET id_lokasi=%s, nama_wisata=%s, harga=%s, durasi=%s, deskripsi=%s, gambar=%s 
            WHERE id=%s
        """
        cursor.execute(
            query,
            (id_lokasi, nama_wisata, harga, durasi, deskripsi_json, filename, p_id),
        )
    else:
        # Update data saja tanpa menyentuh kolom gambar
        query = """
            UPDATE wisata 
            SET id_lokasi=%s, nama_wisata=%s, harga=%s, durasi=%s, deskripsi=%s 
            WHERE id=%s
        """
        cursor.execute(
            query, (id_lokasi, nama_wisata, harga, durasi, deskripsi_json, p_id)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("admin_page"))


@wisata_bp.route("/delete-package/<int:package_id>", methods=["POST"])
def delete_package(package_id):
    """Fungsi Admin untuk menghapus paket dan membersihkan file fotonya."""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # 1. Mencari nama gambar di database sebelum data ditiadakan
    cursor.execute("SELECT gambar FROM wisata WHERE id = %s", (package_id,))
    row = cursor.fetchone()

    if row:
        nama_file = row["gambar"]
        if nama_file:
            base_dir = os.getcwd()
            file_path = os.path.join(base_dir, "frontend", "public", nama_file)

            # 2. Menghapus file gambar dari komputer jika filenya memang ada
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"✅ File {nama_file} berhasil dihapus secara fisik.")
                except Exception as e:
                    print(f"❌ Gagal menghapus file fisik: {e}")
            else:
                print(f"⚠️ File tidak ditemukan di path: {file_path}")

        # 3. Menghapus data paket dari database MySQL
        cursor.execute("DELETE FROM wisata WHERE id = %s", (package_id,))
        conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("admin_page"))


# ==========================================
# --- 4. KERANJANG & TRANSAKSI (USER) ---
# ==========================================


@wisata_bp.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    """Fungsi User untuk memasukkan paket ke keranjang dan menghitung End Date otomatis."""
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Login dulu ya!"}), 401

    data = request.get_json()
    p_id = data.get("package_id")
    qty = int(data.get("qty", 1))
    start_date_str = data.get("start_date")
    u_id = session["user_id"]

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # LOGIKA OTOMATIS: Ambil durasi paket untuk menghitung End Date (Kapan perjalanan selesai)
        cursor.execute("SELECT harga, durasi FROM wisata WHERE id = %s", (p_id,))
        paket = cursor.fetchone()

        total_item = paket["harga"] * qty
        durasi = paket["durasi"] if paket["durasi"] else 1

        # Mengolah tanggal menggunakan library datetime
        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
        # bentuk tanggal itu diubah jadi objek tanggal (awalnya string)

        end_dt = start_dt + timedelta(days=durasi - 1)
        # hitung

        end_date_str = end_dt.strftime("%Y-%m-%d")
        # ubah jadi string lagi untuk ditampilin

        # STEP 1: Mencari keranjang yang sedang aktif (status 'cart') milik user
        cursor.execute(
            "SELECT id FROM pemesanan WHERE id_user = %s AND status = 'cart' LIMIT 1",
            (u_id,),
        )
        # LIMIT 1 pengaman jadi 1 user 1 cart

        keranjang = cursor.fetchone()

        if keranjang:
            id_p = keranjang["id"]
            # Sinkronisasi total harga dan update rentang tanggal di tabel induk (Parent)
            cursor.execute(
                """
                UPDATE pemesanan 
                SET total_harga = total_harga + %s, start_date = %s, end_date = %s 
                WHERE id = %s
            """,
                (total_item, start_date_str, end_date_str, id_p),
            )
        else:
            # Jika belum punya keranjang aktif, buat baris baru di tabel pemesanan
            query_p = """
                INSERT INTO pemesanan (id_user, total_harga, status, start_date, end_date) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                query_p, (u_id, total_item, "cart", start_date_str, end_date_str)
            )
            id_p = cursor.lastrowid

        # STEP 2: Mencatat detail paket di tabel pemesanan_detail (Child)
        cursor.execute(
            "SELECT id FROM pemesanan_detail WHERE id_pemesanan = %s AND id_wisata = %s",
            (id_p, p_id),
        )
        detail = cursor.fetchone()

        if detail:
            # Jika paket yang sama ditambah lagi, cukup perbarui qty dan subtotalnya
            cursor.execute(
                "UPDATE pemesanan_detail SET qty = qty + %s, subtotal = subtotal + %s WHERE id = %s",
                (qty, total_item, detail["id"]),
            )
        else:
            # Jika paket berbeda, tambahkan baris baru di detail
            cursor.execute(
                "INSERT INTO pemesanan_detail (id_pemesanan, id_wisata, qty, subtotal) VALUES (%s, %s, %s, %s)",
                (id_p, p_id, qty, total_item),
            )

        conn.commit()
        return jsonify({"status": "success", "message": "Berhasil masuk keranjang!"})

    except Exception as e:
        if conn:
            conn.rollback()
        print("SQL ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@wisata_bp.route("/delete-cart-item/<int:detail_id>", methods=["POST"])
def delete_cart_item(detail_id):
    """Fungsi User untuk menghapus satu item dari keranjang dan mengupdate total bayar."""
    if "user_id" not in session:
        return redirect(url_for("auth.login_user"))

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Mengambil data subtotal item yang mau dihapus untuk mengurangi total_harga di Parent
        # parent : pemesanan, child : pemesanan_detail
        # pemesanan tidak tahu paket apa yang dipesan — itu urusan pemesanan_detail.
        # pemesanan_detail tidak tahu siapa yang pesan — itu urusan pemesanan.
        # Keduanya dihubungkan lewat id_pemesanan.
        
        cursor.execute(
            "SELECT id_pemesanan, subtotal FROM pemesanan_detail WHERE id = %s",
            (detail_id,),
        )
        # ambil data item yg mau dihapus
        # ambil subtotal karena mau dipakai buat hitung di parent
        item = cursor.fetchone()

        if item:
            id_p = item["id_pemesanan"]
            sub = item["subtotal"]

            # 2. Menghapus item dari tabel pemesanan_detail
            cursor.execute("DELETE FROM pemesanan_detail WHERE id = %s", (detail_id,))
            # hapus item dari child 

            # 3. Mengurangi total_harga di tabel pemesanan (Parent)
            cursor.execute(
                "UPDATE pemesanan SET total_harga = total_harga - %s WHERE id = %s",
                (sub, id_p),
            )

            # 4. Jika setelah dihapus keranjang kosong (0 item), hapus baris induk pemesanannya juga
            cursor.execute(
                "SELECT COUNT(*) as sisa FROM pemesanan_detail WHERE id_pemesanan = %s",
                (id_p,),
            )
            # di cart ada sisa berapa item
            if cursor.fetchone()["sisa"] == 0:
                cursor.execute("DELETE FROM pemesanan WHERE id = %s", (id_p,))
                # hapus cart nya
            # kalau != 0 biarin aja tetep

            conn.commit()
    except Exception as e:
        print("Error Delete:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("order_page"))


@wisata_bp.route("/checkout", methods=["POST"])
def checkout():
    """Fungsi User untuk melakukan konfirmasi pembayaran (Checkout)."""
    if "user_id" not in session:
        return redirect(url_for("auth.login_user"))

    u_id = session["user_id"]
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Mencari apakah ada keranjang aktif ('cart') milik user
        cursor.execute(
            "SELECT id FROM pemesanan WHERE id_user = %s AND status = 'cart'", (u_id,)
        )
        keranjang = cursor.fetchall()

        if keranjang:
            # 2. Mengubah status pemesanan menjadi 'paid' (Sudah dibayar)
            query = "UPDATE pemesanan SET status = 'paid' WHERE id_user = %s AND status = 'cart'"
            cursor.execute(query, (u_id,))
            conn.commit()
            print(f"✅ User {u_id} berhasil checkout!")
        else:
            print("⚠️ Tidak ada item di keranjang untuk checkout.")

    except Exception as e:
        if conn:
            conn.rollback()
        print("CHECKOUT ERROR:", str(e))
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("order_page"))


@wisata_bp.route("/update-cart-full", methods=["POST"])
def update_cart_full():
    """Fungsi untuk update Quantity (QTY) dan Tanggal langsung di halaman Order via AJAX/Fetch."""
    data = request.get_json()
    # karena bentuk data nya json
    
    detail_id = data.get("id")
    new_date = data.get("date")
    new_qty = int(data.get("qty"))

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Mendapatkan harga paket untuk menghitung subtotal baru
        cursor.execute(
            """
            SELECT pd.id_pemesanan, w.harga 
            FROM pemesanan_detail pd 
            JOIN wisata w ON pd.id_wisata = w.id 
            WHERE pd.id = %s
        """,
            (detail_id,),
        )
        res = cursor.fetchone()

        if res:
            id_p = res["id_pemesanan"]
            new_subtotal = res["harga"] * new_qty

            # 2. Memperbarui tanggal di tabel Parent (Pemesanan)
            cursor.execute(
                "UPDATE pemesanan SET start_date = %s WHERE id = %s", (new_date, id_p)
            )

            # 3. Memperbarui Qty dan Subtotal di tabel Child (Detail)
            cursor.execute(
                "UPDATE pemesanan_detail SET qty = %s, subtotal = %s WHERE id = %s",
                (new_qty, new_subtotal, detail_id),
            )

            # 4. Menghitung ulang (SUM) total harga keseluruhan keranjang tersebut
            cursor.execute(
                "SELECT SUM(subtotal) as total FROM pemesanan_detail WHERE id_pemesanan = %s",
                (id_p,),
            )
            total_baru = cursor.fetchone()["total"]
            cursor.execute(
                "UPDATE pemesanan SET total_harga = %s WHERE id = %s",
                (total_baru, id_p),
            )

            conn.commit()
            return jsonify({"status": "success"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()
