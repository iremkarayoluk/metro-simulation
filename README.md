# Metro Ağı Rota Bulucu

Bu proje, bir metro ağında iki istasyon arasındaki en az aktarmalı ve en hızlı rotayı bulmayı sağlayan bir Python uygulamasıdır.

## Kullanılan Teknolojiler ve Kütüphaneler

- *Python:* Proje, Python programlama dili kullanılarak geliştirilmiştir.
- *collections.deque:* BFS (genişlik öncelikli arama) algoritmasını uygulamak için kullanılmıştır. deque yapısı, elemanların eklenmesi ve çıkarılmasında O(1) zaman karmaşıklığı sunar.
- *collections.defaultdict:* İstasyonları ve hatları tutan sözlük yapısını, varsayılan değer üreterek (liste) kolaylaştırmak için kullanılmıştır.
- *heapq:* En hızlı rotayı bulmak için öncelik kuyruğu (min-heap) yapısını uygular. Bu yapı, en kısa sürede ulaşılabilen istasyonu hızlıca seçmeye olanak sağlar.
- *typing:* Kodun okunabilirliğini artırmak ve tip kontrolü sağlamak için kullanılmıştır.

## Algoritmaların Çalışma Mantığı

### BFS (Breadth-First Search) - En Az Aktarmalı Rota

- *Nasıl Çalışır?*
  - Başlangıç istasyonundan başlanarak, komşu istasyonlar sırayla ziyaret edilir.
  - Her adımda, mevcut istasyona olan uzaklık (aktarma sayısı) artırılır.
  - İlk bulunan hedef istasyon, en az aktarma yapılan yoldur çünkü BFS katman katman ilerler.
  
- *Neden Kullanıldı?*
  - BFS, en kısa yol (en az aktarma) problemleri için idealdir.
  - Ağdaki tüm düğümleri katman katman ziyaret ettiği için, hedefe ulaşıldığında o rota en az aktarmalı olur.

### A* Algoritması (Dijkstra Benzeri Yaklaşım) - En Hızlı Rota

- *Nasıl Çalışır?*
  - Başlangıç istasyonundan, her istasyona ulaşmak için geçen toplam süre hesaplanır.
  - Öncelik kuyruğu (heapq) kullanılarak, en düşük toplam süreye sahip rota sürekli olarak genişletilir.
  - Heuristik olarak bu örnekte ek bir tahmin kullanılmamış, yani sıfır kabul edilerek temel Dijkstra algoritması mantığı uygulanmıştır.
  
- *Neden Kullanıldı?*
  - A* (veya Dijkstra) algoritması, ağırlıklı graf yapılarında (burada süreler ağırlık olarak kullanılmıştır) en kısa/sürekli yolu bulmada etkilidir.
  - Rota üzerindeki toplam süreyi minimize etmek için öncelik kuyruğu sayesinde en verimli yol hızlıca bulunur.

## Proje Çalıştırma

1. *Gerekli Python Sürümü:*  
   Python 3.x (3.6 ve üzeri tavsiye edilir)

2. *Dosya Yapısı:*
   - İremKarayoluk_MetroSimulation.py: Ana kod dosyası. İçerisinde istasyonlar, bağlantılar ve rota bulma algoritmaları yer alır.
   - README.md: Projenin genel açıklamalarını ve kullanılan teknolojileri içerir.

3. *Çalıştırma:*
   Terminal veya komut satırında proje dizinine gidip aşağıdaki komut ile çalıştırabilirsiniz:
   ```bash
   İremKarayoluk_MetroSimulation.py
