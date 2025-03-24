from collections import defaultdict, deque  # defaultdict: varsayılan değerli sözlük, deque: çift uçlu kuyruk
import heapq  # Öncelik kuyruğu (min-heap) yapısı için kullanılır
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx    # İstasyonun benzersiz kimliği
        self.ad = ad      # İstasyonun adı
        self.hat = hat    # İstasyonun ait olduğu hat
        # Her istasyonun, komşu istasyonları ve aralarındaki seyahat süresini içeren bir liste
        self.komsular: List[Tuple['Istasyon', int]] = []  

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        # Mevcut istasyona, belirtilen süre ile komşu istasyonu ekler
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        # Tüm istasyonları tutan sözlük (anahtar: istasyon kimliği)
        self.istasyonlar: Dict[str, Istasyon] = {}
        # Hat isimlerine göre istasyonları listeleyen sözlük
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        # Eğer istasyon daha önce eklenmediyse yeni bir istasyon oluştur ve ekle
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        # İki istasyon arasındaki bağlantıyı, çift yönlü olarak ekler
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """
        BFS algoritması kullanılarak en az aktarmalı rota bulunur.
        
        İşleyiş:
        1. Başlangıç ve hedef istasyonun varlığı kontrol edilir.
        2. deque (çift uçlu kuyruk) yapısı kullanılarak BFS uygulanır.
        3. Her adımda, mevcut istasyonun tüm komşuları kontrol edilerek,
           daha önce ziyaret edilmemişse kuyruga eklenir.
        4. Hedef istasyon bulunursa, o ana kadar izlenen rota döndürülür.
        5. Rota bulunamazsa None döndürülür.
        """
        # Başlangıç veya hedef istasyon yoksa fonksiyondan çıkılır.
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # deque kullanılarak kuyruk oluşturulur, her eleman (mevcut istasyon,o ana kadar izlenen rota)
        kuyruk = deque([(baslangic, [baslangic])])
        # Ziyaret edilen istasyonları tutan küme, tekrarlı ziyaretleri önlemek için
        ziyaret_edilen = {baslangic}
        
        while kuyruk:
            su_an, rota = kuyruk.popleft()  # Kuyruğun başından eleman alınır
            # Eğer mevcut istasyon hedef istasyon ise, o ana kadar izlenen rota döndürülür
            if su_an == hedef:
                return rota
            # Mevcut istasyonun tüm komşuları incelenir
            for komsu, _ in su_an.komsular:
                if komsu not in ziyaret_edilen:
                    ziyaret_edilen.add(komsu)  # Tekrardan ziyaret edilmemesi için eklenir
                    # Mevcut rota üzerine yeni komşu istasyon eklenerek kuyruga eklenir
                    kuyruk.append((komsu, rota + [komsu]))
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        A* algoritması benzeri (burada heuristik sıfır kabul edilip Dijkstra'ya yakın çalışmaktadır)
        yaklaşımı kullanılarak en hızlı rota bulunur.
        
        İşleyiş:
        1. Başlangıç ve hedef istasyon kontrol edilir.
        2. heapq (öncelik kuyruğu) kullanılarak, toplam seyahat süresine göre
           en hızlı rota aranır.
        3. Her adımda, mevcut istasyona ulaşmak için harcanan toplam süre hesaplanır.
        4. Eğer hedef istasyona ulaşıldıysa, o ana kadar izlenen rota ve toplam süre döndürülür.
        5. Eğer daha önce aynı istasyona daha kısa sürede ulaşıldıysa, o dal atlanır.
        6. Rota bulunamazsa None döndürülür.
        """
        # Başlangıç veya hedef istasyon yoksa fonksiyondan çıkılır.
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # Öncelik kuyruğuna ilk eleman eklenir; 
        # Tuple elemanları: (şu ana kadar toplam süre, benzersiz id, mevcut istasyon, o ana kadar izlenen rota)
        priority_queue = [(0, id(baslangic), baslangic, [baslangic])]
        
        # Her istasyona varılan en kısa süreyi tutmak için bir sözlük
        ziyaret_edilen: Dict[Istasyon, int] = {}
        
        while priority_queue:
            toplam_sure, _, su_an, rota = heapq.heappop(priority_queue)
            # Hedefe ulaşıldıysa, rota ve toplam süre döndürülür
            if su_an == hedef:
                return (rota, toplam_sure)
            # Eğer daha önce bu istasyona daha kısa sürede ulaşılmışsa, bu dal işleme alınmaz
            if su_an in ziyaret_edilen and ziyaret_edilen[su_an] <= toplam_sure:
                continue
            ziyaret_edilen[su_an] = toplam_sure
            # Mevcut istasyonun tüm komşuları incelenir
            for komsu, sure in su_an.komsular:
                yeni_sure = toplam_sure + sure  # Komşuya varmak için harcanan toplam süre
                # Eğer daha önce bu komşuya daha kısa sürede ulaşılmışsa, onu tekrar eklemeyiz
                if komsu in ziyaret_edilen and ziyaret_edilen[komsu] <= yeni_sure:
                    continue
                # Yeni komşu istasyon, güncellenmiş süre ile öncelik kuyruğuna eklenir
                heapq.heappush(priority_queue, (yeni_sure, id(komsu), komsu, rota + [komsu]))
        return None

# Aşağıdaki bölüm, modül doğrudan çalıştırıldığında test senaryolarının yürütülmesini sağlar
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme: Her hat için ilgili istasyonlar ekleniyor.
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")           # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # İstasyonlar arası bağlantılar ekleniyor.
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Aktarma bağlantıları: Farklı hatlardaki aynı istasyonlar arası bağlantılar
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları: Farklı başlangıç ve hedef noktaları ile fonksiyonlar test ediliyor.
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
