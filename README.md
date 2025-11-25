# 🚨 HasWave Deprem

KOERI'den deprem verilerini çekerek Home Assistant'a sensor olarak ekler.

## 📋 Özellikler

* 🚨 **Deprem Verileri** - Son depremler ve istatistikler
* 📊 **İstatistikler** - Maksimum, ortalama büyüklük ve deprem sayısı
* 🔄 **Otomatik Güncelleme** - Belirli aralıklarla otomatik veri güncelleme
* 🏙️ **Filtreleme** - İl ve bölge bazlı filtreleme

## 🚀 Kurulum

### HACS ile Kurulum

1. HACS → Integrations → Custom repositories
2. Repository URL: `https://github.com/HasWave/Home-Assistant-Deprem`
3. Category: Integration
4. Add butonuna tıklayın
5. HACS → Integrations → HasWave Deprem'i bulun ve yükleyin

### Manuel Kurulum

1. Bu repository'yi klonlayın veya indirin
2. `custom_components` klasörünü Home Assistant'ın `config` klasörüne kopyalayın
3. Home Assistant'ı yeniden başlatın
4. Settings → Devices & Services → Add Integration
5. "HasWave Deprem" arayın ve ekleyin

## ⚙️ Yapılandırma

Integration eklerken şu bilgileri girebilirsiniz:

- **API URL**: Varsayılan: `https://api.haswave.com/api/v1/deprem`
- **Güncelleme Aralığı**: Saniye cinsinden (varsayılan: 300)
- **Minimum Büyüklük**: Filtreleme için minimum büyüklük (varsayılan: 0.0)
- **İl Filtresi**: Opsiyonel, belirli bir il için filtreleme
- **Bölge Filtresi**: Opsiyonel, belirli bir bölge için filtreleme

## 📊 Sensor'lar

Entegrasyon aşağıdaki sensor'ları oluşturur:

- `sensor.deprem_latest` - Son deprem bilgisi
- `sensor.deprem_magnitude` - Son deprem büyüklüğü
- `sensor.deprem_max_magnitude` - Maksimum büyüklük
- `sensor.deprem_avg_magnitude` - Ortalama büyüklük
- `sensor.deprem_count` - Deprem sayısı

## 📖 Daha Fazla Bilgi

Detaylı dokümantasyon için: [GitHub Repository](https://github.com/HasWave/Home-Assistant-Deprem)

## 👨‍💻 Geliştirici

**HasWave**

🌐 [HasWave](https://haswave.com) | 📱 [Telegram](https://t.me/HasWave) | 📦 [GitHub](https://github.com/HasWave)

