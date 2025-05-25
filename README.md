## 1. Update sistem
```
pkg update && pkg upgrade -y
```

## 2. Install Python
```
pkg install python -y
```

## Untuk Termux
 3. Install dependency native untuk Pillow
```
pkg install clang libjpeg-turbo libjpeg-turbo-static freetype freetype-static libpng libpng-static -y
```

 4. Set environment agar build library sukses
```
export LDFLAGS="-L/data/data/com.termux/files/usr/lib"
export CFLAGS="-I/data/data/com.termux/files/usr/include"
```

## 5. Install dependensi Python
```
pip install qrcode[pil]
```

## 6. Install Git
```
pkg install git -y
```

## 7. Clone repo ini
```
git clone https://github.com/topibajaa/qriskonverter.git
cd qriskonverter
```

## 8. Jalankan script
```
python qris.py
```
