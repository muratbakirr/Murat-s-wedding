# Beyza & Murat — Dijital Düğün Davetiyesi

Tek sayfalık, statik bir düğün davetiyesi sitesi. Derleme adımı yok — sadece
`index.html` ve `assets/`. Telefonda açılmak üzere tasarlandı (davetliler linki
WhatsApp'tan açacak).

**Düğün:** 12 Eylül 2026, Cumartesi · 19:00
**Mekân:** Düş Bahçesi Kır Düğünü — İncek Mah., Turgut Özal Bulvarı, Dural Sok. No:11, 06830 Gölbaşı / Ankara

---

## Yerelde çalıştırma

```bash
cd "Murat's Wedding"
python3 -m http.server 8000
```

Sonra tarayıcıda **http://localhost:8000** adresini aç.

> `index.html` dosyasına çift tıklayarak (`file://`) açma — müzik ve Google
> Fonts o şekilde düzgün çalışmaz. Mutlaka yukarıdaki sunucuyu kullan.

---

## Vercel'e yayınlama

> ⚠️ **Dikkat:** Bu klasör başta ev dizinindeki (`/Users/muratbakir`) git deposunun
> içindeydi. O depoya push atsaydın `.ssh/`, `.aws/`, `.netrc` gibi gizli dosyaların
> da GitHub'a gidebilirdi. Bu yüzden bu klasöre kendi bağımsız git deposu kuruldu
> (`main` dalı). Aşağıdaki komutları **bu klasörün içinden** çalıştır.

```bash
git add .
git commit -m "Düğün davetiyesi sitesi"

# GitHub'da boş bir repo aç, sonra:
git remote add origin git@github.com:<kullanici-adin>/<repo-adi>.git
git push -u origin main
```

Ardından [vercel.com/new](https://vercel.com/new) → GitHub reposunu **Import** et.
Statik site olduğu için hiçbir ayar gerekmiyor:

| Ayar | Değer |
|---|---|
| Framework Preset | **Other** |
| Build Command | *(boş bırak)* |
| Output Directory | *(boş bırak)* |

**Deploy**'a bas. Link hazır.

### Yayından sonra tek yapman gereken

`index.html` içindeki iki `og:image` / önizleme adresini kendi alan adınla
değiştir — WhatsApp önizlemesi için **tam adres** gerekiyor:

```html
<meta property="og:image" content="https://SENIN-ADRESIN.vercel.app/assets/og.png">
```

Böylece linki WhatsApp'ta paylaştığında altında davetiye görseli çıkar.

---

## İçeriği değiştirme

Her şey `index.html` içinde, düz metin olarak duruyor:

| Ne | Nerede |
|---|---|
| İsimler | `<h1 class="names">` |
| Tarih (EYLÜL / CMT / 12 / 2026) | `<div class="date">` |
| Saat | `<p class="time">` |
| Mekân ve adres | `<p class="venue">` ve `<p class="address">` |
| Yol tarifi linki | `<a class="maps" href="...">` |
| Kapanış cümlesi | `<p class="closing">` |
| Renkler | CSS'in en üstündeki `:root` bloğu |

**Önemli:** Büyük harfli metinleri doğrudan büyük harfle yaz. CSS'in
`text-transform: uppercase` özelliği Türkçe'de `i` harfini `I` yapar (`İ`
değil), bu yüzden sayfada bilerek kullanılmadı.

### Müzik nasıl çalışıyor (önemli)

**Hiçbir tarayıcı, sayfa açılır açılmaz sesli müzik başlatmaz.** iOS Safari,
Android Chrome ve WhatsApp'ın kendi içindeki tarayıcı bunu kesin olarak
engelliyor — bu bir kod eksiği değil, tarayıcı kuralı. Müziğin başlaması için
kullanıcının **gerçek bir dokunuşu** şart.

Çözüm: davetiye bir **açılış ekranının** arkasında duruyor. Davetli linke
tıklayınca önce isimlerin olduğu bir kapak görüyor ve **"DAVETİYEYİ AÇ"**
butonuna basıyor. İşte o dokunuş, tarayıcının istediği izin oluyor — müzik
başlıyor ve davetiye açılıyor.

Yani pratikte: davetiyeyi açan herkes müziği duyar. Butona basmadan içeriği
göremediği için "dokunmayı atlama" ihtimali yok.

- Sağ alttaki 🔊 butonu müziği sonradan kapatıp açmaya yarıyor.
- `preload="auto"` — dokunuş geleceği kesin olduğu için parça önceden yükleniyor,
  butona basıldığı anda gecikmesiz başlıyor.
- JavaScript kapalıysa açılış ekranı gizleniyor (`<noscript>`), davetiye yine açılıyor.

### Ses seviyesi ve iPhone

Ses seviyesi **mp3 dosyasının içine gömüldü** (-5 dB), JavaScript ile
ayarlanmıyor. Sebebi: iOS'ta `audio.volume` salt-okunur — atama sessizce
görmezden geliniyor. Eskiden JS ile 0.55'e çekiliyordu; bu masaüstünde çalışıp
iPhone'da çalışmıyordu, yani iPhone'da müzik sonuna kadar açık başlıyordu.

Yeni parça koyarken aynı işlemi uygula:

```bash
ffmpeg -i yeni-parca.mp3 -map 0:a -af "volume=-5dB" \
       -c:a libmp3lame -b:a 96k -ar 44100 assets/music.mp3
```

96 kbps mobil veri için yeterli — şu anki dosya 2.0 MB.

### Yazı boyutlarını değiştirme

Bütün yazı boyutları `index.html` içindeki `:root` bloğunda, tek yerde toplandı.
CSS'in derinlerini kurcalamana gerek yok — sadece bu satırları düzenle:

```css
--fs-names:   clamp(4.7rem, 20vw, 7.5rem);   /* Beyza / Murat */
--fs-invite:  clamp(.74rem, 3.1vw, .9rem);   /* DÜĞÜN TÖRENİMİZDE... */
--fs-num:     clamp(2.9rem, 12vw, 3.9rem);   /* 12 */
--fs-venue:   clamp(1.02rem, 4.6vw, 1.4rem); /* DÜŞ BAHÇESİ */
--fs-closing: clamp(1.45rem, 5.8vw, 1.95rem);/* kapanış cümlesi */
...
```

`clamp(en_küçük, ekrana_göre, en_büyük)` üç değer alır:

| Değer | Anlamı |
|---|---|
| 1. | Telefonda inebileceği **en küçük** boyut |
| 2. | Ekran genişliğine göre esneyen değer (`vw` = ekran genişliğinin %'si) |
| 3. | Masaüstünde çıkabileceği **en büyük** boyut |

Yani isimleri büyütmek için `--fs-names` satırındaki **1. ve 3.** değerleri artır.
Üçünü birden büyütürsen telefonda taşabilir — büyüttükten sonra tarayıcı
penceresini daraltıp kontrol et.

> Kavisli üstteki "AİLELERİMİZİN MUTLULUĞUYLA" bir SVG içinde olduğu için ayrı:
> `.arch text { font-size: 16px }`. O SVG ile birlikte ölçekleniyor.

### Çiçekler

Köşelerdeki suluboya çiçekler **OpenAI `gpt-image-2`** ile üretildi, beyaz zemin
üzerine. Sayfada `mix-blend-mode: multiply` ile bindiriliyor — beyaz zemin
çarpma modunda etkisiz olduğu için çiçekler hem kartın üzerine hem de fildişi
çerçevenin üstüne temiz biniyor. Şeffaf PNG'ye gerek kalmıyor.

**Tek bir görsel iki köşede de kullanılıyor:** `assets/floral-corner.*`. Sağ üst
köşedeki, aynı görselin `transform: rotate(180deg)` ile 180° döndürülmüş hâli.
Böylece iki köşe çapraz simetrik duruyor ve tek dosya iniyor.

| Dosya | Boyut | Ne zaman kullanılır |
|---|---|---|
| `floral-corner.webp` | ~61 KB | Tüm modern tarayıcılar (fiilen herkes) |
| `floral-corner.png` | ~660 KB | Çok eski tarayıcılar için yedek |

`<picture>` etiketi seçimi kendi yapıyor; modern tarayıcı PNG'yi hiç indirmiyor.

Yeni görsel üretirsen aynı işlemi uygula (ImageMagick yok, ffmpeg var):

```bash
ffmpeg -y -i yeni.png -vf scale=760:-1 -c:v libwebp -quality 86 assets/floral-top.webp
ffmpeg -y -i yeni.png -vf scale=760:-1 assets/floral-top.png
```

**Alternatif:** `tools/make_florals.py` elle kodlanmış, prosedürel bir SVG çiçek
seti üretir (yaprakları bezier saplar boyunca dizer). AI görselleri beğenmezsen
yedek olarak duruyor:

```bash
python3 tools/make_florals.py assets   # floral-top.svg + floral-bottom.svg
```

Bu durumda `index.html`'deki `<picture>` bloklarını tek bir
`<img src="assets/floral-top.svg">` ile değiştir ve `mix-blend-mode` satırını sil.

---

## Notlar

- **Müzik** açılış ekranındaki butona basılınca başlıyor; sağ alttaki 🔊 ile
  kapatılıp açılabiliyor. Sesi 2 saniyede yumuşakça yükseliyor (iOS bu geçişi
  desteklemiyor, orada direkt başlıyor — sorun değil, seviye dosyada ayarlı).
- **Yol tarifi** butonu telefonda doğrudan Google Maps uygulamasını açar.
- Sayfa toplam ~2.2 MB indiriyor (2.0 MB müzik + 61 KB çiçek). PNG yedekleri
  depoda duruyor ama modern tarayıcı indirmiyor.
- Yazı tipleri Google Fonts: **Italianno** (isimler), **Cinzel** (büyük harfli
  satırlar), **Cormorant Garamond** (adres ve rakamlar). Cinzel küçük harfleri
  small-caps'e çevirdiği için adreste bilerek kullanılmadı.
