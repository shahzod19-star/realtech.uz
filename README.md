# RealTech Uz — Gadjetlarning Real Vaqtdagi Ishlash va Batareya Tahlili Platformasi

> **"Marketing va'dalari emas — Oddiy insonning real kundalik tajribasi."**

**RealTech Uz** — bu xaridorlarga gadjetlarni (smartfon, aqlli soat, simsiz quloqchin) sotib olishdan oldin:
1. Ularning imkoniyatlarini sodda, tushunarli xalqchil o'zbek tilida o'rganish;
2. Zavodning bo'rttirilgan reklama raqamlarini emas, balki oddiy inson ishlatgandagi **haqiqiy batareya chidamliligini (Screen-on-Time)** ko'rish;
3. Har bir faktni **YouTube video sharhlar (taymkodlari bilan)** hamda yozma konspektlar orqali tekshirib olish imkonini beruvchi zamonaviy interaktiv platforma.

---

## ⚡ Asosiy Imkoniyatlar

1. **Bosh Sahifa va Smart Qidiruv (Hero & Live Filter)**:
   - Jonli qidiruv satri (nomi, protsessor, xususiyatlari bo'yicha darhol topadi).
   - Kategoriya filtrlari: *"Barchasi"*, *"Smartfonlar"*, *"Aqlli soatlar"*, *"Quloqchinlar"*.
   - Tezkor filtr teglari: *1 kundan ko'p yetadiganlar*, *Tez zaryadlanuvchilar (≤32 daq)*, *ANC Shovqin so'ndiruvchilar*.
   - Saralash: Ommabop, batareya hajmi bo'yicha, tez zaryadlash bo'yicha.

2. **Batafsil Gadjet Modali (Deep-Dive Analysis)** 3 ta interaktiv tab bilan:
   - **Tab 1: Qanday ishlaydi va Asosiy funksiyalar**:
     Murakkab texnik terminlarsiz (Cinematic mode, OLED, A15/A17, Sleep Apnea, ANC, Spatial Audio) oddiy tushuntirish, kundalik hayotdagi foydasi, plyus va minuslari.
   - **Tab 2: Real-Time Batareya Testi**:
     Rasmiy va'da vs Oddiy inson natijasi, vizual taqqoslash progress-barlari, har xil ssenariylar (Aralash, YouTube, Og'ir o'yin, Ijtimoiy tarmoqlar, Kamera), zaryadlash tezligi grafigi (0 dan 80% va 0 dan 100%).
   - **Tab 3: YouTube va Yozma Manbalar**:
     Har bir gadjet uchun nufuzli blogerlarning (PhoneBuff, Mrwhosetheboss, MKBHD, RTINGS) video manbalari, aniq taymkodlar (masalan: `06:18`), asosiy faktlar va **videoni ko'rmasdan ham o'qish mumkin bo'lgan yozma konspekt**.

3. **Interaktiv Batareya Simulyatori ("Menga zaryadi qancha yetadi?")**:
   - Har bir qurilma toifasiga mos slayderlar (Telegram/Instagram, YouTube, O'yinlar, Kamera, Always-On, GPS mashg'ulot, ANC, Ovoz balandligi).
   - Real vaqtda kechki soat 23:00 da qancha foiz qolishi, soat nechagacha yetishi va foydali energiya tejash maslahati.

4. **Yonma-yon Solishtirish (Comparison Tool)**:
   - 2-3 ta gadjetni bitta jadvalda yonma-yon qo'yib, real ekran vaqti, rasmiy va'dasi, zaryadlash tezligi va plyus/minuslarini solishtirish.

5. **Apple Uslubidagi Dizayn**:
   - Dark va Light rejimlari (tizimni avtomatik aniqlaydi va eslab qoladi).
   - Glassmorphism, SF Pro / Inter shriftlari, chiroyli silliq animatsiyalar.
   - 100% mobil va desktopga moslashuvchan (Responsive).

---

## 📱 Dastlabki Kiritilgan To'liq Gadjetlar (Seed Data)

- **iPhone 13 (128/256 GB)** — A15 Bionic, Cinematic Mode, Super Retina XDR, IP68. (Rasmiy: 19 soat / Real ekran: 6.5–7.5 soat).
- **Apple Watch Series 10 (45/46 mm)** — Keng burchakli OLED, Sleep Apnea, 0 dan 80% gacha 30 daqiqada tez zaryad. (Rasmiy: 18 soat / Real: 22–26 soat).
- **AirPods Pro (2-avlod / USB-C)** — Faol shovqinni kesish (ANC), Adaptive Audio, Spatial Audio. (Rasmiy: 6 soat / Real ANC bilan: 5.2–5.5 soat).
- **AirPods 3** — Ochiq qulay dizayn, Adaptiv ekvayzer. (Rasmiy: 6 soat / Real: 5.8–6.2 soat).
- **iPhone 15 Pro** — Titan korpus, 120Hz ProMotion, A17 Pro, USB-C 3.0. (Rasmiy: 23 soat / Real: 6.8–7.8 soat).
- **Samsung Galaxy S24 Ultra** — 5000 mAh batareya, Gorilla Armor aks ettirmaydigan ekran, S-Pen. (Rasmiy: 30 soat / Real: 8.5–9.5 soat).

---

## 🚀 Ishga Tushirish Qo'llanmasi

### 1-usul: Bir marta bosish orqali (Windows uchun eng osoni):
Papka ichidagi `start.bat` fayliga sichqoncha bilan ikki marta bosing. U serverni ishga tushirib, brauzerda avtomatik ravishda ochib beradi!

### 2-usul: Python orqali:
```bash
cd "C:\Users\Acer\.gemini\antigravity\scratch\realtech-uz"
py server.py
```
So'ng brauzerda oching: **http://localhost:3000**

### 3-usul: To'g'ridan-to'g'ri brauzerda ochish:
Papka ichidagi `index.html` faylini istalgan brauzerda (Chrome, Edge, Opera GX) oching.

---

## 📂 Loyiha Tuzilmasi

```
realtech-uz/
│
├── index.html             # Asosiy veb-sahifa (Barcha bo'limlar, modal va tray)
├── server.py              # Mahalliy web-server skripti (Python 3)
├── start.bat              # Bir marta bosish bilan ishga tushiruvchi Windows fayli
├── README.md              # Ushbu hujjat
│
├── css/
│   └── styles.css         # Apple-style maxsus vizual uslublar va slayder animatsiyalari
│
└── js/
    ├── data.js            # Gadjetlarning boyitilgan bazasi (JSON sxemasi asosida)
    ├── calculator.js      # Dinamik batareya simulyatori algoritmi
    ├── comparison.js      # Yonma-yon taqqoslash boshqaruvchisi
    └── app.js             # Asosiy reaktiv ilova mantiqi va hodisalar
```

---

## 🔧 Yangi Gadjet Qo'shish

Yangi gadjet qo'shish uchun `js/data.js` faylini ochib, `GADGETS_DATA` massiviga yangi obyekt qo'shish kifoya:

```javascript
{
  id: "gadget-id",
  name: "Gadjet Nomi",
  category: "Smartfonlar" // yoki "Aqlli soatlar", "Quloqchinlar"
  battery: {
    officialClaimHours: 20,
    realWorldActiveHours: 7.5,
    chargingZeroToEightyMins: 30,
    chargingZeroToFullMins: 75,
    scenarios: { ... }
  },
  howItWorks: [ ... ],
  sources: [ ... ]
}
```
Platforma yangi qo'shilgan gadjetni avtomatik ravishda qidiruv, katalog, kalkulyator va taqqoslash bo'limlariga kiritadi.
