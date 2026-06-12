import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style('whitegrid')
plt.rcParams['font.family'] = 'Tahoma'
plt.rcParams['font.size'] = 11

df = pd.read_csv('food_coded.csv')
gender_map = {1: 'Female', 2: 'Male'}

# Chart 1: Gender Distribution
fig, ax = plt.subplots(figsize=(5, 4))
df['gender'].map(gender_map).value_counts().plot(kind='bar', color=['#ff6b6b', '#4ecdc4'], ax=ax)
ax.set_title('Gender Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Gender')
ax.set_ylabel('Count')
for i, v in enumerate(df['gender'].map(gender_map).value_counts()):
    ax.text(i, v + 1, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('assets/chart_gender.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] chart_gender.png')

# Chart 2: Average Calories by Gender
cal_cols = ['calories_chicken', 'calories_scone', 'waffle_calories', 'tortilla_calories', 'turkey_calories']
df_cal = df[['gender'] + cal_cols].copy()
for c in cal_cols:
    df_cal[c] = pd.to_numeric(df_cal[c], errors='coerce')
avg_cal = df_cal.groupby('gender').mean()
avg_cal.index = avg_cal.index.map(gender_map)

fig, ax = plt.subplots(figsize=(8, 4))
avg_cal.plot(kind='bar', ax=ax, color=['#ff6b6b', '#4ecdc4', '#ffe66d', '#95e1d3', '#f38181'])
ax.set_title('Average Calories by Gender', fontsize=14, fontweight='bold')
ax.set_xlabel('Gender')
ax.set_ylabel('Avg Calories')
ax.legend(loc='upper right', fontsize=8)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('assets/chart_calories.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] chart_calories.png')

# Chart 3: Top Favorite Cuisines
top_cuisines = df['fav_cuisine'].value_counts().head(8)
fig, ax = plt.subplots(figsize=(8, 4))
colors = sns.color_palette('husl', 8)
top_cuisines.plot(kind='barh', color=colors, ax=ax)
ax.set_title('Top 8 Favorite Cuisines', fontsize=14, fontweight='bold')
ax.set_xlabel('Count')
ax.set_ylabel('Cuisine')
for i, v in enumerate(top_cuisines):
    ax.text(v + 0.3, i, str(v), va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('assets/chart_cuisines.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] chart_cuisines.png')

# Chart 4: Comfort Food Reasons
def simplify_reason(r):
    r = str(r).lower()
    if 'stress' in r or 'angry' in r or 'sad' in r or 'depress' in r or 'anxiety' in r:
        return 'Stress/Sadness'
    if 'bored' in r:
        return 'Boredom'
    if 'hunger' in r or 'hungry' in r:
        return 'Hunger'
    if 'happy' in r or 'celeb' in r or 'satisf' in r:
        return 'Happiness'
    if 'tired' in r:
        return 'Tiredness'
    if 'lazy' in r:
        return 'Laziness'
    return 'Other'

df['reason_simple'] = df['comfort_food_reasons'].apply(simplify_reason)
reason_counts = df['reason_simple'].value_counts()
fig, ax = plt.subplots(figsize=(7, 5))
colors = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#95e1d3', '#f38181', '#a8e6cf']
wedges, texts, autotexts = ax.pie(
    reason_counts, labels=reason_counts.index, autopct='%1.1f%%',
    colors=colors, startangle=90, textprops={'fontsize': 10}
)
ax.set_title('Why Students Eat Comfort Food?', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('assets/chart_comfort_food.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] chart_comfort_food.png')

# Chart 5: Exercise vs Veggies intake
exercise_map = {0: 'None', 1: 'Light', 2: 'Moderate', 3: 'Active', 4: 'Very Active', 5: 'Extreme'}
df['exercise_label'] = df['exercise'].map(exercise_map)
exercise_order = ['None', 'Light', 'Moderate', 'Active', 'Very Active', 'Extreme']
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=df, x='exercise_label', y='veggies_day', order=exercise_order,
            palette='Blues_d', ax=ax, ci=None)
ax.set_title('Exercise Frequency vs Veggies Intake', fontsize=14, fontweight='bold')
ax.set_xlabel('Exercise Frequency')
ax.set_ylabel('Avg Veggies per Day')
plt.tight_layout()
plt.savefig('assets/chart_exercise_veggies.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] chart_exercise_veggies.png')

# Chart 6: Income vs Nutrition
income_map = {1: 'Low', 2: 'Low-Mid', 3: 'Mid', 4: 'Mid-High', 5: 'High', 6: 'Very High', 7: 'Wealthy', 8: 'N/A'}
df['income_label'] = df['income'].map(income_map)
fig, ax = plt.subplots(figsize=(9, 4))
income_nutrition = df.groupby('income')[['veggies_day', 'fruit_day', 'calories_day']].mean()
income_nutrition.index = income_nutrition.index.map(income_map)
income_nutrition.plot(kind='bar', ax=ax, color=['#2ecc71', '#3498db', '#e74c3c'])
ax.set_title('Income Level vs Nutrition', fontsize=14, fontweight='bold')
ax.set_xlabel('Income Level')
ax.set_ylabel('Average Score')
ax.legend(loc='upper left', fontsize=8)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('assets/chart_income_nutrition.png', dpi=150, bbox_inches='tight')
plt.close()
print('[OK] chart_income_nutrition.png')

print('\n=== All charts generated in assets/ ===')
