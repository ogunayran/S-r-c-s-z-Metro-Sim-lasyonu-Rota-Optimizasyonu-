from collections import defaultdict, deque
import heapq
from typing import Dict, List,Set, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """
        BFS algoritması kullanarak en az aktarmalı (en az kenar geçişli) rotayı bulur.
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. BFS algoritmasını kullanarak en az aktarmalı rotayı bulun
        3. Rota bulunamazsa None, bulunursa istasyon listesi döndürün
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        ziyaret_edildi = set([baslangic])
        queue = deque([(baslangic, [baslangic])])

        while queue:
            mevcut_istasyon, yol = queue.popleft()
            
            # Hedefe ulaştıysak yolu döndür
            if mevcut_istasyon == hedef:
                return yol
            
            # Komşuları ziyaret et
            for komsu, _ in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    queue.append((komsu, yol + [komsu]))

        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        A* algoritması (heuristic=0, yani fiilen Dijkstra) kullanarak en hızlı rotayı bulur
        1. Başlangıç ve hedef istasyonların varlığını kontrol eder
        2. A* (Dijkstra benzeri) algoritmasıyla en az süreli rota bulunur
        3. Rota yoksa None, varsa (istasyon_listesi, toplam_sure) döndürülür
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        en_iyi_sure = {istasyon: float('inf') for istasyon in self.istasyonlar.values()}
        en_iyi_sure[baslangic] = 0

        yollar = {istasyon: [] for istasyon in self.istasyonlar.values()}
        yollar[baslangic] = [baslangic]

        pq = [(0, id(baslangic), baslangic)]
        ziyaret_edilen = set()

        while pq:
            mevcut_oncelik, _, mevcut_istasyon = heapq.heappop(pq)

            if mevcut_istasyon == hedef:
                return (yollar[mevcut_istasyon], en_iyi_sure[mevcut_istasyon])

            if mevcut_istasyon in ziyaret_edilen:
                continue
            ziyaret_edilen.add(mevcut_istasyon)

            for komsu, sure in mevcut_istasyon.komsular:
                yeni_sure = en_iyi_sure[mevcut_istasyon] + sure
                if yeni_sure < en_iyi_sure[komsu]:
                    en_iyi_sure[komsu] = yeni_sure
                    yollar[komsu] = yollar[mevcut_istasyon] + [komsu]
                    f = yeni_sure
                    heapq.heappush(pq, (f, id(komsu), komsu))

        return None

    def compute_route_duration(self, route: List[Istasyon]) -> int:
        """
        Verilen rota (istasyon listesi) üzerinden gidilen toplam süreyi hesaplar.
        Her ardışık iki istasyon arasındaki bağlantı süresi toplanır.
        """
        total = 0
        for i in range(len(route) - 1):
            current = route[i]
            next_station = route[i + 1]
            # current'in komşuları arasında next_station'ı arıyoruz.
            for neighbor, sure in current.komsular:
                if neighbor == next_station:
                    total += sure
                    break
        return total

    def visualize_graph(self):
        """
        Metro ağını NetworkX ve Matplotlib kullanarak görselleştirir.
        Bu versiyonda, düğümlerin konumları el ile (manuel) belirlenmiştir.
        """
        G = nx.Graph()
        
        for station in self.istasyonlar.values():
            G.add_node(station.idx, label=station.ad, hat=station.hat)
        
        added_edges = set()
        for station in self.istasyonlar.values():
            for neighbor, weight in station.komsular:
                edge = tuple(sorted([station.idx, neighbor.idx]))
                if edge not in added_edges:
                    G.add_edge(station.idx, neighbor.idx, weight=weight)
                    added_edges.add(edge)
        
        # Manuel olarak belirlenen düğüm konumları (örnek değerler, ihtiyaca göre ayarlayın)
        pos = {
            "K1": (0, 2),
            "K2": (1, 2),
            "K3": (2, 2),
            "K4": (3, 2),
            "M1": (0, 1),
            "M2": (1, 1),
            "M3": (2, 1),
            "M4": (3, 1),
            "T1": (0, 0),
            "T2": (1, 0),
            "T3": (2, 0),
            "T4": (3, 0)
        }
        
        hat_color = {"Kırmızı Hat": "red", "Mavi Hat": "blue", "Turuncu Hat": "orange"}
        node_colors = [hat_color.get(G.nodes[node]['hat'], "gray") for node in G.nodes]
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)
        nx.draw_networkx_edges(G, pos)
        labels = {node: G.nodes[node]['label'] for node in G.nodes}
        nx.draw_networkx_labels(G, pos, labels, font_size=7)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        plt.title("Ankara Metro Ağı")
        plt.axis("off")
        plt.show()
    
    def find_station_by_ad(self, ad: str) -> Optional[Istasyon]:
        """
        Verilen istasyon adını (durak ismini) arar ve eşleşen istasyon nesnesini döndürür.
        Büyük/küçük harf duyarlılığı olmadan karşılaştırılır.
        """
        for station in self.istasyonlar.values():
            if station.ad.lower() == ad.lower():
                return station
        return None

if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay(K)", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler(K)", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay(M)", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar(M)", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler(T)", "Turuncu Hat")
    metro.istasyon_ekle("T3", "Gar(T)", "Turuncu Hat")
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)
    metro.baglanti_ekle("K2", "K3", 6)
    metro.baglanti_ekle("K3", "K4", 8)
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)
    metro.baglanti_ekle("M2", "M3", 3)
    metro.baglanti_ekle("M3", "M4", 4)
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)
    metro.baglanti_ekle("T2", "T3", 9)
    metro.baglanti_ekle("T3", "T4", 5)
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)
    metro.baglanti_ekle("K3", "T2", 3)
    metro.baglanti_ekle("M4", "T3", 2)
    
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota1 = metro.en_az_aktarma_bul("M1", "K4")
    if rota1:
        duration1 = metro.compute_route_duration(rota1)
        print("En az aktarmalı rota ({} dakika):".format(duration1), " -> ".join(i.ad for i in rota1))
    
    # Senaryo 2: AŞTİ'den OSB'ye en hızlı rota (A*)
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota2, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota2))
    
    # Senaryo 3: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota3 = metro.en_az_aktarma_bul("T1", "T4")
    if rota3:
        duration3 = metro.compute_route_duration(rota3)
        print("En az aktarmalı rota ({} dakika):".format(duration3), " -> ".join(i.ad for i in rota3))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota4, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota4))
    
    # Senaryo 4: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota5 = metro.en_az_aktarma_bul("T4", "M1")
    if rota5:
        duration5 = metro.compute_route_duration(rota5)
        print("En az aktarmalı rota ({} dakika):".format(duration5), " -> ".join(i.ad for i in rota5))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota6, sure = sonuc
        print(f"En hızlı rota ( {sure} dakika):", " -> ".join(i.ad for i in rota6))
    
 
    
    # Kullanıcı tarafından seçilen istasyonlar için hem en az aktarmalı hem en hızlı rotaları yazdırma
    print("\n--- Kullanıcı İstasyonu ---")
    baslangic_ad = input("Lütfen başlangıç istasyonunun adını girin: ")
    hedef_ad = input("Lütfen hedef istasyonunun adını girin: ")
    
    ist1 = metro.find_station_by_ad(baslangic_ad)
    ist2 = metro.find_station_by_ad(hedef_ad)
    
    if ist1 and ist2:
        rota_kullanici_bfs = metro.en_az_aktarma_bul(ist1.idx, ist2.idx)
        if rota_kullanici_bfs:
            duration_kullanici_bfs = metro.compute_route_duration(rota_kullanici_bfs)
            print("Kullanıcı tarafından seçilen istasyonlar arasındaki en az aktarmalı rota ({} dakika):".format(duration_kullanici_bfs),
                  " -> ".join(i.ad for i in rota_kullanici_bfs))
        else:
            print("Kullanıcı tarafından seçilen istasyonlar arasında en az aktarmalı rota bulunamadı.")
        
        sonuc_hizli = metro.en_hizli_rota_bul(ist1.idx, ist2.idx)
        if sonuc_hizli:
            rota_kullanici_hizli, sure = sonuc_hizli
            print("Kullanıcı tarafından seçilen istasyonlar arasındaki en hızlı rota ({} dakika):".format(sure),
                  " -> ".join(i.ad for i in rota_kullanici_hizli))
        else:
            print("Kullanıcı tarafından seçilen istasyonlar arasında en hızlı rota bulunamadı.")
    else:
        print("Girilen istasyon isimlerinden en az biri haritada bulunamadı.")
       # Tüm test rotalarını görselleştir
    metro.visualize_graph()