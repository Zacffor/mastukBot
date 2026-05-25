import os
import schedule
import time
import requests
import logging
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")   # Ambil dari environment
CHAT_ID   = os.getenv("CHAT_ID")     # Ambil dari environment

PESAN = "Belajar miskin"

# Jam pengiriman pesan (format 24 jam)
JAM_KIRIM = [15, 16, 17, 18, 19, 20, 21, 22]  # 15.00 - 22.00 (jam 3 sore s/d 10 malam)

# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def kirim_pesan():
    """Kirim pesan ke Telegram."""
    sekarang = datetime.now().strftime("%H:%M:%S")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": PESAN,
        "parse_mode": "HTML",
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            log.info(f"✅ Pesan berhasil dikirim pukul {sekarang}")
        else:
            log.error(f"❌ Gagal kirim pesan: {resp.status_code} - {resp.text}")
    except requests.exceptions.RequestException as e:
        log.error(f"❌ Error koneksi: {e}")


def setup_jadwal():
    """Daftarkan semua jadwal pengiriman pesan."""
    for jam in JAM_KIRIM:
        waktu = f"{jam:02d}:00"
        schedule.every().day.at(waktu).do(kirim_pesan)
        log.info(f"📅 Jadwal ditambahkan: {waktu}")


def cek_konfigurasi():
    """Validasi token dan chat_id dari environment variable."""
    error = False
    if not BOT_TOKEN:
        print("  ⚠️  BOT_TOKEN belum diset di environment variable!")
        error = True
    if not CHAT_ID:
        print("  ⚠️  CHAT_ID belum diset di environment variable!")
        error = True
    if error:
        print("\n" + "="*55)
        print("  Buat file .env dan isi:")
        print("  BOT_TOKEN=token_kamu")
        print("  CHAT_ID=chat_id_kamu")
        print("="*55 + "\n")
        return False
    return True


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════╗
║     🤖 Bot Telegram - Belajar Miskin  ║
╚═══════════════════════════════════════╝
    """)

    if not cek_konfigurasi():
        exit(1)

    setup_jadwal()

    log.info("🚀 Bot berjalan... Tekan Ctrl+C untuk berhenti.")
    log.info(f"📨 Pesan: '{PESAN}'")
    log.info(f"🕒 Jadwal: jam {', '.join(str(j)+':00' for j in JAM_KIRIM)}")

    while True:
        schedule.run_pending()
        time.sleep(30)   # cek jadwal setiap 30 detik
