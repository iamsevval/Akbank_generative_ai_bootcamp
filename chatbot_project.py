import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt


# -----------------------
# Ortam Ayarları
# -----------------------
load_dotenv()
st.set_page_config(page_title="Yazılım Kariyer Chatbotu", page_icon="🤖", layout="wide" )
st.title("💼 Yazılım Kariyer Yol Haritası Chatbotu")

# -----------------------
# OpenAI API Ayarı
# -----------------------
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("🚨 OPENAI_API_KEY bulunamadı. Lütfen .env veya Streamlit Secrets'e ekleyin.")
    st.stop()

client = OpenAI(api_key=api_key)

# -----------------------
# Veri Setlerini Oku
# -----------------------
csv_files = {
    "salary_basic": "datasets/Software_Professional_Salaries.csv",
    "salary_extra": "datasets/Salary_Dataset_with_Extra_Features.csv",
    "jobs_basic": "datasets/Software_Engineer_Salaries.csv",
    "career_fields": "datasets/career_path_in_all_field.csv",
    "career_student": "datasets/computer_science_student_career_datasetMar62024.csv",
    "postings": "datasets/postings2.csv"
}

dfs = {}
for key, path in csv_files.items():
    try:
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip()
        dfs[key] = df
    except FileNotFoundError:
        st.warning(f"{path} bulunamadı, bu veri seti yüklenmedi.")

df_salary_basic = dfs.get("salary_basic", pd.DataFrame())
df_salary_extra = dfs.get("salary_extra", pd.DataFrame())
df_jobs = dfs.get("jobs_basic", pd.DataFrame())
df_postings = dfs.get("postings", pd.DataFrame())

# -----------------------
# Yazılım Alanı Seçimi
# -----------------------
software_fields = ["Mobile", "Web", "Backend", "Frontend", "Game", "Full Stack", "DevOps", "AI"]
selected_field = st.selectbox("İlgilendiğiniz yazılım alanını seçin:", software_fields)

# -----------------------
# Career Data
# -----------------------
career_data = {
    "Mobile": {
        "Learning_Path": ["Kotlin veya Swift öğrenin", "Mobil UI/UX temellerini çalışın", "API ve veri yönetimini öğrenin"],
        "Projects": ["Todo uygulaması", "Hava durumu uygulaması", "Chat uygulaması"],
        "Similar_Fields": ["Web", "Full Stack", "Backend"]
    },
    "Web": {
        "Learning_Path": ["HTML, CSS, JavaScript öğrenin", "Frontend framework: React, Angular, Vue", "Backend: Node.js veya Django öğrenin"],
        "Projects": ["Portfolio sitesi", "E-ticaret sitesi", "Blog platformu"],
        "Similar_Fields": ["Frontend", "Backend", "Full Stack"]
    },
    "Backend": {
        "Learning_Path": ["Python, Java veya C# öğrenin", "API geliştirme ve veri tabanı yönetimi", "RESTful servisler oluşturun"],
        "Projects": ["Blog API", "Stok yönetim sistemi", "RESTful servisler"],
        "Similar_Fields": ["Full Stack", "DevOps", "Web"]
    },
    "Frontend": {
        "Learning_Path": ["HTML, CSS, JavaScript öğrenin", "React, Angular veya Vue öğrenin", "UI/UX ve responsive design çalışın"],
        "Projects": ["Landing page", "Dashboard", "E-ticaret frontend"],
        "Similar_Fields": ["Web", "Full Stack", "Mobile"]
    },
    "Game": {
        "Learning_Path": ["Unity veya Unreal Engine öğrenin", "C# veya C++ öğrenin", "2D/3D oyun tasarımı ve fizik motoru"],
        "Projects": ["Basit platformer", "Puzzle oyunu", "Mini RPG"],
        "Similar_Fields": ["AI", "Mobile", "Backend"]
    },
    "Full Stack": {
        "Learning_Path": ["Frontend: React veya Vue", "Backend: Node.js, Django veya Flask", "Veritabanı yönetimi ve deployment"],
        "Projects": ["E-ticaret platformu", "Sosyal ağ sitesi", "Blog platformu"],
        "Similar_Fields": ["Frontend", "Backend", "Web"]
    },
    "DevOps": {
        "Learning_Path": ["CI/CD araçlarını öğrenin", "Docker ve Kubernetes kullanın", "AWS, GCP veya Azure öğrenin"],
        "Projects": ["Otomatik deploy pipeline oluşturun"],
        "Similar_Fields": ["Backend", "Full Stack", "Cloud"]
    },
    "AI": {
        "Learning_Path": ["Python, NumPy, Pandas öğrenin", "TensorFlow veya PyTorch ile ML ve DL öğrenin", "Temel makine öğrenmesi algoritmalarını çalışın"],
        "Projects": ["Basit chatbot", "Görüntü sınıflandırma", "Tahmin modelleri"],
        "Similar_Fields": ["Data Science", "Backend", "Game"]
    }
}

# -----------------------
# Örnek Soru Butonları
# -----------------------
# -----------------------
# Örnek Soru Butonları ve Ekstra Veri
# -----------------------
st.subheader("💬 Soru Seçimi veya Yazma")
st.write("Aşağıdaki butonlardan birini tıklayarak sorabilirsiniz:")

col1, col2, col3, col4, col5 = st.columns(5)
user_question = ""

with col1:
    if st.button("Öğrenme Yolu"):
        user_question = "Öğrenme yolu nedir?"
with col2:
    if st.button("Proje Önerileri"):
        user_question = "Hangi projeleri yapabilirim?"
with col3:
    if st.button("Benzer Alanlar"):
        user_question = "Benzer alanlar nelerdir?"

# -----------------------
# Alan Bazlı Ortalama Maaşlar
# -----------------------
with col4:
    if st.button("Ortalama Maaşlar"):
        if not df_salary_basic.empty:
            st.subheader(f"💰 {selected_field} Alanı Ortalama Maaşlar")
            
            # Alan bazlı filtre (Job Title içinde alan adı geçiyorsa)
            df_field_salary = df_salary_basic[df_salary_basic["Job Title"].str.contains(selected_field, case=False, na=False)]
            
            if df_field_salary.empty:
                st.warning(f"{selected_field} alanı için maaş verisi bulunamadı.")
            else:
                avg_salary_by_job = df_field_salary.groupby("Job Title")["Salary"].mean().sort_values(ascending=False)
                st.dataframe(
                avg_salary_by_job.reset_index().rename(columns={"Job Title":"Pozisyon", "Salary":"Ortalama Maaş"}),
                width=1200,  
                height=400   
)
                
                # Grafik
                fig, ax = plt.subplots(figsize=(12,6))
                avg_salary_by_job.plot(kind="bar", ax=ax, color="skyblue")
                ax.set_title(f"{selected_field} Alanı Ortalama Maaşlar", fontsize=16)
                ax.set_ylabel("Ortalama Maaş")
                ax.set_xlabel("Pozisyon")
                plt.xticks(rotation=45, ha="right")
                st.pyplot(fig)
        else:
            st.warning("💡 Maaş verisi bulunamadı.")

# -----------------------
# Alan Bazlı Top Şirketlerden İş İlanları
# -----------------------
with col5:
    if st.button("Top Şirketlerden İş İlanları"):
        if not df_jobs.empty:
            st.subheader(f"🏢 {selected_field} Alanı Top Şirketler")
            
            # Alan bazlı filtre
            df_field_jobs = df_jobs[df_jobs["Job Title"].str.contains(selected_field, case=False, na=False)]
            
            if df_field_jobs.empty:
                st.warning(f"{selected_field} alanı için iş ilanı bulunamadı.")
            else:
                top_companies = df_field_jobs["Company"].value_counts().head(10)
                st.write("En çok ilan açan şirketler:")
                st.dataframe(top_companies.reset_index().rename(columns={"index": "Şirket", "Company": "İlan Sayısı"}))
                
                # Grafik
                fig, ax = plt.subplots(figsize=(12,6))
                top_companies.plot(kind="barh", ax=ax, color="orange")
                ax.set_title(f"{selected_field} Alanı En Çok İlan Açan Şirketler", fontsize=16)
                ax.set_xlabel("İlan Sayısı")
                ax.set_ylabel("Şirket")
                plt.gca().invert_yaxis()
                st.pyplot(fig)
                
                st.write("Örnek iş ilanları:")
                st.dataframe(
                df_field_jobs[["Job Title", "Company", "Salary"]].head(10),
                width=1200,
                height=400
)

        else:
            st.warning("💡 İş ilanları verisi bulunamadı.")


# Kullanıcı kendi sorusunu da yazabilir
custom_question = st.text_input("Veya kendi sorunuzu yazın:")
if custom_question:
    user_question = custom_question

# -----------------------
# Chatbot Mantığı
# -----------------------
if user_question:
    query = user_question.lower()
    
    # Career veri kontrolü
    if "öğrenme yolu" in query:
        st.write("📘 Öğrenme Yolu:")
        for step in career_data[selected_field]["Learning_Path"]:
            st.write(f"- {step}")
    elif "proje" in query:
        st.write("💡 Önerilen Projeler:")
        for proj in career_data[selected_field]["Projects"]:
            st.write(f"- {proj}")
    elif "benzer alan" in query or "alt alan" in query:
        st.write("🔄 Benzer Alanlar:")
        for similar in career_data[selected_field]["Similar_Fields"]:
            st.write(f"- {similar}")
    else:
        # Salary & Jobs veri setlerinden metin birleştirme
        salary_combined = pd.concat([df_salary_basic, df_salary_extra], ignore_index=True)
        salary_combined["passage"] = salary_combined.apply(
            lambda row: f"Job Title: {row.get('Job Title','')}, Company: {row.get('Company Name','')}, Salary: {row.get('Salary','')}",
            axis=1
        )
        
        jobs_combined = pd.concat([df_jobs, df_postings], ignore_index=True)
        jobs_combined["passage"] = jobs_combined.apply(
            lambda row: f"Job Title: {row.get('Job Title', row.get('job_title',''))}, Company: {row.get('Company', row.get('company',''))}, Salary: {row.get('Salary','')}",
            axis=1
        )
        
        matched_salary = salary_combined[salary_combined["passage"].str.lower().str.contains(query, na=False)]
        matched_jobs = jobs_combined[jobs_combined["passage"].str.lower().str.contains(query, na=False)]
        
        if not matched_salary.empty or not matched_jobs.empty:
            passages_text = " ".join(matched_salary["passage"].tolist() + matched_jobs["passage"].tolist())
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen bir yazılım kariyer chatbotusun."},
                    {"role": "user", "content": f"Soru: {user_question}\nBilgi: {passages_text}"}
                ]
            )
            chatbot_answer = response.choices[0].message.content
            st.write(chatbot_answer)
        else:
            st.info("🤖 Bu soruya uygun veri bulunamadı. Örnek sorulardan birini deneyebilirsiniz.")
