# 📊 Stack Overflow Developer Survey 2025 — US Market Analysis

> **Author:** Kanojerera  
> **Dataset:** Stack Overflow Annual Developer Survey 2025  
> **Environment:** [Deepnote](https://deepnote.com)

---

## 🗂️ Project Overview

This project walks the full data science pipeline, from raw, messy survey data to polished, actionable insights, using the **2025 Stack Overflow Developer Survey**, one of the most comprehensive annual censuses of software professionals worldwide.

The analysis focuses specifically on the **United States employed developer market**, probing the relationships between education, experience, language choice, industry, and compensation.

---

## 🎯 Objectives

- Build robust data wrangling pipelines (encoding fallback, filtering, imputation, type coercion)
- Engineer new features from free-text multi-value columns (e.g., `is_python_dev`)
- Conduct demographic and experience-driven EDA
- Quantify the **"Python Premium"** in developer compensation
- Visualise salary distributions, satisfaction patterns, and industry/company-size effects
- Identify and characterise high-earning outliers

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3** | Core language |
| **pandas** | Data wrangling & aggregation |
| **matplotlib** | Base plotting |
| **seaborn** | Statistical visualisation |
| **Deepnote** | Collaborative notebook environment |

---

## 📦 Dataset

| Property | Value |
|----------|-------|
| Source | Stack Overflow Annual Developer Survey 2025 |
| File | `survey_results_public_2025_v1.csv` |
| Raw rows | 49,132 |
| Columns used | 17 (ResponseId, Age, EdLevel, Employment, WorkExp, YearsCode, DevType, OrgSize, RemoteWork, Industry, Country, LanguageHaveWorkedWith, AIThreat, AISelect, ConvertedCompYearly, JobSat, MainBranch) |

---

## 🔄 Data Pipeline

### Part 1 — Cleaning & Wrangling

| Task | Technique | Outcome |
|------|-----------|---------|
| Load with encoding fallback | `pd.read_csv` with `latin-1` fallback | 49,132 rows loaded cleanly |
| Filter: US respondents | Boolean indexing | 7,226 US records |
| Filter: Employed only | `== 'Employed'` | 5,408 employed |
| Drop missing salaries | `.dropna(subset=['ConvertedCompYearly'])` | 4,529 records with salary |
| Impute JobSat | `.fillna(median)` | 0 nulls remaining |
| Type coerce numeric | `pd.to_numeric(..., errors='coerce')` | YearsCode, WorkExp → float64 |
| Feature engineer `is_python_dev` | `.str.contains('Python', na=False)` | 2,703 Python / 1,826 non-Python devs |
| Simplify EdLevel | Custom function + `.apply()` | Undergrad / Graduate / Other |

---

## 📈 Key Findings

### 1. Age Distribution
US employed developers are predominantly in the **25–44** age range, reflecting mid-career professionals and a relatively young workforce.

### 2. Experience vs. Compensation
| Metric | Value |
|--------|-------|
| Mean YearsCode | **20.3 years** |
| Median YearsCode | **18.0 years** |
| Pearson r (YearsCode vs Salary) | **0.138** |
| Pearson r (WorkExp vs Salary) | **0.101** |

> **Insight:** Experience has only a weak positive correlation with salary (~0.14). Other factors (tech stack, industry, company size) likely explain more variance.

---

### 3. Salary Distribution

Salary is **right-skewed**: the bulk of US employed developers earn between **$50k–$250k**, with a long tail above that.  
Filtered to ≤ $500k to avoid visual distortion from extreme outliers.

---

### 4. The Python Premium 🐍

| Group | Median Salary |
|-------|--------------|
| Python developers | **$157,000** |
| Non-Python developers | **$148,000** |
| **Premium** | **+$9,000** |

> **Insight:** Python proficiency is associated with a **~6% salary premium** at the median. Given Python's dominance in data science, ML, and automation — where compensation tends to be elevated — this is consistent with market dynamics.

---

### 5. Remote Work & Pay

Salary distributions vary across remote work models. Remote-heavy arrangements tend toward higher medians, though hybrid modes cluster similarly. The data  suggests location flexibility correlates with (but does not solely drive) higher pay ([See Chart](outputs/remote_work_salary.png)). 

---

### 6. Job Satisfaction vs. Pay

No strong linear relationship between salary and job satisfaction score (0–10) ([See chart](outputs/jobsat_salary.png)). Developers at the extremes of satisfaction (very low or very high) show wide salary variance, suggesting satisfaction is driven by factors beyond compensation alone.

---

### 7. Top 10 Highest-Paying Industries (Median)

| Rank | Industry | Median Salary |
|------|----------|--------------|
| 1 | *([see chart](outputs/top10_industries_salary.png))* | highest |
| … | … | … |
| 10 | *([see chart](outputs/top10_industries_salary.png))*| … |
<img width="996" height="790" alt="top10_industries_salary" src="https://github.com/user-attachments/assets/ebdb216c-77fa-483b-829a-ea9097d3bfe8" />

> Finance, cloud/SaaS, and software development sectors consistently top the list.

---

### 8. Company Size & Compensation

| Company Size | Median Salary |
|-------------|--------------|
| 10,000+ employees | **$171,500** |
| 5,000–9,999 | $160,000 |
| 100–499 | $154,000 |
| 1,000–4,999 | $150,000 |
| 500–999 | $146,350 |
| 20–99 | $145,000 |
| < 20 / Freelancer | $75,000 – $125,000 |

> **Insight:** Larger organisations pay substantially more — likely due to structured pay bands, economies of scale, and greater access to high-value domains.

---

### 9. Salary Outliers

Only **0.82%** of respondents earn more than 3 standard deviations above the mean — confirming the right tail is thin but real (executive/principal engineers, high-equity roles).

---

### 10. The $150k Club

| Group | % Earning > $150k |
|-------|-----------------|
| Python developers | **51.9%** |
| Non-Python developers | **45.6%** |

> More than half of Python developers clear the $150k mark, compared to ~46% of non-Python peers — reinforcing the Python Premium finding.

---

## 📁 Repository Structure

```
├── README.md                          ← This file
├── SO_data_analysis.ipynb      ← Full analysis notebook
└── outputs/
    ├── remote_work_salary.png
    ├── jobsat_salary.png
    └── top10_industries_salary.png
```

---

## 🚀 Running the Notebook

1. **Clone or download** this repository.
2. **Place the dataset** `survey_results_public_2025_v1.csv` in the same directory as the notebook.
3. **Install dependencies:**
   ```bash
   pip install pandas matplotlib seaborn
   ```
4. **Open the notebook** in Jupyter or Deepnote and run all cells.

> ⚠️ The dataset CSV is not included in this repository due to size. Download it directly from [Stack Overflow Insights](https://insights.stackoverflow.com/survey).

---

## 💡 Design Decisions & Lessons Learned

- **Encoding fallback strategy:** UTF-8 decoding fails on this dataset. The code gracefully falls back through `utf-8-sig` → `latin-1`, logging each attempt. This pattern is production-grade for real-world messy CSVs.
- **Copy discipline:** Every filtered subset uses `.copy()` to prevent `SettingWithCopyWarning` and unintended view mutation.
- **Outlier handling for visualisation:** Salary histograms and boxplots filter to ≤ $500k *before* plotting (not just axis-limiting) so the KDE and IQR calculations remain meaningful.
- **Median over mean:** Throughout this analysis, median salary is preferred over mean due to the right skew of compensation data.
- **Feature engineering from multi-value strings:** `LanguageHaveWorkedWith` stores semicolon-delimited lists. `.str.contains()` handles this cleanly without splitting overhead.

---

## 🔭 Extensions & Future Work

- [ ] Regression modelling: predict salary from experience, education, Python use, company size
- [ ] NLP on DevType column to cluster developer roles and salary
- [ ] Year-over-year comparison (2023 → 2025) to track the Python Premium trend
- [ ] AI tools adoption (`AISelect`, `AIThreat`) and its effect on job satisfaction

---

## 📜 License

This project is for educational purposes. The Stack Overflow survey data is © Stack Overflow and subject to their [usage terms](https://insights.stackoverflow.com/survey).
