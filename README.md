# Telco Customer Churn Prediction

## Projenin amacı

Bu projede bir telekom şirketinin müşteri verilerini kullanarak,
aboneliğini iptal etme ihtimali bulunan müşterilerin önceden tahmin
edilmesi amaçlanmaktadır.

Model, müşterinin abonelik süresi,
kullandığı hizmetler, sözleşme türü, ödeme yöntemi ve fatura bilgileri
gibi özelliklerden yararlanarak müşterinin churn olasılığını tahmin
edecektir.

## Neden önemli?

Mevcut bir müşteriyi elde tutmak, yeni bir müşteri kazanmaktan daha az maliyetli olabilir. Bu nedenle ayrılma ihtimali yüksek müşterilerin önceden tespit edilmesi şirket açısından önemlidir. Şirket bu müşterilere özel kampanyalar, indirimler veya farklı teklifler sunarak aboneliklerini devam ettirmelerini sağlayabilir. Bu da müşteri kaybının ve buna bağlı oluşan zararın azaltılmasına yardımcı olur.

## Data Leakage

Veri ön işleme sırasında kullanılan bazı işlemler veri setinden bilgi öğrenir. 

Bu bilgilerin bütün veri seti üzerinden hesaplanması durumunda test verisine ait bilgiler de eğitime dahil edilmiş olur. Model test verisini doğrudan görmese bile test verisinin dağılımı hakkında dolaylı olarak bilgi edinir. Bu durum data leakage olarak bilinir ve model performansının gerçekte olduğundan daha yüksek görünmesine neden olabilir.

Bu nedenle pipeline yalnızca tarin verisi üzerinde fit_transform() ile çalıştırıldı. Test verisine ise train verisinden öğrenilen medyan, ölçeklendirme değerleri ve kategori bilgileri transform() ile uygulandı. Böylece test verisi modelin son performansını tarafsız şekilde değerlendirmek için ayrı tutulmuştur.

## Birinci Hafta Özeti

Bu hafta veri setindeki değişkenleri inceleyerek başladım. Keşifçi veri analizi sırasında hedef değişkenin dengeli dağılmadığını, TotalCharges kolonunun metin olarak geldiğini ve bazı yeni müşterilerde boş değer içerdiğini fark ettim. Sayısal ve kategorik değişkenlerin dağılımlarını inceleyerek churn ile ilişkili görünen müşteri özelliklerini değerlendirdim.

Veri ön işleme aşamasında veriyi churn oranlarını koruyacak şekilde train ve test bölümlerine ayırdım. Eksik değer doldurma, sayısal ölçeklendirme ve one-hot encoding işlemlerini Pipeline ve ColumnTransformer kullanarak birleştirdim. Fit işlemlerini yalnızca train verisinde gerçekleştirerek data leakage oluşmamasını sağladım.

İlk baseline model olarak Logistic Regression kullandım ve modeli 5-fold stratified cross-validation ile değerlendirdim. Accuracy’nin dengesiz hedef değişkenlerde tek başına yanıltıcı olabileceğini; precision, recall, F1, ROC-AUC ve PR-AUC metriklerinin model performansının farklı yönlerini gösterdiğini öğrendim.

En çok zorlandığım konular cross-validation ve pipeline oluşturma sırası.

Son olarak baseline sonuçlarında modelin churn eden müşterilerin önemli bir bölümünü kaçırdığı görüldü.

## Projenin Genel Akışı

Proje, ham müşteri verisinden çalışan bir tahmin servisine kadar aşağıdaki adımlarla geliştirilmiştir:

1. Veri seti incelendi, hedef değişkenin dağılımı ve değişkenlerin churn ile ilişkisi analiz edildi.
2. `TotalCharges` değişkenindeki veri tipi ve eksik değer sorunları giderildi.
3. Sayısal değişkenlere eksik değer doldurma ve ölçeklendirme, kategorik değişkenlere ise one-hot encoding uygulandı.
4. Ön işleme adımları ve modeller tek bir scikit-learn Pipeline yapısında birleştirildi. Böylece eğitim ve tahmin sırasında aynı işlemlerin uygulanması sağlandı.
5. Logistic Regression, XGBoost, Random Forest, SVM-RBF ve KNN modelleri stratified cross-validation ile karşılaştırıldı.
6. Logistic Regression ve XGBoost için hiperparametre optimizasyonu yapıldı.
7. Nihai model yalnızca sınıflandırma metriklerine göre değil, müşteri kaybının ve müşteriye kampanya sunmanın tahmini iş maliyetlerine göre de değerlendirildi.
8. Modelin karar eşiği optimize edildi, SHAP ile model açıklanabilirliği incelendi ve sonuç bir FastAPI servisi olarak kullanıma hazırlandı.

Analiz ve geliştirme adımlarının ayrıntıları `notebooks/` klasöründeki numaralandırılmış notebook dosyalarında bulunmaktadır.

## Projenin Başarısı ve Nihai Sonuçlar

Model seçiminde amaç yalnızca accuracy değerini yükseltmek değildir. Churn problemi dengesiz bir sınıflandırma problemi olduğu için ROC-AUC, PR-AUC, precision, recall ve F1 metrikleri birlikte değerlendirilmiştir. İş açısından churn edecek bir müşteriyi kaçırmanın maliyeti, gereksiz bir kampanya sunmanın maliyetinden daha yüksek kabul edilmiştir.

Nihai model olarak optimize edilmiş XGBoost modeli seçilmiş ve karar eşiği `0.07` olarak belirlenmiştir. Ayrı tutulan test setindeki sonuçlar şöyledir:

| Eşik | Precision | Recall | F1 | Toplam tahmini maliyet |
| --- | ---: | ---: | ---: | ---: |
| 0.50 | %67,34 | %53,48 | %59,61 | 101.850 |
| 0.07 | %37,29 | %96,52 | %53,80 | 54.900 |

Optimize edilmiş eşik sayesinde model, churn eden müşterilerin yaklaşık `%96,5`'ini tespit etmektedir. Standart `0.50` eşiğine kıyasla kaçırılan churn müşterisi sayısı 174'ten 13'e, varsayımsal toplam iş maliyeti ise 101.850'den 54.900'e düşmüştür. Bu, tanımlanan maliyet varsayımları altında yaklaşık `%46,1` tasarruf anlamına gelir.

Recall artarken precision değerinin düşmesi beklenen bir sonuçtur: model daha fazla riskli müşteriyi yakalamak için daha geniş bir müşteri grubunu kampanya adayı olarak işaretlemektedir. Bu nedenle sonuçlar, kampanya maliyeti `50` ve kaybedilen müşteri maliyeti `500` varsayımlarına bağlıdır; gerçek kullanımda bu değerler şirketin güncel maliyetleriyle yeniden belirlenmelidir.

## Kullanılan Teknolojiler

- Python
- pandas ve NumPy
- scikit-learn
- XGBoost
- SHAP
- Matplotlib ve Seaborn
- FastAPI ve Uvicorn
- Jupyter Notebook
- joblib

## Proje Yapısı

```text
telco-churn-project/
├── data/          # Ham veri seti
├── models/        # Eğitilmiş modeller ve karar eşiği ayarları
├── notebooks/     # EDA, ön işleme, modelleme ve değerlendirme çalışmaları
├── reports/       # Metrikler, karşılaştırma tabloları ve grafikler
├── scripts/       # Yardımcı proje scriptleri
├── src/           # FastAPI tahmin servisi
├── tests/         # API istek testleri
├── requirements.txt
└── README.md
```

## Kurulum

Öncelikle projeyi bilgisayarınıza indirin ve proje klasörüne geçin. Ardından sanal ortam oluşturup bağımlılıkları yükleyin.

Windows PowerShell için:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS veya Linux için:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Veri dosyasının `data/telco_customer_churn.csv`, eğitilmiş nihai modelin `models/final_churn_pipeline.joblib` ve eşik ayarlarının `models/threshold_config.json` konumunda bulunduğundan emin olun.

## API'yi Çalıştırma

Proje ana dizinindeyken aşağıdaki komutu çalıştırın:

```bash
python -m uvicorn src.api:app --reload
```

Servis varsayılan olarak `http://127.0.0.1:8000` adresinde açılır. Tarayıcıdan `http://127.0.0.1:8000/docs` adresine giderek Swagger arayüzü üzerinden `/predict` endpoint'ini deneyebilirsiniz.

Örnek istek:

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 12,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "No",
  "DeviceProtection": "Yes",
  "TechSupport": "No",
  "StreamingTV": "Yes",
  "StreamingMovies": "Yes",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 89.5,
  "TotalCharges": 1074.0
}
```

API; churn olasılığını, `0` veya `1` tahminini, okunabilir sınıf etiketini ve kullanılan karar eşiğini döndürür.

## Notebook'ları Çalıştırma

Analizleri yeniden incelemek veya çalıştırmak için sanal ortam aktifken aşağıdaki komutu kullanabilirsiniz:

```bash
jupyter lab
```

Notebook'lar işlem sırasını gösterecek şekilde `01` ile `08` arasında numaralandırılmıştır. Sonuçların yeniden üretilebilmesi için bu dosyaların numara sırasıyla çalıştırılması önerilir.

## Raporlar ve Görseller

Model karşılaştırmaları, eşik analizleri ve nihai test sonuçları `reports/` klasöründe CSV olarak; confusion matrix, model karşılaştırması, maliyet-eşik ilişkisi ve SHAP önem grafikleri ise `reports/figures/` klasöründe yer almaktadır.




