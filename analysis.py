"""
Stack Overflow Developer Survey 2025 — US Market Analysis
==========================================================
Author : Libert Kanojerera
Dataset: survey_results_public_2025_v1.csv
"""

# =============================================================================
# 0. IMPORTS
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# PART 1: DATA CLEANING & WRANGLING
# =============================================================================

# -----------------------------------------------------------------------------
# Task 1 — Load & Inspect
# -----------------------------------------------------------------------------
# Attempt to read the CSV with a fallback for encoding issues.
# The raw file contains bytes that are invalid UTF-8, so we try a sequence of
# encodings and report which one succeeds.

encodings_to_try = [
    'utf-8',        # default
    'utf-8-sig',    # handles BOM (byte-order mark)
    'latin-1',      # very permissive; will not raise on undecodable bytes
    'cp1252',       # common Windows encoding
]

last_error = None
for enc in encodings_to_try:
    try:
        df = pd.read_csv('survey_results_public_2025_v1.csv', encoding=enc)
        print(f"Loaded CSV successfully using encoding: {enc}")
        break
    except UnicodeDecodeError as e:
        print(f"Failed with encoding {enc}: {e}")
        last_error = e
else:
    # Last-resort fallback: latin-1 with error replacement
    try:
        with open('survey_results_public_2025_v1.csv', 'r', encoding='latin-1', errors='replace') as f:
            df = pd.read_csv(f)
        print("Loaded CSV using latin-1 with errors='replace' fallback.")
    except Exception as e:
        raise RuntimeError(
            f"Unable to load CSV. Last Unicode error: {last_error}; Fallback error: {e}"
        )

print(df.head())
print(df.info())


# -----------------------------------------------------------------------------
# Task 2 — Filter by Country (United States only)
# -----------------------------------------------------------------------------
# .copy() prevents SettingWithCopyWarning on downstream mutations.
df_usa = df[df['Country'] == 'United States of America'].copy()
print(df_usa.info())


# -----------------------------------------------------------------------------
# Task 3 — Filter by Employment (Employed only)
# -----------------------------------------------------------------------------
df_employed = df_usa[df_usa['Employment'] == 'Employed'].copy()
df_employed.info()


# -----------------------------------------------------------------------------
# Task 4 — Drop rows with missing salary
# -----------------------------------------------------------------------------
df_employed = df_employed.dropna(subset=['ConvertedCompYearly']).copy()
df_employed.info()


# -----------------------------------------------------------------------------
# Task 5 — Impute missing JobSat with group median
# -----------------------------------------------------------------------------
print("Missing before:", df_employed['JobSat'].isna().sum())
print("Median JobSat:", df_employed['JobSat'].median())

df_employed['JobSat'] = df_employed['JobSat'].fillna(df_employed['JobSat'].median())

print("Missing after:", df_employed['JobSat'].isna().sum())


# -----------------------------------------------------------------------------
# Task 6 — Coerce YearsCode and WorkExp to numeric
# -----------------------------------------------------------------------------
df_employed['YearsCode'] = pd.to_numeric(df_employed['YearsCode'], errors='coerce')
df_employed['WorkExp']   = pd.to_numeric(df_employed['WorkExp'],   errors='coerce')

print(df_employed[['YearsCode', 'WorkExp']].dtypes)
print("YearsCode missing:", df_employed['YearsCode'].isna().sum())
print("WorkExp missing:  ", df_employed['WorkExp'].isna().sum())


# -----------------------------------------------------------------------------
# Task 7 — Feature engineering: is_python_dev boolean flag
# -----------------------------------------------------------------------------
# LanguageHaveWorkedWith is a semicolon-separated multi-value string.
# .str.contains() handles partial matching without splitting overhead.
df_employed['is_python_dev'] = (
    df_employed['LanguageHaveWorkedWith'].str.contains('Python', na=False)
)

print(df_employed['is_python_dev'].value_counts())
print()
print(df_employed[['LanguageHaveWorkedWith', 'is_python_dev']].head(10))


# -----------------------------------------------------------------------------
# Task 8 — Simplify EdLevel into three tiers
# -----------------------------------------------------------------------------
def simplify_ed(level):
    if pd.isna(level):
        return 'Other'
    level = level.lower()
    if 'bachelor' in level:
        return 'Undergrad'
    if 'master' in level or 'doctoral' in level or 'professional' in level:
        return 'Graduate'
    return 'Other'

df_employed['EdLevel'] = df_employed['EdLevel'].apply(simplify_ed)
print(df_employed['EdLevel'].value_counts())


# =============================================================================
# PART 2: DEMOGRAPHIC & EXPERIENCE EXPLORATION
# =============================================================================

# -----------------------------------------------------------------------------
# Task 9 — Age Distribution (Bar Chart)
# -----------------------------------------------------------------------------
plt.figure(figsize=(10, 5))
df_employed['Age'].value_counts().sort_index().plot(kind='bar')
plt.title('US Developer Age Distribution')
plt.tight_layout()
plt.show()


# -----------------------------------------------------------------------------
# Task 10 — Experience Summary: mean & median YearsCode
# -----------------------------------------------------------------------------
mean_exp   = df_employed['YearsCode'].mean()
median_exp = df_employed['YearsCode'].median()

print(f"Mean Experience:   {mean_exp:.2f} years")
print(f"Median Experience: {median_exp} years")


# -----------------------------------------------------------------------------
# Task 11 — Pearson correlation: YearsCode vs. Salary
# -----------------------------------------------------------------------------
correlation_years = df_employed[['YearsCode', 'ConvertedCompYearly']].corr()
corr_years = correlation_years.loc['YearsCode', 'ConvertedCompYearly']
print(f"Correlation (YearsCode vs Salary): {corr_years:.4f}")


# -----------------------------------------------------------------------------
# Task 12 — Pearson correlation: WorkExp vs. Salary
# -----------------------------------------------------------------------------
correlation_workexp = df_employed[['WorkExp', 'ConvertedCompYearly']].corr()
corr_work = correlation_workexp.loc['WorkExp', 'ConvertedCompYearly']
print(f"Correlation (WorkExp vs Salary): {corr_work:.4f}")
# Observation: both correlations are similar (~0.10–0.14), suggesting that
# raw years of experience is only weakly predictive of salary.


# =============================================================================
# PART 3: COMPENSATION & INDUSTRY INSIGHTS
# =============================================================================

# -----------------------------------------------------------------------------
# Task 13 — Salary Distribution (Histogram + KDE)
# -----------------------------------------------------------------------------
# Filter BEFORE plotting so the KDE is computed on the truncated distribution,
# not just clipped visually — avoids a misleadingly flat curve.
salary_data = df_employed['ConvertedCompYearly'].dropna()
salary_data = salary_data[salary_data <= 500_000]

fig, ax = plt.subplots(figsize=(10, 6))

sns.histplot(
    data=salary_data,
    kde=True,
    bins=50,
    color='steelblue',
    edgecolor='white',
    linewidth=0.5,
    ax=ax,
)

ax.set_title('Salary Distribution of Employed Developers (US)', fontsize=14)
ax.set_xlabel('Annual Compensation (USD)', fontsize=12)
ax.set_ylabel('Number of Respondents', fontsize=12)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# -----------------------------------------------------------------------------
# Task 14 — The Python Premium
# -----------------------------------------------------------------------------
python_premium = (
    df_employed
    .groupby('is_python_dev')['ConvertedCompYearly']
    .median()
)

print(python_premium)
print()

py_med     = python_premium[True]
non_py_med = python_premium[False]

print(f"Python Median Salary:     ${py_med:,.2f}")
print(f"Non-Python Median Salary: ${non_py_med:,.2f}")
print(f"The 'Python Premium' is:  ${py_med - non_py_med:,.2f}")


# -----------------------------------------------------------------------------
# Task 15 — Remote Work & Pay (Boxplot)
# -----------------------------------------------------------------------------
df_plot = df_employed[df_employed['ConvertedCompYearly'] <= 500_000].copy()

print(f"Rows before filter: {len(df_employed)}")
print(f"Rows after filter:  {len(df_plot)}")
print(f"Rows removed:       {len(df_employed) - len(df_plot)}")

# Sort categories by median salary (descending) for readability
remote_order = (
    df_plot
    .groupby('RemoteWork')['ConvertedCompYearly']
    .median()
    .sort_values(ascending=False)
    .index
)

fig, ax = plt.subplots(figsize=(10, 6))

sns.boxplot(
    data=df_plot,
    x='RemoteWork',
    y='ConvertedCompYearly',
    order=remote_order,
    color='steelblue',
    width=0.5,
    flierprops=dict(marker='o', markerfacecolor='steelblue', markersize=3, alpha=0.4),
    ax=ax,
)

ax.set_title('Compensation by Remote Work Status', fontsize=14)
ax.set_xlabel('Remote Work Type', fontsize=12)
ax.set_ylabel('Annual Compensation (USD)', fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig('remote_work_salary.png', dpi=150)
plt.show()


# -----------------------------------------------------------------------------
# Task 16 — Job Satisfaction vs. Pay (Boxplot)
# -----------------------------------------------------------------------------
df_plot = df_employed[df_employed['ConvertedCompYearly'] <= 500_000].copy()
jobsat_order = sorted(df_plot['JobSat'].dropna().unique())

fig, ax = plt.subplots(figsize=(10, 6))

sns.boxplot(
    data=df_plot,
    x='JobSat',
    y='ConvertedCompYearly',
    order=jobsat_order,
    color='steelblue',
    width=0.5,
    flierprops=dict(marker='o', markerfacecolor='steelblue', markersize=3, alpha=0.4),
    ax=ax,
)

ax.set_title('Salary Distribution by Job Satisfaction Score (US)', fontsize=14)
ax.set_xlabel('Job Satisfaction Score (0 = Lowest, 10 = Highest)', fontsize=12)
ax.set_ylabel('Annual Compensation (USD)', fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig('jobsat_salary.png', dpi=150)
plt.show()


# -----------------------------------------------------------------------------
# Task 17 — Top 10 Highest-Paying Industries (Bar Chart)
# -----------------------------------------------------------------------------
df_plot = df_employed[df_employed['ConvertedCompYearly'] <= 500_000].copy()

top10_industries = (
    df_plot
    .groupby('Industry')['ConvertedCompYearly']
    .median()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 8))

sns.barplot(
    x=top10_industries.values,
    y=top10_industries.index,
    palette='crest',
    ax=ax,
)

for i, val in enumerate(top10_industries.values):
    ax.text(val * 1.01, i, f'${val:,.0f}', va='center', fontsize=9)

ax.set_title('Top 10 Highest Paying Industries (Median)', fontsize=14)
ax.set_ylabel('Industry')
ax.set_xlabel('Median Salary (USD)')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top10_industries_salary.png', dpi=150)
plt.show()


# -----------------------------------------------------------------------------
# Task 18 — Company Size Impact
# -----------------------------------------------------------------------------
org_med = (
    df_employed
    .groupby('OrgSize')['ConvertedCompYearly']
    .median()
    .sort_values(ascending=False)
)

print("\nMedian Salary by Organization Size:\n", org_med)
# Observation: larger organisations pay substantially more — consistent with
# structured pay bands and access to high-value product domains.


# -----------------------------------------------------------------------------
# Task 19 — Identify Salary Outliers (> 3 SD above mean)
# -----------------------------------------------------------------------------
salary_mean = df_employed['ConvertedCompYearly'].mean()
salary_std  = df_employed['ConvertedCompYearly'].std()

threshold  = salary_mean + (3 * salary_std)
n_outliers = (df_employed['ConvertedCompYearly'] > threshold).sum()
n_total    = df_employed['ConvertedCompYearly'].notna().sum()
outlier_pct = (n_outliers / n_total) * 100

print(f"\nPercentage of extreme salary outliers: {outlier_pct:.2f}%")


# -----------------------------------------------------------------------------
# Task 20 — The $150k Threshold: Python vs. Non-Python developers
# -----------------------------------------------------------------------------
df_employed['high_earner'] = df_employed['ConvertedCompYearly'] > 150_000

high_earner_stats = (
    df_employed
    .groupby('is_python_dev')['high_earner']
    .mean() * 100
)

print(f"High Earner % (Python Developers):     {high_earner_stats[True]:.2f}%")
print(f"High Earner % (Non-Python Developers): {high_earner_stats[False]:.2f}%")
