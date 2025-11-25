# 🚨 HasWave Deprem

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**KOERI'den deprem verilerini çekerek Home Assistant'a sensor olarak ekler**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=HasWave&repository=HACS-Deprem&category=Integration" target="_blank">
  <img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.">
</a>

</div>

---

## 📋 Özellikler

* 🌍 **KOERI Entegrasyonu** - HasWave API üzerinden KOERI deprem verilerini çeker
* ✅ **Config Flow** - Kolay kurulum ve yapılandırma
* 📊 **İstatistikler** - Maksimum, ortalama büyüklük ve deprem sayısı
* 🎯 **Filtreleme** - İl, bölge ve büyüklük bazlı filtreleme
* ⚡ **Yüksek Performans** - Optimize edilmiş API çağrıları
* 🔄 **Otomatik Güncelleme** - Belirli aralıklarla otomatik veri güncelleme
* 📊 **Statistics** - Home Assistant statistics sayfasında görünür

## 🚀 Hızlı Başlangıç

### 1️⃣ HACS ile Kurulum

1. Home Assistant → **HACS** → **Integrations**
2. Sağ üstteki **⋮** menüsünden **Custom repositories** seçin
3. Repository URL: `https://github.com/HasWave/HACS-Deprem`
4. Category: **Integration** seçin
5. **Add** butonuna tıklayın
6. HACS → Integrations → **HasWave Deprem**'i bulun
7. **Download** butonuna tıklayın
8. Home Assistant'ı yeniden başlatın

### 2️⃣ Manuel Kurulum

1. Bu repository'yi klonlayın veya indirin
2. `custom_components/haswave_deprem` klasörünü Home Assistant'ın `config/custom_components/` klasörüne kopyalayın
3. Home Assistant'ı yeniden başlatın

### 3️⃣ Integration Ekleme

1. Home Assistant → **Settings** → **Devices & Services**
2. Sağ alttaki **+ ADD INTEGRATION** butonuna tıklayın
3. **HasWave Deprem** arayın ve seçin
4. Yapılandırma formunu doldurun:
   - **API URL**: Varsayılan: `https://api.haswave.com/api/v1/deprem`
   - **Güncelleme Aralığı**: Saniye cinsinden (varsayılan: 300 = 5 dakika)
   - **Minimum Büyüklük**: Filtreleme için minimum büyüklük (varsayılan: 0.0)
   - **İl Filtresi**: Opsiyonel, belirli bir il için filtreleme
   - **Bölge Filtresi**: Opsiyonel, belirli bir bölge için filtreleme
5. **Submit** butonuna tıklayın

**✅ Sensor'lar Otomatik Oluşturulur:** Integration eklendiğinde sensor'lar direkt Home Assistant'a eklenir. Hiçbir ek kurulum gerekmez!

## 📖 Kullanım

### Home Assistant Sensor'ları

Integration otomatik olarak şu sensor'ları oluşturur:

#### `sensor.deprem_magnitude`
Son deprem büyüklüğü (statistics için)

#### `sensor.deprem_location`
Son deprem lokasyonu

#### `sensor.deprem_date`
Son deprem tarihi

#### `sensor.deprem_depth`
Son deprem derinliği (km birimi entity'de tanımlı)

#### `sensor.deprem_latest`
Son deprem (tüm bilgiler attributes içinde)

#### `sensor.deprem_max_magnitude`
Maksimum deprem büyüklüğü (statistics için)

#### `sensor.deprem_avg_magnitude`
Ortalama deprem büyüklüğü (statistics için)

#### `sensor.deprem_count`
Toplam deprem sayısı

#### `sensor.deprem_list`
Son 10 deprem listesi (JSON attributes içinde)

### Dashboard Kartı

Lovelace UI'da kart ekleyin:

**Not:** `unit_of_measurement` kartta değil, entity'de tanımlıdır. Dashboard'da sadece entity ID, name ve icon kullanın.

```yaml
type: entities
title: Deprem Bilgileri
entities:
  - entity: sensor.deprem_latest
    name: Son Deprem
    icon: mdi:earthquake
  - entity: sensor.deprem_magnitude
    name: Büyüklük
    icon: mdi:gauge
  - entity: sensor.deprem_location
    name: Lokasyon
    icon: mdi:map-marker
  - entity: sensor.deprem_date
    name: Tarih
    icon: mdi:calendar-clock
  - entity: sensor.deprem_depth
    name: Derinlik
    icon: mdi:arrow-down
```

### Otomasyon Örneği

Belirli büyüklükte deprem olduğunda bildirim gönderme:

```yaml
automation:
  - alias: "Deprem Uyarısı - 4.0+"
    trigger:
      platform: numeric_state
      entity_id: sensor.deprem_magnitude
      above: 4.0
    action:
      - service: notify.mobile_app
        data:
          title: "🚨 Deprem Uyarısı!"
          message: >
            {{ states('sensor.deprem_location') }} yakınlarında
            {{ states('sensor.deprem_magnitude') }} büyüklüğünde deprem!
          data:
            priority: high
            sound: default
      
      - service: light.turn_on
        entity_id: light.living_room
        data:
          brightness: 255
          rgb_color: [255, 0, 0]  # Kırmızı
      
      - delay: "00:00:10"
      
      - service: light.turn_off
        entity_id: light.living_room
```

## 🔧 Gelişmiş Kullanım

### İl/Bölge Filtreleme

Sadece belirli bir il veya bölgedeki depremleri takip etmek için integration ayarlarından filtreleme yapabilirsiniz.

**Bölgeler:**
- `MARMARA`
- `EGE`
- `AKDENİZ`
- `İÇ ANADOLU`
- `KARADENİZ`
- `DOĞU ANADOLU`
- `GÜNEYDOĞU ANADOLU`

### Performans Optimizasyonu

* **Güncelleme Aralığı** değerini artırarak API çağrı sayısını azaltabilirsiniz
* **Minimum Büyüklük** değerini ayarlayarak sadece önemli depremleri takip edebilirsiniz
* **İl** veya **Bölge** filtresi kullanarak gereksiz veri işlemeyi önleyebilirsiniz

### Sorun Giderme

#### Sensor'lar Görünmüyor

* Integration'ın eklendiğini kontrol edin: **Settings** → **Devices & Services**
* Home Assistant'ı yeniden başlatın
* Sensor'ları **Settings** → **Devices & Services** → **Entities** bölümünden kontrol edin
* Logları kontrol edin: **Settings** → **System** → **Logs**

#### API Hatası

* İnternet bağlantınızı kontrol edin
* API URL ayarının doğru olduğundan emin olun
* Logları kontrol edin

#### Integration Ekleme Hatası

* HACS üzerinden doğru şekilde yüklendiğinden emin olun
* Home Assistant'ı yeniden başlatın
* `custom_components` klasörünün doğru konumda olduğundan emin olun

## 📁 Dosya Yapısı

```
HACS-Deprem/
├── custom_components/
│   └── haswave_deprem/
│       ├── __init__.py
│       ├── manifest.json
│       ├── const.py
│       ├── api.py
│       ├── sensor.py
│       └── config_flow.py
├── hacs.json
└── README.md
```

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**HasWave**

🌐 [HasWave](https://haswave.com) | 📱 [Telegram](https://t.me/HasWave) | 📦 [GitHub](https://github.com/HasWave)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

Made with ❤️ by HasWave
