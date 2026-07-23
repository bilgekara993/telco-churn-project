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




