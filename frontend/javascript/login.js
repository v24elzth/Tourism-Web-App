function showToast(message, type = "error") {
    const old = document.querySelector(".toast-popup");
    if (old) old.remove();
    const toast = document.createElement("div");
    toast.className = `toast-popup ${type}`;
    toast.innerText = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add("hide");
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

document.getElementById("login-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch("/login-process", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect;
            } else {
                showToast(data.message, "error");
            }
        })
        .catch(() => showToast("Terjadi kesalahan koneksi!"));
});