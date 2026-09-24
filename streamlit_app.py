import io

import qrcode
import streamlit as st

st.set_page_config(page_title="Generator QR Code", page_icon="🔳")
st.title("🔳 Generator QR Code dari Link")


def buat_qr(link: str) -> bytes:
    """Membuat QR code dari link dan mengembalikannya dalam bentuk bytes PNG."""
    qr = qrcode.QRCode(
        version=None,  # ukuran menyesuaikan otomatis
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


# Form input
with st.form("form_qr"):
    judul = st.text_input("Judul Link", placeholder="Contoh: Website Kemenag Sumbar")
    link = st.text_input("Link / URL", placeholder="https://contoh.com")
    submit = st.form_submit_button("Generate QR Code")

# Proses saat tombol ditekan
if submit:
    judul = judul.strip()
    link = link.strip()

    if not judul or not link:
        st.session_state.pop("hasil", None)
        st.warning("Judul dan link wajib diisi.")
    else:
        # Tambahkan https:// bila pengguna lupa menuliskannya
        if not link.lower().startswith(("http://", "https://")):
            link = "https://" + link

        st.session_state["hasil"] = {
            "judul": judul,
            "link": link,
            "png": buat_qr(link),
        }

# Tampilkan hasil (disimpan di session_state agar tidak hilang saat klik download)
hasil = st.session_state.get("hasil")
if hasil:
    st.markdown("---")
    st.subheader(hasil["judul"])
    st.image(hasil["png"], width=300)
    st.caption(hasil["link"])

    nama_file = "".join(c if c.isalnum() else "_" for c in hasil["judul"]).strip("_")
    st.download_button(
        label="⬇️ Download QR Code (PNG)",
        data=hasil["png"],
        file_name=f"qrcode_{nama_file or 'link'}.png",
        mime="image/png",
    )
