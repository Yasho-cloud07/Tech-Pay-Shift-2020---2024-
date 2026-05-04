# Tech-Pay-Shift-2020---2024
# ⚡ Tech Pay Shift — Global Compensation & Remote Work Dynamics (2020–2024)

An interactive data visualization project analyzing how remote work has reshaped global tech salaries using real-world datasets.

---

## 📌 Overview

This project explores the evolution of tech salaries from 2020 to 2024, focusing on:

- 💼 Experience-based salary distribution  
- 🌐 Global salary differences adjusted for GDP (PPP)  
- 🏠 Impact of remote work on compensation  
- 📈 Time-series divergence between remote and onsite roles  

The goal is to move beyond averages and uncover **distributional insights, inequality trends, and global pay dynamics**.

---

## 📊 Data Sources

### 1. Data Science Salaries Dataset (Kaggle)
- 4,000+ records of global tech salaries  
- Features:
  - Salary (USD standardized)
  - Experience level
  - Remote ratio (0%, 50%, 100%)
  - Company & employee location  

🔗 https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries  

### 2. World Bank GDP per Capita (PPP)
- Country-level economic data  
- Used to normalize salaries across countries  

🔗 https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD  

---

## 🚀 Features

- 📊 **Interactive Dashboard (Streamlit)**
- 🎛️ Real-time filtering:
  - Year
  - Experience level
  - Work mode (Remote / Hybrid / Onsite)
  - Country
- 🌍 **Choropleth Map** for salary-to-GDP ratio
- 📈 **Time-series analysis** of remote vs onsite salaries
- 🎻 **Distribution visualizations** (Violin plots & KDE)
- 💡 Insight cards explaining trends and methodology

---

## 🧠 Key Insights

- Remote work significantly increased salary dispersion, especially at senior levels  
- High-income countries show lower salary-to-GDP ratios compared to emerging markets  
- Remote salary premiums peaked around 2023 and are stabilizing  
- Salary distributions shifted upward during the remote work boom  

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Plotly**
- **NumPy / SciPy**

---

## 📁 Project Structure
Tech-Pay-Shift/
│
├── app.py # Main Streamlit app
├── processed_data.csv # Cleaned dataset
├── README.md # Project documentation
├── requirements.txt # Dependencies
└── assets/ # Optional images / animations


---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/tech-pay-shift.git
cd tech-pay-shift
pip install -r requirements.txt
streamlit run app.py
