# S-r-c-s-z-Metro-Sim-lasyonu-Rota-Optimizasyonu-
Bu projede, ankara metro ağında; İki istasyon arasındaki en hızlı, En az aktarmalı rotayı bulan bir simülasyon deneyimleyeceksiniz.

## Özellikler

- Metro hatlarının düğüm-temelli veri yapısıyla modellenmesi
- En az aktarma yapılan rotanın **BFS (Breadth-First Search)** ile bulunması
- En kısa sürede gidilen rotanın **A* (Dijkstra benzeri)** algoritmasıyla bulunması
- Rota sürelerinin hesaplanması
- Kullanıcının başlangıç ve hedef istasyon seçimiyle dinamik sorgulama
- **NetworkX** ve **Matplotlib** ile metro ağının görselleştirilmesi

## Dosya İçeriği

- `Istasyon` sınıfı: Her bir metro istasyonunu temsil eder
- `MetroAgi` sınıfı: Metro ağı yapısını ve algoritmaları barındırır
- Algoritmalar:
  - `en_az_aktarma_bul`: BFS algoritması
  - `en_hizli_rota_bul`: A* (Dijkstra)
  - `compute_route_duration`: Toplam rota süresi
- Görselleştirme: `visualize_graph` fonksiyonu ile metro ağı diyagramı


## Nasıl Çalıştırılır?
1. Gerekli kütüphaneleri yükleyin:
pip install networkx matplotlib

2. Python dosyasını çalıştırın:
python metro_simulasyon.py

3. Terminalde örnek çıktılar görüntülenecek, ardından sizden başlangıç ve hedef istasyonlar istenecek.
