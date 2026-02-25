from fastapi import FastAPI
from pydantic import BaseModel

from .utils import (
    plot_age_histogram,
    get_percentage_male,
    average_fare,
    embarked_counts,
    plot_embarked_bar,
    survival_rate,
    survival_by_class,
    survival_by_gender,
    class_distribution,
    age_statistics,
    fare_statistics,
    family_size_distribution,
    plot_survival_by_class,
    plot_survival_by_gender,
    plot_class_distribution,
    plot_fare_distribution,
    youngest_passenger,
    oldest_passenger,
    children_count,
    males_survived,
    females_survived,
    average_fare_by_class,
    median_age,
    median_fare,
    alone_passengers,
    passengers_with_family,
    plot_survival_counts,
    # New comprehensive functions
    age_groups_analysis,
    survival_by_age_group,
    correlation_age_survival,
    correlation_fare_survival,
    correlation_class_survival,
    average_age_by_class,
    average_age_by_gender,
    survival_by_family_size,
    most_common_ticket_fares,
    passengers_by_embarkation_and_class,
    gender_distribution_by_class,
    plot_age_groups,
    plot_survival_by_age_group,
    plot_family_size_survival,
    # Advanced analysis functions
    extract_titles,
    title_survival_analysis,
    extract_deck_info,
    deck_survival_analysis,
    ticket_prefix_analysis,
    ticket_prefix_survival,
    missing_data_analysis,
    age_missing_by_class,
    cabin_missing_by_class,
    family_composition_analysis,
    passenger_id_patterns,
    comprehensive_statistics,
    plot_title_survival,
    plot_deck_survival,
    plot_missing_data
)
from .data_loader import load_titanic_data, preprocess

app = FastAPI()

# Load dataframe once
df = preprocess(load_titanic_data())

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    q = query.question.lower()
    print("Incoming Question:", q)

    # Age-related questions (must be ordered by specificity)
    # Average age by categories (most specific)
    if "average age" in q and "class" in q:
        avg_ages = average_age_by_class(df)
        return {"answer": f"Average age by passenger class:\n• Class 1: {avg_ages[1]} years\n• Class 2: {avg_ages[2]} years\n• Class 3: {avg_ages[3]} years"}
    elif "average age" in q and any(word in q for word in ["gender", "sex", "men", "women", "male", "female"]):
        avg_ages = average_age_by_gender(df)
        return {"answer": f"Average age by gender:\n• Male: {avg_ages['male']} years\n• Female: {avg_ages['female']} years"}
    # Age group analysis (specific)
    elif any(word in q for word in ["age group", "age groups", "age categories", "age distribution by group"]):
        age_groups = age_groups_analysis(df)
        img = plot_age_groups(df)
        response = "Passenger distribution by age groups:\n"
        for group, count in age_groups.items():
            response += f"• {group}: {count} passengers\n"
        return {"answer": response, "image": img}
    # Survival by age group (specific)
    elif "survival" in q and any(word in q for word in ["age group", "age groups", "by age"]):
        survival_rates = survival_by_age_group(df)
        img = plot_survival_by_age_group(df)
        response = "Survival rates by age group:\n"
        for group, rate in survival_rates.items():
            response += f"• {group}: {rate:.1f}%\n"
        return {"answer": response, "image": img}
    # Teenager/young adult specific questions
    elif any(word in q for word in ["teenager", "teenagers", "teen"]) and any(word in q for word in ["how many", "count", "number"]):
        teen_count = age_groups_analysis(df)['Teenagers (13-19)']
        return {"answer": f"There were {teen_count} teenagers (ages 13-19) on the Titanic."}
    elif any(word in q for word in ["young adult", "young adults"]) and any(word in q for word in ["how many", "count", "number"]):
        young_adult_count = age_groups_analysis(df)['Young Adults (20-35)']
        return {"answer": f"There were {young_adult_count} young adults (ages 20-35) on the Titanic."}
    # General age histogram
    elif "age" in q and any(word in q for word in ["histogram", "distribution", "chart", "plot", "show", "graph"]):
        img = plot_age_histogram(df)
        return {
            "answer": "Here's the age distribution histogram of Titanic passengers:",
            "image": img
        }
    # Fare average (moved up to avoid confusion with age statistics)
    elif any(word in q for word in ["fare", "ticket", "price", "cost"]) and any(word in q for word in ["average", "mean"]) and not "class" in q:
        ans = average_fare(df)
        return {"answer": f"The average ticket fare was ${ans}."}
    # Age statistics (general)
    elif "age" in q and any(word in q for word in ["statistics", "stats", "min", "max", "average", "mean", "median"]):
        stats = age_statistics(df)
        return {"answer": f"Age statistics for Titanic passengers:\n• Minimum: {stats['min']} years\n• Maximum: {stats['max']} years\n• Average: {stats['mean']} years\n• Median: {stats['median']} years"}
    # Youngest/oldest passengers
    elif any(word in q for word in ["youngest", "oldest"]) and "passenger" in q:
        youngest = youngest_passenger(df)
        oldest = oldest_passenger(df)
        if "youngest" in q:
            return {"answer": f"The youngest passenger was {youngest} years old."}
        elif "oldest" in q:
            return {"answer": f"The oldest passenger was {oldest} years old."}
        else:
            return {"answer": f"Age range: youngest passenger was {youngest} years old, oldest was {oldest} years old."}
    # Median age
    elif "median" in q and "age" in q:
        med = median_age(df)
        return {"answer": f"The median age of Titanic passengers was {med} years."}

    # Children questions
    elif any(word in q for word in ["children", "child", "kids", "kid"]) and any(word in q for word in ["how many", "count", "number"]):
        count = children_count(df)
        return {"answer": f"There were {count} children (under 18 years old) on the Titanic."}

    # Gender-related questions
    # Gender distribution by class (specific - must come first)
    elif "gender" in q and "class" in q and any(word in q for word in ["distribution", "breakdown"]):
        gender_by_class = gender_distribution_by_class(df)
        response = "Gender distribution by passenger class:\n\n"
        for class_num in [1, 2, 3]:
            if class_num in gender_by_class.index:
                male_count = gender_by_class.loc[class_num, 'male']
                female_count = gender_by_class.loc[class_num, 'female']
                total = male_count + female_count
                male_pct = (male_count / total * 100) if total > 0 else 0
                female_pct = (female_count / total * 100) if total > 0 else 0
                response += f"Class {class_num}:\n"
                response += f"• Male: {male_count} ({male_pct:.1f}%)\n"
                response += f"• Female: {female_count} ({female_pct:.1f}%)\n\n"
        return {"answer": response}
    # General gender questions
    elif any(word in q for word in ["percentage", "percent", "ratio"]) and "male" in q:
        ans = get_percentage_male(df)
        return {"answer": f"{ans}% of passengers were male."}
    elif any(word in q for word in ["percentage", "percent", "ratio"]) and "female" in q:
        female_pct = 100 - get_percentage_male(df)
        return {"answer": f"{female_pct}% of passengers were female."}
    elif "gender" in q and any(word in q for word in ["distribution", "breakdown", "count"]) and not "class" in q:
        male_pct = get_percentage_male(df)
        female_pct = 100 - male_pct
        return {"answer": f"Gender distribution:\n• Male: {male_pct}%\n• Female: {female_pct}%"}

    # Name/Title analysis questions
    elif any(word in q for word in ["title", "titles", "mr", "mrs", "miss", "master"]) and any(word in q for word in ["survival", "survived", "rate"]):
        title_data = title_survival_analysis(df)
        img = plot_title_survival(df)
        response = "Survival rates by passenger title:\n\n"
        for title, row in title_data.iterrows():
            response += f"• {title}: {row['Survival_Rate']:.1f}% ({int(row['Count'])} passengers)\n"
        return {"answer": response, "image": img}
    elif any(word in q for word in ["title", "titles"]) and any(word in q for word in ["distribution", "count", "how many"]):
        title_data = title_survival_analysis(df)
        response = "Passenger title distribution:\n"
        for title, row in title_data.iterrows():
            response += f"• {title}: {int(row['Count'])} passengers\n"
        return {"answer": response}

    # Cabin/Deck analysis questions
    elif any(word in q for word in ["cabin", "deck", "decks"]) and any(word in q for word in ["survival", "survived", "rate"]):
        deck_data = deck_survival_analysis(df)
        img = plot_deck_survival(df)
        response = "Survival rates by cabin deck:\n\n"
        for deck, row in deck_data.iterrows():
            response += f"• Deck {deck}: {row['Survival_Rate']:.1f}% ({int(row['Count'])} passengers)\n"
        response += f"\nNote: {df['Cabin'].isnull().sum()} passengers had unknown cabin information."
        return {"answer": response, "image": img}
    elif any(word in q for word in ["cabin", "deck"]) and any(word in q for word in ["distribution", "count"]):
        deck_data = deck_survival_analysis(df)
        response = "Cabin deck distribution (known cabins only):\n"
        for deck, row in deck_data.iterrows():
            response += f"• Deck {deck}: {int(row['Count'])} passengers\n"
        response += f"\nTotal known cabins: {deck_data['Count'].sum()}"
        return {"answer": response}

    # Ticket analysis questions
    elif any(word in q for word in ["ticket", "tickets"]) and any(word in q for word in ["prefix", "prefixes", "survival", "rate"]):
        ticket_data = ticket_prefix_survival(df)
        response = "Survival rates by ticket prefix (significant groups only):\n\n"
        for prefix, row in ticket_data.iterrows():
            response += f"• {prefix}: {row['Survival_Rate']:.1f}% ({int(row['Count'])} passengers)\n"
        return {"answer": response}
    elif any(word in q for word in ["ticket", "tickets"]) and any(word in q for word in ["prefix", "prefixes", "distribution"]):
        df_copy = df.copy()
        df_copy['Ticket_Prefix'] = ticket_prefix_analysis(df)
        prefix_counts = df_copy['Ticket_Prefix'].value_counts()
        response = "Ticket prefix distribution:\n"
        for prefix, count in prefix_counts.head(10).items():  # Top 10
            response += f"• {prefix}: {count} passengers\n"
        if len(prefix_counts) > 10:
            response += f"• ... and {len(prefix_counts) - 10} other prefixes"
        return {"answer": response}

    # Survival-related questions
    elif any(word in q for word in ["survival", "survived", "survivors"]) and any(word in q for word in ["rate", "percentage", "percent"]):
        if "class" in q or "pclass" in q:
            rates = survival_by_class(df)
            img = plot_survival_by_class(df)
            return {"answer": f"Survival rates by passenger class:\n• Class 1: {rates[1]:.1f}%\n• Class 2: {rates[2]:.1f}%\n• Class 3: {rates[3]:.1f}%", "image": img}
        elif "gender" in q or "sex" in q or "men" in q or "women" in q:
            rates = survival_by_gender(df)
            img = plot_survival_by_gender(df)
            return {"answer": f"Survival rates by gender:\n• Female: {rates['female']:.1f}%\n• Male: {rates['male']:.1f}%\n\nWomen had a significantly higher survival rate than men.", "image": img}
        elif "port" in q or "embarked" in q:
            # Calculate survival by port
            port_survival = df.groupby('Embarked')['Survived'].mean() * 100
            return {"answer": f"Survival rates by embarkation port:\n• Southampton (S): {port_survival.get('S', 0):.1f}%\n• Cherbourg (C): {port_survival.get('C', 0):.1f}%\n• Queenstown (Q): {port_survival.get('Q', 0):.1f}%"}
        else:
            print(f"Debug: df shape {df.shape}, Survived sum {df['Survived'].sum()}")
            rate = survival_rate(df)
            print(f"Debug: rate {rate}")
            return {"answer": f"Overall survival rate: {rate}% of passengers survived the Titanic disaster."}
    elif "how many" in q and "survived" in q:
        if "male" in q or "men" in q:
            count = males_survived(df)
            return {"answer": f"{count} males survived."}
        elif "female" in q or "women" in q:
            count = females_survived(df)
            return {"answer": f"{count} females survived."}
        else:
            survived_count = df['Survived'].sum()
            return {"answer": f"{survived_count} passengers survived out of {len(df)} total passengers."}
    elif "survival" in q and any(word in q for word in ["count", "counts", "bar chart", "chart"]):
        img = plot_survival_counts(df)
        survived_count = df['Survived'].sum()
        not_survived = len(df) - survived_count
        return {"answer": f"Survival counts:\n• Survived: {survived_count} passengers\n• Did not survive: {not_survived} passengers", "image": img}

    # Class-related questions
    elif any(word in q for word in ["class", "pclass"]) and any(word in q for word in ["distribution", "breakdown", "count"]):
        classes = class_distribution(df)
        img = plot_class_distribution(df)
        return {"answer": f"Passenger class distribution:\n• Class 1 (First): {classes[1]} passengers\n• Class 2 (Second): {classes[2]} passengers\n• Class 3 (Third): {classes[3]} passengers", "image": img}
    elif "how many" in q and any(word in q for word in ["first", "1st", "class 1"]):
        count = class_distribution(df)[1]
        return {"answer": f"{count} passengers were in first class."}
    elif "how many" in q and any(word in q for word in ["second", "2nd", "class 2"]):
        count = class_distribution(df)[2]
        return {"answer": f"{count} passengers were in second class."}
    elif "how many" in q and any(word in q for word in ["third", "3rd", "class 3"]):
        count = class_distribution(df)[3]
        return {"answer": f"{count} passengers were in third class."}
    elif "highest" in q and "survival" in q and "class" in q:
        rates = survival_by_class(df)
        highest_class = rates.idxmax()
        highest_rate = rates.max()
        return {"answer": f"Class {highest_class} had the highest survival rate at {highest_rate:.1f}%."}

    # Fare-related questions
    elif any(word in q for word in ["fare", "ticket", "price", "cost"]) and any(word in q for word in ["average", "mean"]):
        if "class" in q:
            fares = average_fare_by_class(df)
            return {"answer": f"Average fares by class:\n• Class 1: ${fares[1]}\n• Class 2: ${fares[2]}\n• Class 3: ${fares[3]}"}
        else:
            ans = average_fare(df)
            return {"answer": f"The average ticket fare was ${ans}."}
    elif any(word in q for word in ["fare", "ticket", "price", "cost"]) and any(word in q for word in ["statistics", "stats", "distribution"]):
        stats = fare_statistics(df)
        img = plot_fare_distribution(df)
        return {"answer": f"Fare statistics:\n• Minimum: ${stats['min']}\n• Maximum: ${stats['max']}\n• Average: ${stats['mean']}\n• Median: ${stats['median']}", "image": img}
    elif any(word in q for word in ["highest", "maximum", "max"]) and any(word in q for word in ["fare", "ticket"]):
        max_fare = fare_statistics(df)['max']
        return {"answer": f"The highest ticket fare was ${max_fare}."}
    elif any(word in q for word in ["lowest", "minimum", "min"]) and any(word in q for word in ["fare", "ticket"]):
        min_fare = fare_statistics(df)['min']
        return {"answer": f"The lowest ticket fare was ${min_fare}."}
    elif "median" in q and any(word in q for word in ["fare", "ticket"]):
        med = median_fare(df)
        return {"answer": f"The median ticket fare was ${med}."}

    # Embarkation questions
    # Cross-tabulation of embarkation and class (specific)
    elif any(word in q for word in ["embarkation", "port"]) and "class" in q:
        cross_tab = passengers_by_embarkation_and_class(df)
        response = "Passengers by embarkation port and class:\n\n"
        port_names = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
        for port in ['S', 'C', 'Q']:
            if port in cross_tab.index:
                response += f"{port_names[port]}:\n"
                for class_num in [1, 2, 3]:
                    if class_num in cross_tab.columns:
                        count = cross_tab.loc[port, class_num]
                        response += f"• Class {class_num}: {count} passengers\n"
                response += "\n"
        return {"answer": response}
    # General embarkation
    elif any(word in q for word in ["embarked", "embark", "port", "ports"]) and not "class" in q:
        counts = embarked_counts(df)
        img = plot_embarked_bar(df)
        return {"answer": f"Passengers embarked from each port:\n• Southampton (S): {counts.get('S', 0)} passengers\n• Cherbourg (C): {counts.get('C', 0)} passengers\n• Queenstown (Q): {counts.get('Q', 0)} passengers", "image": img}
    elif "southampton" in q or ("port" in q and "s" in q):
        count = embarked_counts(df).get('S', 0)
        return {"answer": f"{count} passengers embarked from Southampton."}
    elif "cherbourg" in q or ("port" in q and "c" in q):
        count = embarked_counts(df).get('C', 0)
        return {"answer": f"{count} passengers embarked from Cherbourg."}
    elif "queenstown" in q or ("port" in q and "q" in q):
        count = embarked_counts(df).get('Q', 0)
        return {"answer": f"{count} passengers embarked from Queenstown."}
    elif "most" in q and any(word in q for word in ["passengers", "embarked", "port"]):
        counts = embarked_counts(df)
        most_port = max(counts, key=counts.get)
        most_count = counts[most_port]
        port_names = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
        return {"answer": f"{port_names[most_port]} had the most passengers with {most_count} embarking from there."}

    # Family and travel alone questions
    # Family size and survival (specific - must come first)
    elif "family size" in q and "survival" in q:
        survival_rates = survival_by_family_size(df)
        img = plot_family_size_survival(df)
        response = "Survival rates by family size:\n"
        for size, rate in survival_rates.items():
            family_desc = f"{size} person{'s' if size > 1 else ''}"
            response += f"• {family_desc}: {rate:.1f}%\n"
        return {"answer": response, "image": img}
    # General family questions
    elif any(word in q for word in ["family", "sibling", "spouse", "parent", "child"]) and not "survival" in q:
        family_dist = family_size_distribution(df)
        return {"answer": f"Family size distribution:\n• Solo travelers: {family_dist.get(1, 0)} passengers\n• Small families (2-4): {sum(family_dist.get(i, 0) for i in range(2, 5))} passengers\n• Large families (5+): {sum(family_dist.get(i, 0) for i in range(5, family_dist.index.max() + 1))} passengers"}
    elif any(word in q for word in ["alone", "solo", "single"]) and any(word in q for word in ["travel", "traveled", "passengers"]):
        alone = alone_passengers(df)
        return {"answer": f"{alone} passengers traveled alone (no siblings, spouses, parents, or children)."}
    elif "with family" in q or "had family" in q:
        with_family = passengers_with_family(df)
        return {"answer": f"{with_family} passengers traveled with family members."}

    # Age group analysis questions
    elif any(word in q for word in ["age group", "age groups", "age categories", "age distribution by group"]):
        age_groups = age_groups_analysis(df)
        img = plot_age_groups(df)
        response = "Passenger distribution by age groups:\n"
        for group, count in age_groups.items():
            response += f"• {group}: {count} passengers\n"
        return {"answer": response, "image": img}
    elif "survival" in q and any(word in q for word in ["age group", "age groups", "by age"]):
        survival_rates = survival_by_age_group(df)
        img = plot_survival_by_age_group(df)
        response = "Survival rates by age group:\n"
        for group, rate in survival_rates.items():
            response += f"• {group}: {rate:.1f}%\n"
        return {"answer": response, "image": img}

    # Correlation questions
    elif any(word in q for word in ["correlation", "relationship", "correlation between"]) and "age" in q and "survival" in q:
        corr = correlation_age_survival(df)
        direction = "positive" if corr > 0 else "negative"
        strength = "weak" if abs(corr) < 0.3 else "moderate" if abs(corr) < 0.7 else "strong"
        return {"answer": f"The correlation between age and survival is {corr} ({strength} {direction} correlation). This suggests that {'older passengers had slightly lower survival rates' if corr < 0 else 'older passengers had slightly higher survival rates'}."}
    elif any(word in q for word in ["correlation", "relationship"]) and "fare" in q and "survival" in q:
        corr = correlation_fare_survival(df)
        return {"answer": f"The correlation between ticket fare and survival is {corr}. This indicates that passengers who paid higher fares had {'higher' if corr > 0 else 'lower'} survival rates."}
    elif any(word in q for word in ["correlation", "relationship"]) and "class" in q and "survival" in q:
        corr = correlation_class_survival(df)
        return {"answer": f"There is a {corr} correlation between passenger class and survival. Higher class passengers (lower numbers) had significantly higher survival rates."}
    elif any(word in q for word in ["affect", "impact", "influence"]) and "class" in q and "survival" in q:
        corr = correlation_class_survival(df)
        return {"answer": f"Passenger class significantly affected survival rates. There is a {corr} correlation, meaning higher class passengers had much higher survival rates."}

    # Average age by categories (must come before general age statistics)
    elif "average age" in q and "class" in q:
        avg_ages = average_age_by_class(df)
        return {"answer": f"Average age by passenger class:\n• Class 1: {avg_ages[1]} years\n• Class 2: {avg_ages[2]} years\n• Class 3: {avg_ages[3]} years"}
    elif "average age" in q and any(word in q for word in ["gender", "sex", "men", "women", "male", "female"]):
        avg_ages = average_age_by_gender(df)
        return {"answer": f"Average age by gender:\n• Male: {avg_ages['male']} years\n• Female: {avg_ages['female']} years"}

    # Family size and survival
    elif "family size" in q and "survival" in q:
        survival_rates = survival_by_family_size(df)
        img = plot_family_size_survival(df)
        response = "Survival rates by family size:\n"
        for size, rate in survival_rates.items():
            family_desc = f"{size} person{'s' if size > 1 else ''}"
            response += f"• {family_desc}: {rate:.1f}%\n"
        return {"answer": response, "image": img}

    # Missing data analysis questions
    elif any(word in q for word in ["missing", "null", "nan", "empty"]) and any(word in q for word in ["data", "values", "information"]):
        missing_data = missing_data_analysis(df)
        img = plot_missing_data(df)
        response = "Missing data analysis:\n\n"
        for col, row in missing_data.iterrows():
            if row['Missing_Count'] > 0:
                response += f"• {col}: {int(row['Missing_Count'])} missing ({row['Missing_Percentage']:.1f}%)\n"
        return {"answer": response, "image": img}
    elif any(word in q for word in ["missing", "unknown"]) and "age" in q:
        missing_age = age_missing_by_class(df)
        response = "Missing age data by passenger class:\n\n"
        for class_num, row in missing_age.iterrows():
            response += f"• Class {class_num}: {int(row['Missing_Age_Count'])} missing ages ({row['Missing_Percentage']:.1f}% of class)\n"
        return {"answer": response}
    elif any(word in q for word in ["missing", "unknown"]) and any(word in q for word in ["cabin", "cabins"]):
        missing_cabin = cabin_missing_by_class(df)
        response = "Missing cabin data by passenger class:\n\n"
        for class_num, row in missing_cabin.iterrows():
            response += f"• Class {class_num}: {int(row['Missing_Cabin_Count'])} missing cabins ({row['Missing_Percentage']:.1f}% of class)\n"
        return {"answer": response}

    # Family composition analysis
    elif any(word in q for word in ["family composition", "family type", "family types"]):
        family_comp = family_composition_analysis(df)
        response = "Family composition analysis:\n\n"
        for family_type, stats in family_comp.iterrows():
            surv_rate = stats['mean'] * 100
            count = int(stats['count'])
            response += f"• {family_type}: {count} passengers, {surv_rate:.1f}% survival rate\n"
        return {"answer": response}

    # Passenger ID analysis (usually just sequential)
    elif any(word in q for word in ["passenger id", "passengerid", "id"]) and any(word in q for word in ["pattern", "analysis", "range"]):
        id_patterns = passenger_id_patterns(df)
        response = f"Passenger ID analysis:\n\n"
        response += f"• Range: {id_patterns['min_id']} to {id_patterns['max_id']}\n"
        response += f"• Total passengers: {id_patterns['total_passengers']}\n"
        response += f"• Sequential: {'Yes' if id_patterns['is_sequential'] else 'No'}\n"
        response += f"\nPassenger IDs are typically just sequential identifiers with no special meaning."
        return {"answer": response}

    # Comprehensive overview
    elif any(word in q for word in ["comprehensive", "complete", "full"]) and any(word in q for word in ["overview", "summary", "statistics", "stats"]):
        stats = comprehensive_statistics(df)
        response = f"🎯 **COMPREHENSIVE TITANIC DATASET STATISTICS**\n\n"
        response += f"📊 **Basic Counts:**\n"
        response += f"• Total Passengers: {stats['total_passengers']}\n"
        response += f"• Survived: {stats['survived']} ({stats['survival_rate']:.1f}%)\n\n"

        response += f"🎂 **Age Statistics:**\n"
        response += f"• Mean: {stats['age_mean']:.1f} years\n"
        response += f"• Median: {stats['age_median']:.1f} years\n"
        response += f"• Range: {stats['age_min']:.1f} - {stats['age_max']:.1f} years\n\n"

        response += f"💰 **Fare Statistics:**\n"
        response += f"• Mean: ${stats['fare_mean']:.2f}\n"
        response += f"• Median: ${stats['fare_median']:.2f}\n"
        response += f"• Range: ${stats['fare_min']:.2f} - ${stats['fare_max']:.2f}\n\n"

        response += f"🏷️ **Class Distribution:**\n"
        for class_num, count in stats['class_distribution'].items():
            response += f"• Class {class_num}: {count} passengers\n\n"

        response += f"👥 **Gender Distribution:**\n"
        for gender, count in stats['gender_distribution'].items():
            response += f"• {gender.capitalize()}: {count} passengers\n\n"

        response += f"🚢 **Port Distribution:**\n"
        port_names = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
        for port, count in stats['port_distribution'].items():
            response += f"• {port_names.get(port, port)}: {count} passengers\n"

        return {"answer": response}

    # Fare range analysis
    elif any(word in q for word in ["fare range", "fare ranges", "ticket price range", "most common fares"]):
        fare_ranges = most_common_ticket_fares(df)
        response = "Most common fare ranges:\n"
        for range_name, count in fare_ranges.items():
            response += f"• {range_name}: {count} passengers\n"
        return {"answer": response}

    # General statistics and overview
    elif any(word in q for word in ["total", "how many", "count", "number"]) and "passengers" in q:
        return {"answer": f"There were {len(df)} passengers in the Titanic dataset."}

    # Dataset overview
    elif any(word in q for word in ["overview", "summary", "dataset overview", "complete overview"]):
        print(f"Debug: Matched overview condition for question: {q}")
        survival = survival_rate(df)
        male_pct = get_percentage_male(df)
        avg_age = age_statistics(df)['mean']
        avg_fare = average_fare(df)
        return {"answer": f"Titanic Dataset Overview: Total Passengers: {len(df)}, Survival Rate: {survival}%, Male Passengers: {male_pct}%, Average Age: {avg_age} years, Average Fare: ${avg_fare}"}

    # Default → comprehensive help
    return {"answer": "I can help you explore the Titanic dataset! Ask me questions about survival rates, demographics, fares, and more."}