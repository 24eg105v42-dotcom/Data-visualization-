"""
================================================
  Data Cleaning & Visualization Project
  Tools  : Pandas, Matplotlib, Seaborn
  Dataset: Student Performance (Synthetic)
================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# STEP 1: Create Raw Dataset (with issues)
# ─────────────────────────────────────────────
np.random.seed(42)
n = 200

df = pd.DataFrame({
    'StudentID'   : range(1, n+1),
    'Age'         : np.random.randint(17, 25, n),
    'Gender'      : np.random.choice(['Male', 'Female', 'male', 'FEMALE'], n),
    'MathScore'   : np.random.randint(30, 100, n).astype(float),
    'ScienceScore': np.random.randint(30, 100, n).astype(float),
    'EnglishScore': np.random.randint(30, 100, n).astype(float),
    'Attendance'  : np.random.uniform(50, 100, n),
    'Grade'       : np.random.choice(['A', 'B', 'C', 'D', 'F'], n)
})

# Introduce missing values
df.loc[np.random.choice(n, 15, replace=False), 'MathScore']    = np.nan
df.loc[np.random.choice(n, 15, replace=False), 'ScienceScore'] = np.nan
df.loc[np.random.choice(n, 15, replace=False), 'EnglishScore'] = np.nan
df.loc[np.random.choice(n, 15, replace=False), 'Attendance']   = np.nan
df.loc[np.random.choice(n, 15, replace=False), 'Gender']       = np.nan
df.loc[np.random.choice(n, 10, replace=False), 'Grade']        = np.nan

# Introduce outlier ages
df.loc[5,  'Age'] = 999
df.loc[10, 'Age'] = -5

# Introduce duplicate rows
df = pd.concat([df, df.iloc[:10]], ignore_index=True)

# ─────────────────────────────────────────────
# STEP 2: Explore Raw Data
# ─────────────────────────────────────────────
print("=" * 55)
print("   DATA CLEANING & VISUALIZATION PROJECT")
print("=" * 55)
print(f"\n[1] Raw Shape        : {df.shape}")
print(f"[2] Duplicate Rows   : {df.duplicated().sum()}")
print(f"\n[3] Missing Values (Before Cleaning):")
print(df.isnull().sum().to_string())

# ─────────────────────────────────────────────
# STEP 3: Remove Duplicates
# ─────────────────────────────────────────────
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)

# ─────────────────────────────────────────────
# STEP 4: Handle Outliers (Age)
# ─────────────────────────────────────────────
df.loc[(df['Age'] < 10) | (df['Age'] > 30), 'Age'] = np.nan
df['Age'] = df['Age'].fillna(df['Age'].median()).astype(int)

# ─────────────────────────────────────────────
# STEP 5: Fill Missing Values
# ─────────────────────────────────────────────
for col in ['MathScore', 'ScienceScore', 'EnglishScore', 'Attendance']:
    df[col] = df[col].fillna(df[col].median())

df['Gender'] = df['Gender'].fillna(df['Gender'].dropna().mode()[0]).str.capitalize()
df['Grade']  = df['Grade'].fillna(df['Grade'].dropna().mode()[0])

# ─────────────────────────────────────────────
# STEP 6: Feature Engineering
# ─────────────────────────────────────────────
df['TotalScore'] = df['MathScore'] + df['ScienceScore'] + df['EnglishScore']
df['Percentage'] = (df['TotalScore'] / 300 * 100).round(2)

print(f"\n[4] Clean Shape      : {df.shape}")
print(f"\n[5] Missing Values (After Cleaning):")
print(df.isnull().sum().to_string())
print(f"\n[6] Sample Data (3 rows):")
print(df[['Age','Gender','MathScore','ScienceScore',
          'EnglishScore','Attendance','Grade','Percentage']].head(3).to_string(index=False))

# ─────────────────────────────────────────────
# STEP 7: VISUALIZATION DASHBOARD (3×3)
# ─────────────────────────────────────────────
palette = ['#2E86AB', '#E84855', '#3BB273', '#F4A261', '#8338EC']
sns.set_style('whitegrid')

fig = plt.figure(figsize=(18, 14))
fig.suptitle('Student Performance Dashboard', fontsize=22,
             fontweight='bold', y=0.99, color='#1a1a2e')

# Plot 1: Score Distribution
ax1 = fig.add_subplot(3, 3, 1)
for col, c in zip(['MathScore', 'ScienceScore', 'EnglishScore'], palette):
    ax1.hist(df[col], bins=15, alpha=0.65,
             label=col.replace('Score', ''), color=c, edgecolor='white')
ax1.set_title('Score Distribution', fontweight='bold')
ax1.set_xlabel('Score'); ax1.set_ylabel('Frequency')
ax1.legend(fontsize=8)

# Plot 2: Boxplot
ax2 = fig.add_subplot(3, 3, 2)
bp = ax2.boxplot([df['MathScore'], df['ScienceScore'], df['EnglishScore']],
                 labels=['Math', 'Science', 'English'], patch_artist=True)
for patch, c in zip(bp['boxes'], palette):
    patch.set_facecolor(c); patch.set_alpha(0.7)
ax2.set_title('Boxplot – Outlier Detection', fontweight='bold')
ax2.set_ylabel('Score')

# Plot 3: Gender Bar Chart
ax3 = fig.add_subplot(3, 3, 3)
gc = df['Gender'].value_counts()
bars = ax3.bar(gc.index, gc.values, color=palette[:2], edgecolor='white', width=0.5)
for b in bars:
    ax3.text(b.get_x()+b.get_width()/2, b.get_height()+1,
             str(int(b.get_height())), ha='center', fontsize=9, fontweight='bold')
ax3.set_title('Gender Distribution', fontweight='bold'); ax3.set_ylabel('Count')

# Plot 4: Grade Pie Chart
ax4 = fig.add_subplot(3, 3, 4)
grd = df['Grade'].value_counts().sort_index()
ax4.pie(grd.values, labels=grd.index, autopct='%1.1f%%', colors=palette,
        startangle=90, wedgeprops=dict(edgecolor='white'))
ax4.set_title('Grade Distribution', fontweight='bold')

# Plot 5: Correlation Heatmap
ax5 = fig.add_subplot(3, 3, 5)
corr = df[['MathScore', 'ScienceScore', 'EnglishScore',
           'Attendance', 'Percentage']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', ax=ax5,
            linewidths=0.5, square=True)
ax5.set_title('Correlation Heatmap', fontweight='bold')
ax5.set_xticklabels(['Math', 'Sci', 'Eng', 'Att', '%'], rotation=30, fontsize=8)
ax5.set_yticklabels(['Math', 'Sci', 'Eng', 'Att', '%'], rotation=0, fontsize=8)

# Plot 6: Attendance vs Percentage Scatter
ax6 = fig.add_subplot(3, 3, 6)
sc = ax6.scatter(df['Attendance'], df['Percentage'],
                 c=df['Percentage'], cmap='RdYlGn',
                 alpha=0.7, edgecolors='gray', linewidths=0.3, s=40)
plt.colorbar(sc, ax=ax6, label='Percentage')
ax6.set_title('Attendance vs Percentage', fontweight='bold')
ax6.set_xlabel('Attendance (%)'); ax6.set_ylabel('Overall %')

# Plot 7: Avg Score by Gender
ax7 = fig.add_subplot(3, 3, 7)
avg = df.groupby('Gender')[['MathScore', 'ScienceScore', 'EnglishScore']].mean()
x = np.arange(3); w = 0.35
ax7.bar(x - w/2, avg.loc['Male'],   w, label='Male',   color=palette[0], edgecolor='white')
ax7.bar(x + w/2, avg.loc['Female'], w, label='Female', color=palette[1], edgecolor='white')
ax7.set_xticks(x); ax7.set_xticklabels(['Math', 'Science', 'English'])
ax7.set_title('Avg Score by Gender', fontweight='bold')
ax7.set_ylabel('Avg Score'); ax7.legend(fontsize=8)

# Plot 8: Avg Percentage by Grade
ax8 = fig.add_subplot(3, 3, 8)
ap = df.groupby('Grade')['Percentage'].mean().sort_index()
bars2 = ax8.bar(ap.index, ap.values, color=palette, edgecolor='white')
for b in bars2:
    ax8.text(b.get_x()+b.get_width()/2, b.get_height()+0.3,
             f'{b.get_height():.1f}', ha='center', fontsize=8, fontweight='bold')
ax8.set_title('Avg Percentage by Grade', fontweight='bold')
ax8.set_ylabel('Percentage (%)')

# Plot 9: Age Distribution
ax9 = fig.add_subplot(3, 3, 9)
ax9.hist(df['Age'], bins=8, color=palette[2], edgecolor='white')
ax9.set_title('Age Distribution', fontweight='bold')
ax9.set_xlabel('Age'); ax9.set_ylabel('Count')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('/mnt/user-data/outputs/dashboard.png', dpi=150, bbox_inches='tight')
plt.close()

# ─────────────────────────────────────────────
# STEP 8: Save Cleaned Dataset
# ─────────────────────────────────────────────
df.to_csv('/mnt/user-data/outputs/cleaned_student_data.csv', index=False)

print("\n[7] Dashboard saved  → dashboard.png")
print("[8] CSV saved        → cleaned_student_data.csv")
print("\n" + "=" * 55)
print("   PROJECT COMPLETE!")
print("=" * 55)
