import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
import numpy as np

def get_percentage_male(df):
    male_count = df[df['Sex']=='male'].shape[0]
    return round((male_count / len(df)) * 100, 2)

def average_fare(df):
    return round(df['Fare'].mean(), 2)

def embarked_counts(df):
    return df['Embarked'].value_counts().to_dict()

def plot_age_histogram(df):
    plt.figure(figsize=(8,5))
    sns.histplot(df['Age'], bins=30, kde=True)
    plt.title('Age Distribution of Titanic Passengers')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def plot_embarked_bar(df):
    plt.figure(figsize=(8,5))
    sns.countplot(x='Embarked', data=df)
    plt.title('Passengers Embarked from Each Port')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

# New utility functions for expanded questions
def survival_rate(df):
    survived = df['Survived'].sum()
    total = len(df)
    return round((survived / total) * 100, 2)

def survival_by_class(df):
    return df.groupby('Pclass')['Survived'].mean() * 100

def survival_by_gender(df):
    return df.groupby('Sex')['Survived'].mean() * 100

def class_distribution(df):
    return df['Pclass'].value_counts().sort_index()

def age_statistics(df):
    return {
        'min': round(df['Age'].min(), 1),
        'max': round(df['Age'].max(), 1),
        'mean': round(df['Age'].mean(), 1),
        'median': round(df['Age'].median(), 1)
    }

def fare_statistics(df):
    return {
        'min': round(df['Fare'].min(), 2),
        'max': round(df['Fare'].max(), 2),
        'mean': round(df['Fare'].mean(), 2),
        'median': round(df['Fare'].median(), 2)
    }

def family_size_distribution(df):
    df_copy = df.copy()
    df_copy['FamilySize'] = df_copy['SibSp'] + df_copy['Parch'] + 1
    return df_copy['FamilySize'].value_counts().sort_index()

def plot_survival_by_class(df):
    plt.figure(figsize=(8,5))
    survival_rates = df.groupby('Pclass')['Survived'].mean() * 100
    sns.barplot(x=survival_rates.index, y=survival_rates.values)
    plt.title('Survival Rate by Passenger Class')
    plt.ylabel('Survival Rate (%)')
    plt.xlabel('Passenger Class')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def plot_survival_by_gender(df):
    plt.figure(figsize=(8,5))
    survival_rates = df.groupby('Sex')['Survived'].mean() * 100
    sns.barplot(x=survival_rates.index, y=survival_rates.values)
    plt.title('Survival Rate by Gender')
    plt.ylabel('Survival Rate (%)')
    plt.xlabel('Gender')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def plot_class_distribution(df):
    plt.figure(figsize=(8,5))
    class_counts = df['Pclass'].value_counts().sort_index()
    sns.barplot(x=class_counts.index, y=class_counts.values)
    plt.title('Passenger Class Distribution')
    plt.ylabel('Number of Passengers')
    plt.xlabel('Passenger Class')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def plot_fare_distribution(df):
    plt.figure(figsize=(8,5))
    sns.histplot(df['Fare'], bins=50, kde=True)
    plt.title('Fare Distribution of Titanic Passengers')
    plt.xlabel('Fare ($)')
    plt.ylabel('Number of Passengers')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

# Additional utility functions for comprehensive questions
def youngest_passenger(df):
    return df['Age'].min()

def oldest_passenger(df):
    return df['Age'].max()

def children_count(df):
    return len(df[df['Age'] < 18])

def males_survived(df):
    return df[(df['Sex'] == 'male') & (df['Survived'] == 1)].shape[0]

def females_survived(df):
    return df[(df['Sex'] == 'female') & (df['Survived'] == 1)].shape[0]

def average_fare_by_class(df):
    return df.groupby('Pclass')['Fare'].mean().round(2)

def median_age(df):
    return round(df['Age'].median(), 1)

def median_fare(df):
    return round(df['Fare'].median(), 2)

def alone_passengers(df):
    return len(df[(df['SibSp'] == 0) & (df['Parch'] == 0)])

def passengers_with_family(df):
    return len(df[(df['SibSp'] > 0) | (df['Parch'] > 0)])

def plot_survival_counts(df):
    plt.figure(figsize=(8,5))
    survival_counts = df['Survived'].value_counts().sort_index()
    survival_counts.index = ['Did not survive', 'Survived']
    sns.barplot(x=survival_counts.index, y=survival_counts.values)
    plt.title('Survival Counts of Titanic Passengers')
    plt.ylabel('Number of Passengers')
    plt.xlabel('Survival Status')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

# Additional comprehensive utility functions
def age_groups_analysis(df):
    """Analyze passengers by age groups"""
    age_groups = {
        'Children (0-12)': len(df[(df['Age'] >= 0) & (df['Age'] <= 12)]),
        'Teenagers (13-19)': len(df[(df['Age'] >= 13) & (df['Age'] <= 19)]),
        'Young Adults (20-35)': len(df[(df['Age'] >= 20) & (df['Age'] <= 35)]),
        'Middle-aged (36-55)': len(df[(df['Age'] >= 36) & (df['Age'] <= 55)]),
        'Seniors (56+)': len(df[df['Age'] >= 56]),
        'Unknown Age': df['Age'].isnull().sum()
    }
    return age_groups

def survival_by_age_group(df):
    """Survival rates by age groups"""
    age_groups = {
        'Children (0-17)': df[df['Age'] <= 17]['Survived'].mean() * 100,
        'Adults (18-64)': df[(df['Age'] >= 18) & (df['Age'] <= 64)]['Survived'].mean() * 100,
        'Seniors (65+)': df[df['Age'] >= 65]['Survived'].mean() * 100
    }
    return age_groups

def correlation_age_survival(df):
    """Correlation between age and survival"""
    correlation = df[['Age', 'Survived']].dropna().corr().iloc[0, 1]
    return round(correlation, 3)

def correlation_fare_survival(df):
    """Correlation between fare and survival"""
    correlation = df[['Fare', 'Survived']].dropna().corr().iloc[0, 1]
    return round(correlation, 3)

def correlation_class_survival(df):
    """Correlation between class and survival"""
    correlation = df[['Pclass', 'Survived']].corr().iloc[0, 1]
    return round(correlation, 3)

def average_age_by_class(df):
    """Average age by passenger class"""
    return df.groupby('Pclass')['Age'].mean().round(1)

def average_age_by_gender(df):
    """Average age by gender"""
    return df.groupby('Sex')['Age'].mean().round(1)

def survival_by_family_size(df):
    """Survival rates by family size"""
    df_copy = df.copy()
    df_copy['FamilySize'] = df_copy['SibSp'] + df_copy['Parch'] + 1
    return df_copy.groupby('FamilySize')['Survived'].mean() * 100

def most_common_ticket_fares(df):
    """Most common fare ranges"""
    fare_ranges = pd.cut(df['Fare'], bins=[0, 10, 20, 50, 100, 200, 600], labels=['$0-10', '$10-20', '$20-50', '$50-100', '$100-200', '$200+'])
    return fare_ranges.value_counts().sort_index()

def passengers_by_embarkation_and_class(df):
    """Cross-tabulation of embarkation port and class"""
    return pd.crosstab(df['Embarked'], df['Pclass'])

def gender_distribution_by_class(df):
    """Gender distribution within each class"""
    return df.groupby(['Pclass', 'Sex']).size().unstack()

def plot_age_groups(df):
    """Plot age group distribution"""
    age_groups = age_groups_analysis(df)
    plt.figure(figsize=(10,6))
    plt.bar(age_groups.keys(), age_groups.values())
    plt.title('Passenger Distribution by Age Groups')
    plt.ylabel('Number of Passengers')
    plt.xlabel('Age Group')
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def plot_survival_by_age_group(df):
    """Plot survival rates by age group"""
    survival_rates = survival_by_age_group(df)
    plt.figure(figsize=(8,5))
    plt.bar(survival_rates.keys(), survival_rates.values())
    plt.title('Survival Rates by Age Group')
    plt.ylabel('Survival Rate (%)')
    plt.xlabel('Age Group')
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def plot_family_size_survival(df):
    """Plot survival rates by family size"""
    survival_rates = survival_by_family_size(df)
    plt.figure(figsize=(10,6))
    plt.plot(survival_rates.index, survival_rates.values, marker='o')
    plt.title('Survival Rate by Family Size')
    plt.ylabel('Survival Rate (%)')
    plt.xlabel('Family Size (including passenger)')
    plt.grid(True, alpha=0.3)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

# Advanced analysis functions for complete dataset coverage

def extract_titles(df):
    """Extract titles from passenger names"""
    import re
    titles = []
    for name in df['Name']:
        # Extract title using regex
        match = re.search(r' ([A-Za-z]+)\.', name)
        if match:
            title = match.group(1)
            # Standardize some titles
            if title in ['Mlle', 'Ms']:
                title = 'Miss'
            elif title == 'Mme':
                title = 'Mrs'
            elif title in ['Dr', 'Rev', 'Major', 'Col', 'Capt']:
                title = 'Officer'
            elif title in ['Don', 'Sir', 'Lady', 'Countess', 'Jonkheer']:
                title = 'Noble'
            titles.append(title)
        else:
            titles.append('Unknown')
    return titles

def title_survival_analysis(df):
    """Analyze survival rates by title"""
    df_copy = df.copy()
    df_copy['Title'] = extract_titles(df)
    survival_by_title = df_copy.groupby('Title')['Survived'].mean() * 100
    count_by_title = df_copy.groupby('Title').size()
    result = pd.DataFrame({'Survival_Rate': survival_by_title, 'Count': count_by_title})
    # Fill NaN values with 0 for survival rate (in case some titles have no survival data)
    result['Survival_Rate'] = result['Survival_Rate'].fillna(0)
    return result

def extract_deck_info(df):
    """Extract deck information from cabin numbers"""
    decks = []
    for cabin in df['Cabin']:
        if pd.isna(cabin) or cabin == '':
            decks.append('Unknown')
        else:
            # Extract first letter (deck)
            deck = cabin[0]
            decks.append(deck)
    return decks

def deck_survival_analysis(df):
    """Analyze survival rates by deck"""
    df_copy = df.copy()
    df_copy['Deck'] = extract_deck_info(df)
    # Filter out Unknown decks for meaningful analysis
    known_decks = df_copy[df_copy['Deck'] != 'Unknown']
    survival_by_deck = known_decks.groupby('Deck')['Survived'].mean() * 100
    count_by_deck = known_decks.groupby('Deck').size()
    return pd.DataFrame({'Survival_Rate': survival_by_deck, 'Count': count_by_deck})

def ticket_prefix_analysis(df):
    """Analyze ticket prefixes"""
    prefixes = []
    for ticket in df['Ticket']:
        if pd.isna(ticket):
            prefixes.append('Unknown')
        else:
            # Split by space and take first part if it contains letters
            parts = str(ticket).split()
            if len(parts) > 1 and any(c.isalpha() for c in parts[0]):
                prefixes.append(parts[0])
            else:
                prefixes.append('Numeric')
    return prefixes

def ticket_prefix_survival(df):
    """Survival analysis by ticket prefix"""
    df_copy = df.copy()
    df_copy['Ticket_Prefix'] = ticket_prefix_analysis(df)
    survival_by_prefix = df_copy.groupby('Ticket_Prefix')['Survived'].mean() * 100
    count_by_prefix = df_copy.groupby('Ticket_Prefix').size()
    # Only show prefixes with reasonable sample size
    significant_prefixes = count_by_prefix[count_by_prefix >= 5]
    # Filter survival_by_prefix to only include significant prefixes
    significant_survival = survival_by_prefix[survival_by_prefix.index.isin(significant_prefixes.index)]
    return pd.DataFrame({
        'Survival_Rate': significant_survival,
        'Count': significant_prefixes
    })

def missing_data_analysis(df):
    """Analyze missing data patterns"""
    missing_info = df.isnull().sum()
    missing_percentage = (missing_info / len(df)) * 100
    return pd.DataFrame({
        'Missing_Count': missing_info,
        'Missing_Percentage': missing_percentage.round(2)
    })

def age_missing_by_class(df):
    """Analyze age missing patterns by class"""
    missing_by_class = df[df['Age'].isnull()].groupby('Pclass').size()
    total_by_class = df.groupby('Pclass').size()
    percentage_missing = (missing_by_class / total_by_class * 100).round(2)
    return pd.DataFrame({
        'Missing_Age_Count': missing_by_class,
        'Total_In_Class': total_by_class,
        'Missing_Percentage': percentage_missing
    })

def cabin_missing_by_class(df):
    """Analyze cabin missing patterns by class"""
    missing_by_class = df[df['Cabin'].isnull()].groupby('Pclass').size()
    total_by_class = df.groupby('Pclass').size()
    percentage_missing = (missing_by_class / total_by_class * 100).round(2)
    return pd.DataFrame({
        'Missing_Cabin_Count': missing_by_class,
        'Total_In_Class': total_by_class,
        'Missing_Percentage': percentage_missing
    })

def family_composition_analysis(df):
    """Detailed family composition analysis"""
    df_copy = df.copy()
    df_copy['FamilySize'] = df_copy['SibSp'] + df_copy['Parch'] + 1

    # Categorize family types
    conditions = [
        (df_copy['FamilySize'] == 1),
        (df_copy['SibSp'] > 0) & (df_copy['Parch'] == 0),  # Only siblings/spouse
        (df_copy['SibSp'] == 0) & (df_copy['Parch'] > 0),  # Only parents/children
        (df_copy['SibSp'] > 0) & (df_copy['Parch'] > 0),   # Both siblings and parents/children
    ]
    choices = ['Alone', 'Siblings/Spouse Only', 'Parents/Children Only', 'Complex Family']
    df_copy['Family_Type'] = pd.Categorical(np.select(conditions, choices, default='Alone'))

    return df_copy.groupby('Family_Type')['Survived'].agg(['mean', 'count'])

def passenger_id_patterns(df):
    """Analyze if PassengerId has any patterns (usually just sequential)"""
    return {
        'min_id': df['PassengerId'].min(),
        'max_id': df['PassengerId'].max(),
        'total_passengers': len(df),
        'is_sequential': df['PassengerId'].is_monotonic_increasing
    }

def comprehensive_statistics(df):
    """Generate comprehensive statistical summary"""
    stats = {}

    # Basic counts
    stats['total_passengers'] = len(df)
    stats['survived'] = df['Survived'].sum()
    stats['survival_rate'] = (stats['survived'] / stats['total_passengers']) * 100

    # Age statistics (excluding missing)
    age_data = df['Age'].dropna()
    stats['age_mean'] = age_data.mean()
    stats['age_median'] = age_data.median()
    stats['age_min'] = age_data.min()
    stats['age_max'] = age_data.max()

    # Fare statistics
    stats['fare_mean'] = df['Fare'].mean()
    stats['fare_median'] = df['Fare'].median()
    stats['fare_min'] = df['Fare'].min()
    stats['fare_max'] = df['Fare'].max()

    # Class distribution
    stats['class_distribution'] = df['Pclass'].value_counts().to_dict()

    # Gender distribution
    stats['gender_distribution'] = df['Sex'].value_counts().to_dict()

    # Port distribution
    port_dist = df['Embarked'].value_counts().to_dict()
    stats['port_distribution'] = {k: v for k, v in port_dist.items() if pd.notna(k)}

    return stats

def plot_title_survival(df):
    """Plot survival rates by title"""
    title_data = title_survival_analysis(df)
    plt.figure(figsize=(12,6))
    title_data = title_data.sort_values('Survival_Rate', ascending=False)
    plt.bar(title_data.index, title_data['Survival_Rate'])
    plt.title('Survival Rate by Passenger Title')
    plt.ylabel('Survival Rate (%)')
    plt.xlabel('Title')
    plt.xticks(rotation=45)
    # Add count labels
    for i, (idx, row) in enumerate(title_data.iterrows()):
        plt.text(i, row['Survival_Rate'] + 1, f'n={int(row["Count"])}', ha='center', va='bottom')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def plot_deck_survival(df):
    """Plot survival rates by deck"""
    deck_data = deck_survival_analysis(df)
    plt.figure(figsize=(10,6))
    deck_data = deck_data.sort_values('Survival_Rate', ascending=False)
    plt.bar(deck_data.index, deck_data['Survival_Rate'])
    plt.title('Survival Rate by Cabin Deck')
    plt.ylabel('Survival Rate (%)')
    plt.xlabel('Deck')
    # Add count labels
    for i, (idx, row) in enumerate(deck_data.iterrows()):
        plt.text(i, row['Survival_Rate'] + 1, f'n={int(row["Count"])}', ha='center', va='bottom')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def plot_missing_data(df):
    """Plot missing data patterns"""
    missing_data = missing_data_analysis(df)
    missing_data = missing_data[missing_data['Missing_Count'] > 0]

    plt.figure(figsize=(10,6))
    plt.bar(missing_data.index, missing_data['Missing_Percentage'])
    plt.title('Missing Data by Column')
    plt.ylabel('Missing Percentage (%)')
    plt.xlabel('Column')
    plt.xticks(rotation=45)
    # Add count labels
    for i, (idx, row) in enumerate(missing_data.iterrows()):
        plt.text(i, row['Missing_Percentage'] + 0.5, f'{int(row["Missing_Count"])}', ha='center', va='bottom')
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"