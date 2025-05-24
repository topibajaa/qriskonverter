import qrcode

def crc16_ccitt(data: str):
    crc = 0xFFFF
    for c in bytearray(data.encode()):
        crc ^= c << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return format(crc, '04X')

# Input base QRIS
base_qris = input("Masukkan string QRIS statis (tanpa nominal & CRC): ").strip()

# Input nominal
try:
    nominal = int(input("Masukkan nominal utama (tanpa titik/koma): "))
    if nominal <= 0:
        raise ValueError("Nominal harus lebih dari 0.")
except ValueError as e:
    print("Input tidak valid:", e)
    exit()

# Tanya apakah ada biaya layanan
pakai_biaya = input("Tambahkan biaya layanan? (y/n): ").lower()
biaya_tambahan = 0

if pakai_biaya == "y":
    jenis = input("Biaya dalam persen (%) atau rupiah (r)? ").lower()
    if jenis == "%":
        try:
            persen = float(input("Masukkan persen biaya layanan (misal 2.5): "))
            biaya_tambahan = round(nominal * (persen / 100))
        except ValueError:
            print("Input persen tidak valid.")
            exit()
    elif jenis == "r":
        try:
            biaya_tambahan = int(input("Masukkan biaya tetap dalam rupiah: "))
        except ValueError:
            print("Input rupiah tidak valid.")
            exit()
    else:
        print("Jenis biaya tidak valid.")
        exit()

total_nominal = nominal + biaya_tambahan
nominal_str = f"{total_nominal:06d}"
nominal_tag = f"5406{nominal_str}"

# Sisipkan tag 54 (nominal) sebelum tag 58
pos_58 = base_qris.find("5802")
if pos_58 == -1:
    print("Format base QRIS tidak valid (tidak ditemukan tag 5802).")
    exit()

raw_data = base_qris[:pos_58] + nominal_tag + base_qris[pos_58:]
raw_data_no_crc = raw_data + "6304"
crc = crc16_ccitt(raw_data_no_crc)
final_qris = raw_data_no_crc + crc

print("\nQRIS Final (dengan nominal & CRC):")
print(final_qris)

# Simpan gambar
filename = input("Masukkan nama file gambar (tanpa .png): ").strip() + ".png"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(final_qris)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(filename)

print(f"QRIS berhasil dibuat dan disimpan sebagai {filename}")
