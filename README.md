# Duygu-Analizi-Web-Uygulamas-
🤖 Kullanılan Yapay Zeka Modülü
🎯 Proje Amacı
Bu projede kullanıcıdan alınan metinlere göre duygusal durumun (mutlu, üzgün, öfkeli, vb.) analizini yapan bir web tabanlı uygulama geliştirilmiştir. Proje, metin üzerinden çok sınıflı duygu analizi yaparak kullanıcılara yazdıkları ifadelerin hangi duyguyu taşıdığını anlık olarak göstermektedir.


Model: Fine-tuned bir LLM (örneğin DistilBERT) kullanılmıştır.

Veri Seti: GoEmotions veri seti kullanılarak model eğitilmiştir.

Çıktı: Kullanıcının girdiği metin 27 farklı duygu kategorisinden biri veya birkaçıyla eşleştirilir.

Model sadece tahmin (inference) yapar.

💻 Web Uygulaması Özellikleri
Kullanıcı arayüzü: Basit ve kullanıcı dostu bir form (text input)

Girdi: Kullanıcı metni

Çıktı: Modelin tahmini ettiği duygu(lar), görsel olarak gösterilir

Geliştirme teknolojileri: Örneğin Flask (backend) + HTML/CSS (frontend) kullanılmıştır

