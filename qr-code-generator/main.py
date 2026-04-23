import qrcode

print("=== QR Code Generator ===")

data = input("Enter text or link to convert into QR code: ")

filename = input("Enter filename (example: myqr.png): ")

qr = qrcode.make(data)
qr.save(filename)

print(f"\n✅ QR Code saved successfully as: {filename}")
