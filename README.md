# 📊 Stack Overflow Developer Survey 2025 — US Market Analysis

> **Author:** Kanojerera  
> **Dataset:** Stack Overflow Annual Developer Survey 2025  
> **Environment:** [Deepnote](https://deepnote.com)

---

## 🗂️ Project Overview

This project walks the complete data science pipeline — from a raw, messy survey CSV to polished, actionable insights — using the **2025 Stack Overflow Developer Survey**, one of the most comprehensive annual censuses of software professionals worldwide (49,000+ respondents).

The analysis focuses on the **United States employed developer market**, investigating how education, experience, language choice, industry, and company size relate to compensation and job satisfaction.

---

## 📁 Repository Structure

```
├── README.md          ← This file
├── analysis.py        ← All 20 tasks in Python code
└── outputs/
    ├── remote_work_salary.png
    ├── jobsat_salary.png
    └── top10_industries_salary.png
```

> ⚠️ The raw dataset (`survey_results_public_2025_v1.csv`) is not included due to file size. Download it from [Stack Overflow Insights](https://insights.stackoverflow.com/survey) and place it in the project root.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3** | Core language |
| **pandas** | Data wrangling & aggregation |
| **matplotlib** | Base plotting |
| **seaborn** | Statistical visualisation |

**Install dependencies:**
```bash
pip install pandas matplotlib seaborn
```

---

## 🔄 The Pipeline at a Glance

The full code lives in [`analysis.py`](./analysis.py), organised into three parts that mirror the assignment structure.

### Part 1 — Data Cleaning & Wrangling (Tasks 1–8)

| Task | What the code does |
|------|--------------------|
| **1 — Load & Inspect** | Reads the CSV with a chained encoding fallback (`utf-8` → `utf-8-sig` → `latin-1` → `cp1252`) and inspects shape/dtypes |
| **2 — Filter: Country** | Boolean-indexes to US respondents; uses `.copy()` to avoid `SettingWithCopyWarning` |
| **3 — Filter: Employment** | Keeps only `'Employed'` rows |
| **4 — Drop Missing Salaries** | `.dropna(subset=['ConvertedCompYearly'])` |
| **5 — Impute JobSat** | Fills the 781 missing satisfaction scores with the group median |
| **6 — Coerce to Numeric** | `pd.to_numeric(..., errors='coerce')` on `YearsCode` and `WorkExp` |
| **7 — Feature Engineer `is_python_dev`** | `str.contains('Python', na=False)` on the semicolon-delimited `LanguageHaveWorkedWith` column |
| **8 — Simplify EdLevel** | Custom function + `.apply()` → `'Undergrad'` / `'Graduate'` / `'Other'` |

```python
# Task 2 — US filter
df_usa = df[df['Country'] == 'United States of America'].copy()

# Task 7 — Python developer flag
df_employed['is_python_dev'] = (
    df_employed['LanguageHaveWorkedWith'].str.contains('Python', na=False)
)

# Task 8 — Education simplification
def simplify_ed(level):
    if pd.isna(level): return 'Other'
    level = level.lower()
    if 'bachelor' in level: return 'Undergrad'
    if 'master' in level or 'doctoral' in level or 'professional' in level: return 'Graduate'
    return 'Other'

df_employed['EdLevel'] = df_employed['EdLevel'].apply(simplify_ed)
```

---

### Part 2 — Demographic & Experience Exploration (Tasks 9–12)

```python
# Task 9 — Age distribution bar chart
df_employed['Age'].value_counts().sort_index().plot(kind='bar')

# Tasks 10–12 — Experience statistics
mean_exp   = df_employed['YearsCode'].mean()    # 20.30 years
median_exp = df_employed['YearsCode'].median()  # 18.0 years

corr_years = (df_employed[['YearsCode', 'ConvertedCompYearly']].corr()
                          .loc['YearsCode', 'ConvertedCompYearly'])   # 0.1380

corr_work  = (df_employed[['WorkExp', 'ConvertedCompYearly']].corr()
                          .loc['WorkExp', 'ConvertedCompYearly'])     # 0.1014
```

---

### Part 3 — Compensation & Industry Insights (Tasks 13–20)

```python
# Task 14 — Python Premium
python_premium = (
    df_employed
    .groupby('is_python_dev')['ConvertedCompYearly']
    .median()
)
# True  -> $157,000   False -> $148,000   Premium -> $9,000

# Task 15 — Remote work boxplot (sorted by median)
remote_order = (
    df_plot.groupby('RemoteWork')['ConvertedCompYearly']
    .median().sort_values(ascending=False).index
)
sns.boxplot(data=df_plot, x='RemoteWork', y='ConvertedCompYearly', order=remote_order)

# Task 17 — Top 10 paying industries
top10_industries = (
    df_plot.groupby('Industry')['ConvertedCompYearly']
    .median().sort_values(ascending=False).head(10)
)

# Task 19 — Outlier detection (> 3 SD above mean)
threshold   = df_employed['ConvertedCompYearly'].mean() + 3 * df_employed['ConvertedCompYearly'].std()
outlier_pct = (df_employed['ConvertedCompYearly'] > threshold).mean() * 100  # 0.82%

# Task 20 — $150k threshold by Python use
df_employed['high_earner'] = df_employed['ConvertedCompYearly'] > 150_000
high_earner_stats = df_employed.groupby('is_python_dev')['high_earner'].mean() * 100
# Python devs: 51.91%   Non-Python devs: 45.56%
```

---

## 📈 Key Findings

### Dataset after cleaning

| Stage | Rows |
|-------|------|
| Raw survey | 49,132 |
| US respondents | 7,226 |
| US + Employed | 5,408 |
| US + Employed + Has salary | **4,529** |

---

### Experience vs. Compensation

| Metric | Value |
|--------|-------|
| Mean coding experience | 20.3 years |
| Median coding experience | 18.0 years |
| Pearson r (YearsCode × Salary) | **0.138** |
| Pearson r (WorkExp × Salary) | **0.101** |

> Raw years of experience is only weakly correlated with salary. Tech stack, industry, and company size explain far more variance.

---

### 🐍 The Python Premium

| Group | Median Salary |
|-------|--------------|
| Python developers | **$157,000** |
| Non-Python developers | $148,000 |
| **Premium** | **+$9,000 (+6%)** |

---

### Company Size & Pay

| Organisation Size | Median Salary |
|-------------------|--------------|
| 10,000+ employees | **$171,500** |
| 5,000–9,999 | $160,000 |
| 100–499 | $154,000 |
| 1,000–4,999 | $150,000 |
| 500–999 | $146,350 |
| 20–99 | $145,000 |
| Freelancer / sole proprietor | $75,000 |

> Larger organisations pay substantially more — consistent with structured pay bands, economies of scale, and access to high-value product domains.

---

### Salary Outliers

Only **0.82%** of respondents earn more than 3 standard deviations above the mean — confirming the right tail is real but thin (executive/principal engineers, high-equity roles).

---

### The $150k Club

| Group | % Earning > $150k |
|-------|-----------------|
| Python developers | **51.91%** |
| Non-Python developers | 45.56% |

---

## 💡 Engineering Notes

**Encoding fallback**  
The raw CSV cannot be decoded with UTF-8. The code gracefully falls back through `utf-8-sig` → `latin-1` → `cp1252`, logging each attempt. This pattern is production-grade for real-world messy files.

**`.copy()` discipline**  
Every filtered subset calls `.copy()` immediately. This prevents silent view mutations and suppresses `SettingWithCopyWarning` across all downstream assignments.

**Outlier handling for visualisation**  
Salary plots filter to ≤ $500k *before* computing the histogram/KDE, not just by clamping the axis. This keeps the KDE and IQR calculations meaningful rather than distorted by extreme values.

**Median over mean**  
Salary data is right-skewed. All compensation comparisons use the median, which is more robust to the long upper tail than the mean.

**Multi-value string feature engineering**  
`LanguageHaveWorkedWith` stores semicolon-delimited lists (e.g., `"Python;SQL;JavaScript"`). `.str.contains()` handles partial matching cleanly without the overhead of splitting every row.

---

## 🔭 Extensions & Future Work

- [ ] OLS / Ridge regression: predict salary from experience, education, Python use, company size
- [ ] Cluster developer roles from the free-text `DevType` column
- [ ] Year-over-year comparison (2023 → 2025) to track the Python Premium trend
- [ ] Explore `AISelect` / `AIThreat` columns — does AI adoption correlate with job satisfaction or salary?

---

## 📜 License

Educational use only. The Stack Overflow survey data is © Stack Overflow and subject to their [usage terms](https://insights.stackoverflow.com/survey).
