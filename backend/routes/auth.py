from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database import connect_db
import bcrypt

auth_bp = Blueprint("auth", __name__)

# ============================================================
# --- 1. HALAMAN LOGIN (USER & ADMIN) ---
# ============================================================


@auth_bp.route("/login-user")
def login_user():
    """Menampilkan halaman login untuk pelanggan."""
    return render_template("login_user.html")


@auth_bp.route("/login-admin")
def login_admin():
    """Menampilkan halaman login khusus pengelola (Admin)."""
    return render_template("login_admin.html")


@auth_bp.route("/login-process", methods=["POST"])
def login_process():
    """Proses verifikasi login menggunakan Bcrypt."""
    email_input = request.form.get("email")
    password_input = request.form.get("password")

    conn = connect_db()
    if conn is None:
        return "Gagal koneksi ke database!"

    try:
        cursor = conn.cursor(dictionary=True)

        # Cari user berdasarkan email
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email_input,))
        user = cursor.fetchone()

        # LOGIKA : Cek apakah user ada DAN password cocok (setelah di-decode)
        # bcrypt.checkpw membandingkan password ketikan dengan password ter-hash di DB
        if user and bcrypt.checkpw(
            password_input.encode("utf-8"), user["password"].encode("utf-8")
            # UTF-8 itu standar/aturan yang menentukan huruf mana dapat nomor berapa.
            # trus dijadiin bit. 
        ):
        # cek dulu string dari  user baru di encode jadi bytes bandingin pake checkpw

            # Simpan data user ke Session (ingatan server)
            session["user_id"] = user["id"]
            session["user_nama"] = user["nama"]
            session["role"] = user["role"]

            # Kirim URL tujuan ke JS, biar JS yang redirect
            if user["role"] == "admin":
                return jsonify({"status": "success", "redirect": url_for("admin_page")})
                # jsonify buat ubah dict jadi json response

            return jsonify({"status": "success", "redirect": url_for("wisata.explore")})
        else:
            return jsonify({"status": "error", "message": "Email atau password salah!"}), 401

    except Exception as e:
        print(f"Login Error: {e}")
        return "Internal Server Error", 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ============================================================
# --- 2. PROSES PENDAFTARAN (SIGNUP) ---
# ============================================================


@auth_bp.route("/signup-new")
def signup_new():
    """Halaman pendaftaran akun baru."""
    return render_template("signup_new.html")


@auth_bp.route("/signup-process", methods=["POST"])
def signup_process():
    """Proses simpan akun baru dengan Cek Email Duplikat & JSON Response."""
    nama_input = request.form.get("nama")
    email_input = request.form.get("email")
    password_input = request.form.get("password")
    role_input = request.form.get("role")

    conn = connect_db()
    if conn is None:
        return jsonify({"status": "error", "message": "Gagal koneksi ke database!"}), 500
    
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. CEK EMAIL DUPLIKAT (Tarok di sini!)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email_input,))
        user_exist = cursor.fetchone()

        if user_exist:
            # Berhenti di sini kalau email sudah ada
            return jsonify({"status": "error", "message": "Email sudah terdaftar!"}), 400

        # 2. PROSES HASHING (Kalau email aman)
        hashed_password = bcrypt.hashpw(password_input.encode("utf-8"), bcrypt.gensalt())
        hashed_password = hashed_password.decode("utf-8")
        # pas diinput pasword kan string itu di encode jadi bytes lalu diacak pake hash and salt
        # baru di decode jadi string buat simpan ke db

        # 3. INSERT KE DATABASE
        query = "INSERT INTO users (nama, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nama_input, email_input, hashed_password, role_input))
        conn.commit()

        # Berikan respon sukses dalam bentuk JSON
        return jsonify({"status": "success", "message": f"Berhasil mendaftarkan {role_input}!"})

    except Exception as e:
        print(f"Signup Error: {e}")
        return jsonify({"status": "error", "message": "Gagal melakukan pendaftaran."}), 500
    finally:
        cursor.close()
        conn.close()


# ============================================================
# --- 3. PROFILE & LOGOUT ---
# ============================================================


@auth_bp.route("/update-profile", methods=["POST"])
def update_profile():
    """Fitur Edit Profile In-Place (untuk User & Admin)."""
    if "user_id" not in session:
        return "Unauthorized", 401

    nama_baru = request.form.get("nama")
    email_baru = request.form.get("email")
    user_id = session["user_id"]

    if not nama_baru or not email_baru:
        return "Data tidak lengkap", 400

    conn = connect_db()
    if conn is None:
        return "Database Error", 500
    cursor = conn.cursor()

    try:
        # Update data di database
        query = "UPDATE users SET nama = %s, email = %s WHERE id = %s"
        cursor.execute(query, (nama_baru, email_baru, user_id))
        conn.commit()

        # Update Session agar nama di header langsung berubah tanpa relogin
        session["user_nama"] = nama_baru
        return "Success", 200

    except Exception as e:
        print(f"Update Error: {e}")
        return str(e), 500
    finally:
        cursor.close()
        conn.close()


@auth_bp.route("/logout")
def logout():
    """Membersihkan seluruh session dan keluar dari sistem."""
    session.clear()  # Menghapus ID, Nama, dan Role dari memori server
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login_user"))
