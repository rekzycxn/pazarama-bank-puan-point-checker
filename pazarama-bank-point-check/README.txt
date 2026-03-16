# 🏪 Pazaramalternatif Puan Checker

Bu araç **Pazarama.com** üzerinden **MaxiPuan** ve **PazaramaPuan** bilgilerini kontrol eder ve **Discord**'a bildirir.

## 📁 Dosyaların Açıklaması

### 🔑 auth_keys.txt - Token Dosyası
- **Ne işe yarar:** API'ye erişim için gerekli Bearer token'ları içerir
- **Format:** Her satırda bir token (Bearer kelimesi ile birlikte)
- **Önem:** Token süresi dolunca yeni alınmalı

### 💳 cards.txt - Kart Bilgileri Dosyası
- **Ne işe yarar:** Kontrol edilecek kredi kartı bilgilerini içerir
- **Format:** `kart_numarası|ay|yıl|cvv` (pipe işareti ile ayrılmış)
- **Önem:** Yıl 2 haneli olmalı (28 = 2028)

### 🌐 proxy_tokens.txt - Proxy Listesi
- **Ne işe yarar:** Rate limit'i aşmamak için proxy sunucuları kullanır
- **Format:** `ip:port` (her satırda bir proxy)

## 🚀 Nasıl Kullanılır

### 1️⃣ Token Al
- pazarama.com'a gir
- F12 → Network → bank-points request'i bul
- Authorization header'dan token'ı al

### 2️⃣ Çalıştır
```bash
cd pazaramalternatif
python pazaramalternatif_checker.py
```

**Pazaramatatil** ile aynı kartları kullanabilirsin!

## 📁 Dosyaların Açıklaması

### 🔑 auth_keys.txt - Token Dosyası
- **Ne işe yarar:** API'ye erişim için gerekli Bearer token'ları içerir
- **Format:** Her satırda bir token (Bearer kelimesi ile birlikte)
- **Önem:** Token süresi dolunca yeni alınmalı
- **Örnek:**
  ```
  Bearer eyJhbGciOiJSUzUxMiIsImtpZCI6IjM2ODgyMyI...
  ```

### 💳 cards.txt - Kart Bilgileri Dosyası
- **Ne işe yarar:** Kontrol edilecek kredi kartı bilgilerini içerir
- **Format:** `kart_numarası|ay|yıl|cvv` (pipe işareti ile ayrılmış)
- **Önem:** Yıl 2 haneli olmalı (28 = 2028)
- **Örnek:**
  ```
  4743401019480551|11|28|000
  1234567890123456|05|29|123
  ```

### 🌐 proxy_tokens.txt - Proxy Listesi Dosyası
- **Ne işe yarar:** Rate limit'i aşmamak için proxy sunucuları kullanır
- **Format:** `ip:port` (her satırda bir proxy)
- **Önem:** HTTP proxy'ler olmalı, çalışır durumda olmalı
- **Örnek:**
  ```
  104.207.38.51:3129
  209.50.174.135:3129
  ```

## 🚀 Nasıl Kullanılır

### 1️⃣ Token Almak
- **Pazarama.com**'a giriş yap
- **F12 → Network tab**
- **"bank-points"** request'ini bul
- **Authorization header**'ından token'ı kopyala

### 2️⃣ Çalıştırmak
```bash
cd pazaramalternatif
python pazaramalternatif_checker.py
```

## ⚙️ Özellikler

- ✅ **MaxiPuan > 0** ise Discord'a bildirir
- ✅ **HTTP proxy** desteği
- ✅ **Rate limit** koruması
- ✅ **Hata yönetimi** ve yeniden deneme

## 📋 Discord Bildirimi

MaxiPuan 0'dan büyükse Discord'a şu formatta mesaj gönderir:
```
KART BULUNDU!
Kart: 0551
MaxiPuan: 1.588,25
PazaramaPuan: 0,00
Tarih: 2024-01-02 15:30:00
```

## ⚠️ Önemli Uyarılar

- 🔴 **Token geçerli olmalı** (Rate limited = yeni token alın)
- 🔴 **Proxy'ler çalışır durumda olmalı**
- 🔴 **Kart bilgileri doğru girilmeli**

## 📞 Destek

Sorularınız için Discord'da sorun!
