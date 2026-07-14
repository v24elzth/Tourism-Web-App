import os
import json
from flask import (
    Flask,
    render_template,
    send_from_directory,
    session,
    redirect,
    url_for,
    flash,
)
from database import connect_db
from routes.auth import auth_bp
from routes.wisata import wisata_bp

# Inisialisasi Flask dan pengaturan folder template/static
app = Flask(__name__, template_folder="../frontend/html", static_folder="../frontend")

# Secret key wajib ada untuk fitur Session (login/logout)
app.secret_key = "rahasia"

# ============================================================
# --- REGISTER BLUEPRINTS ---
# ============================================================
# Menghubungkan file route terpisah (auth.py & wisata.py) ke aplikasi utama
app.register_blueprint(auth_bp)
app.register_blueprint(wisata_bp)

# blueprint = cara memecah satu aplikasi Flask besar jadi bagian-bagian kecil yang lebih teratur.


# Filter kustom agar Jinja2 bisa memproses data string JSON dari database menjadi Object Python
@app.template_filter("from_json")
def from_json_filter(value):
    return json.loads(value)

# di database kan bentuknya string
# di html kan loop (pake jinja2) 
# karena itu string biasa html gabisa loop karna str biasa bukan obj py
# jadi diubah dulu jadi JSON

# ============================================================
# --- ROUTE AKSES FILE (MEDIA & PUBLIC) ---
# ============================================================


@app.route("/media/<path:filename>") 
def custom_media(filename):
    """Mengakses file statis di folder media (luar folder frontend)."""
    return send_from_directory(os.path.join(app.root_path, "../media"), filename)


@app.route("/public/<path:filename>") 
def custom_public(filename):
    """Mengakses file gambar yang diupload ke folder public."""
    return send_from_directory(
        os.path.join(app.root_path, "../frontend/public"), filename
    )


# ============================================================
# --- 1. HALAMAN UTAMA (LANDING PAGE) ---
# ============================================================


@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# --- 2. HALAMAN ORDER (PROFIL & KERANJANG USER) ---
# ============================================================


@app.route("/order")
def order_page():
    # Proteksi: Pastikan hanya 'user' yang login yang bisa akses
    if "user_id" not in session or session.get("role") != "user":
        return redirect(url_for("auth.login_user"))

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Ambil informasi detail user untuk tampilan profil
        cursor.execute(
            "SELECT email, created_at, updated_at FROM users WHERE id = %s",
            # nama gausa karena udah disimpan pas login, disimpan di auth.py
            (session["user_id"],),
        )
        user_info = cursor.fetchone()
        # karena yg diambil itu sebaris

        # 2. LOGIKA : Ambil item yang masih di KERANJANG (Status: 'cart')
        query_cart = """
            SELECT 
                pd.id, pd.qty, pd.subtotal, 
                w.nama_wisata, w.harga as harga_paket, w.gambar,
                p.start_date
            FROM pemesanan_detail pd
            JOIN pemesanan p ON pd.id_pemesanan = p.id
            JOIN wisata w ON pd.id_wisata = w.id
            WHERE p.id_user = %s AND p.status = 'cart'
        """
        cursor.execute(
            query_cart,
            (session["user_id"],),
        )
        items = cursor.fetchall()

        # 3. LOGIKA : Ambil data pemesanan yang sudah sukses dibayar (Status: 'paid')
        query_paid = """
            SELECT 
                pd.id, pd.qty, pd.subtotal, 
                w.nama_wisata, w.harga as harga_paket, w.gambar,
                p.start_date
            FROM pemesanan_detail pd
            JOIN pemesanan p ON pd.id_pemesanan = p.id
            JOIN wisata w ON pd.id_wisata = w.id
            WHERE p.id_user = %s AND p.status = 'paid'
        """
        cursor.execute(
            query_paid,
            (session["user_id"],),
        )
        paid_items = cursor.fetchall()

        # Hitung total belanja khusus untuk item yang masih di keranjang
        total_bayar = sum(item["subtotal"] for item in items) if items else 0

        return render_template(
            "page_order.html",
            user_data=user_info,
            cart_items=items,
            paid_items=paid_items,
            total_pembayaran=total_bayar,
        )

    except Exception as e:
        print(f"Error di Order Page: {e}")
        return "Internal Server Error", 500
    finally:
        cursor.close()
        conn.close()


# ============================================================
# --- 3. HALAMAN ADMIN (DASHBOARD) ---
# ============================================================


@app.route("/admin-dashboard")
def admin_page():
    # Proteksi: Pastikan yang masuk adalah Admin
    if "user_id" not in session or session.get("role") != "admin":
        flash("Akses ditolak! Halaman ini khusus Admin.", "danger")
        # flash() adalah fungsi Flask untuk mengirim pesan sementara (one-time message) ke template HTML.
        return redirect(url_for("auth.login_admin"))

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Data Admin untuk Header sapaan
        cursor.execute(
            "SELECT id, nama, email, created_at, updated_at FROM users WHERE id = %s",
            (session["user_id"],),
        )
        admin_data = cursor.fetchone()

        # 2. Ambil data LOKASI untuk list dropdown
        cursor.execute("SELECT * FROM lokasi")
        daftar_lokasi = cursor.fetchall()

        # 3. Ambil data PAKET LENGKAP untuk manajemen aset wisata
        query_paket = """
            SELECT wisata.*, lokasi.nama_lokasi 
            FROM wisata 
            JOIN lokasi ON wisata.id_lokasi = lokasi.id
        """
        cursor.execute(query_paket)
        daftar_paket_semua = cursor.fetchall()

        # 4. LOGIKA AGREGASI (): Menggabungkan semua pesanan user untuk laporan Admin
        # Menggunakan SUM dan GROUP BY agar tampilan tabel rapi per pesanan
        query_orders = """
            SELECT 
                p.id, 
                u.nama as nama_user, 
                w.nama_wisata, 
                SUM(pd.qty) as qty,
                p.start_date, 
                p.end_date, 
                SUM(pd.subtotal) as total_harga 
            FROM pemesanan p
            JOIN users u ON p.id_user = u.id
            JOIN pemesanan_detail pd ON p.id = pd.id_pemesanan
            JOIN wisata w ON pd.id_wisata = w.id
            GROUP BY p.id, u.nama, w.nama_wisata, p.start_date, p.end_date
            ORDER BY p.id DESC
        """

        # Mulai dari tabel pesanan
        # Sambungkan ke user yang pesan
        # Sambungkan ke detail item yang dipesan
        # Sambungkan ke nama wisatanya

        cursor.execute(query_orders)
        daftar_orders = cursor.fetchall()

        return render_template(
            "page_admin.html",
            admin=admin_data,
            locations=daftar_lokasi,
            all_packages=daftar_paket_semua,
            orders=daftar_orders,
        )

    except Exception as e:
        print(f"Error di Admin Dashboard: {e}")
        return "Internal Server Error", 500
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Menjalankan aplikasi dalam mode debug agar otomatis restart saat kode diubah
    app.run(debug=True)
