import mysql.connector
from mysql.connector import Error
import json

# ===================================================================
#   1. KONEKSI & INISIALISASI DATABASE
# ===================================================================


def init_database():
    """Fungsi untuk membuat database jika belum ada di MySQL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port=3307,  # Sesuai port MariaDB/MySQL kamu
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS wisata_virtual")
        print("✅ Database 'wisata_virtual' siap digunakan.")
        cursor.close()
        conn.close()
    except Error as e:
        print("❌ Error saat inisialisasi database:", e)


def connect_db():
    """Fungsi untuk menghubungkan aplikasi ke database wisata_virtual."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="wisata_virtual",
            port=3307,
        )
        return conn
    except Error as e:
        print("❌ Gagal terhubung ke database:", e)
        return None


# ===================================================================
#   2. PEMBUATAN TABEL (SCHEMA)
# ===================================================================


def create_tables(conn):
    """Fungsi untuk membuat seluruh struktur tabel wisata virtual."""
    cursor = conn.cursor()

    # --- TABEL USERS ---
    # Menyimpan data akun baik Admin maupun Pelanggan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'user') DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)

    # --- TABEL LOKASI ---
    # Master data untuk kategori lokasi (Bali, Jakarta, dll)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lokasi (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama_lokasi VARCHAR(100) NOT NULL,
            gambar VARCHAR(255) NOT NULL DEFAULT 'default_lokasi.jpg',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)

    # --- TABEL WISATA (PAKET) ---
    # Menyimpan detail paket tour. Relasi: Satu Lokasi punya banyak paket.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wisata (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_lokasi INT NOT NULL,
            gambar VARCHAR(255) NOT NULL DEFAULT 'default_wisata.jpg',
            nama_wisata VARCHAR(100) NOT NULL,
            harga INT NOT NULL,
            durasi INT NOT NULL,
            deskripsi JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (id_lokasi) REFERENCES lokasi(id) ON DELETE CASCADE
        )
    """)

    # --- TABEL PEMESANAN (HEADER) ---
    # Mencatat transaksi utama dan status pembayaran
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pemesanan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_user INT,
            start_date DATE,
            end_date DATE,
            total_harga DECIMAL(15, 2),
            status ENUM('cart', 'paid') DEFAULT 'cart',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # --- TABEL PEMESANAN DETAIL ---
    # Rincian paket apa saja yang dibeli dalam satu transaksi (Relasi many-to-many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pemesanan_detail (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_pemesanan INT,
            id_wisata INT,
            qty INT,
            subtotal DECIMAL(15, 2),
            FOREIGN KEY (id_pemesanan) REFERENCES pemesanan(id) ON DELETE CASCADE,
            FOREIGN KEY (id_wisata) REFERENCES wisata(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    print("✅ Seluruh tabel berhasil diverifikasi/dibuat.")


# ===================================================================
#   3. DATA AWAL (DUMMY DATA)
# ===================================================================


def insert_dummy_data(conn):
    """Fungsi opsional untuk mengisi data awal agar database tidak kosong."""
    cursor = conn.cursor()

    # Cek jika data sudah ada agar tidak duplikat
    cursor.execute("SELECT COUNT(*) FROM lokasi")
    if cursor.fetchone()[0] == 0:
        # Dummy Lokasi
        cursor.execute(
            "INSERT INTO lokasi (nama_lokasi) VALUES ('Bali'), ('Jakarta'), ('Lombok')"
        )

        # Dummy Itinerary (Format JSON sesuai standar CDS)
        sample_itinerary = json.dumps(
            {
                "Day 1": ["Arrival", "Sunset at Kuta"],
                "Day 2": ["Ubud Tour", "Monkey Forest"],
            }
        )

        # Dummy Wisata
        cursor.execute(
            """
            INSERT INTO wisata (id_lokasi, nama_wisata, harga, durasi, deskripsi) 
            VALUES (1, 'Wonderful Bali', 2500000, 2, %s)
        """,
            (sample_itinerary,),
        )

        conn.commit()
        print("✅ Data dummy berhasil dimasukkan.")

    cursor.close()


# ===================================================================
#   4. EKSEKUSI UTAMA
# ===================================================================

if __name__ == "__main__":
    # Menjalankan urutan pembuatan database
    init_database()
    connection = connect_db()
    if connection:
        create_tables(connection)
        # insert_dummy_data(connection)
        connection.close()
