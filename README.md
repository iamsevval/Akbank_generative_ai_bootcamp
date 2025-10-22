# 💼 Yazılım Kariyer Yol Haritası Chatbotu

## Projenin Amacı
Bu proje, kullanıcıların ilgilendiği yazılım alanına göre:
- Ortalama maaşlar,
- Top şirketlerden iş ilanları,
- Önerilen öğrenme yolları ve projeler,
- Benzer kariyer alanları  

bilgilerini sunan **RAG (Retrieval-Augmented Generation) tabanlı chatbot** geliştirmeyi amaçlamaktadır.

---

## Veri Setleri Hakkında
Projede kullanılan veri setleri hazır veri setleridir:

| Veri Seti | Açıklama |
|-----------|----------|
| Software_Professional_Salaries.csv | Yazılım profesyonellerinin iş unvanı, şirket ve maaş bilgileri |
| Salary_Dataset_with_Extra_Features.csv | Maaş verilerine ek bilgiler (lokasyon, deneyim yılı vb.) |
| Software_Engineer_Salaries.csv | Yazılım mühendisleri için detaylı maaş verileri |
| postings2.csv | Farklı şirketlerden yazılım iş ilanları |
| career_path_in_all_field.csv | Yazılım alanındaki kariyer yollarını gösterir |
| computer_science_student_career_datasetMar62024.csv | Bilgisayar bilimi öğrencilerinin kariyer tercihleri |

---

## Kullanılan Yöntemler
- **Web Arayüzü:** Streamlit
- **Veri İşleme:** Pandas
- **RAG Pipeline:** FAISS + LangChain
- **Dil Modeli:** OpenAI GPT-4 API

---

## Çözüm Mimarisi
**RAG (Retrieval-Augmented Generation) Mimarisi:**

1. **Retriever (Bilgi Getirici):** CSV verilerinden embedding’ler oluşturulur, FAISS vektör veritabanında saklanır.
2. **LLM (Cevap Üretici):** GPT-4 modeli, kullanıcı sorusunu ve retriever’dan gelen verileri kullanarak cevap üretir.
3. **Frontend (Sunum Katmanı):** Streamlit arayüzü, kullanıcı ile etkileşimi sağlar.


## Canlı Uygulama

Akbank Generative AI Bootcamp kapsamında hazırlanan uygulamaya [buradan ulaşabilirsiniz](https://akbankgenerativeaibootcamp-lc2hnscvjeidlpmofpabtv.streamlit.app/).
