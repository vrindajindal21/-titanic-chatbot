from fastapi import FastAPI
from pydantic import BaseModel
import re

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
    correlation_age_class,
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
    plot_missing_data,
    # Newly added
    find_passengers_by_name,
    get_passenger_by_id,
    column_total,
    correlation_age_fare
)
from .data_loader import load_titanic_data, preprocess

app = FastAPI()

# Load dataframe once
df = preprocess(load_titanic_data())

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    try:
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
        
        # Survival by age group (specific)
        elif "survival" in q and any(word in q for word in ["age group", "age groups", "by age"]):
            survival_rates = survival_by_age_group(df)
            img = plot_survival_by_age_group(df)
            response = "Survival rates by age group:\n"
            for group, rate in survival_rates.items():
                response += f"• {group}: {rate:.1f}%\n"
            return {"answer": response, "image": img}
        
        # Age group analysis (specific)
        elif any(word in q for word in ["age group", "age groups", "age categories", "age distribution by group"]):
            age_groups = age_groups_analysis(df)
            img = plot_age_groups(df)
            response = "Passenger distribution by age groups:\n"
            for group, count in age_groups.items():
                response += f"• {group}: {count} passengers\n"
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
        elif "age" in q and any(word in q for word in ["statistics", "stats", "min", "minimum", "lowest", "max", "maximum", "highest", "average", "mean", "median"]) and not any(word in q for word in ["all", "everything"]):
            stats = age_statistics(df)
            return {"answer": f"Age statistics for Titanic passengers:\n• Minimum: {stats['min']} years\n• Maximum: {stats['max']} years\n• Average: {stats['mean']} years\n• Median: {stats['median']} years"}
        # Youngest/oldest passengers
        elif any(word in q for word in ["youngest", "oldest", "lowest age", "highest age"]) and not any(word in q for word in ["all", "everything"]):
            y_info = youngest_passenger(df)
            o_info = oldest_passenger(df)
            if "youngest" in q or "lowest age" in q:
                names = ", ".join(y_info['names'])
                return {"answer": f"The youngest passenger(s) was {y_info['age']} years old: {names}"}
            elif "oldest" in q or "highest age" in q:
                names = ", ".join(o_info['names'])
                return {"answer": f"The oldest passenger(s) was {o_info['age']} years old: {names}"}
            else:
                y_names = ", ".join(y_info['names'])
                o_names = ", ".join(o_info['names'])
                return {"answer": f"Age range:\n• Youngest ({y_info['age']} years): {y_names}\n• Oldest ({o_info['age']} years): {o_names}"}
        # Median age
        elif "median" in q and "age" in q:
            med = median_age(df)
            return {"answer": f"The median age of Titanic passengers was {med} years."}

        # Children questions
        elif any(word in q for word in ["children", "child", "kids", "kid", "minor", "minors"]) and any(word in q for word in ["how many", "count", "number", "total"]):
            count = children_count(df)
            return {"answer": f"There were {count} children (under 18 years old) on the Titanic."}

        # Gender-related questions
        # Gender distribution by class (specific - must come first)
        elif "gender" in q and "class" in q and any(word in q for word in ["distribution", "breakdown"]):
            gender_by_class = gender_distribution_by_class(df)
            lines = ["Gender distribution by passenger class:\n\n"]
            for class_num in [1, 2, 3]:
                if class_num in gender_by_class.index:
                    male_count = gender_by_class.loc[class_num, 'male']
                    female_count = gender_by_class.loc[class_num, 'female']
                    total_in_class = male_count + female_count
                    if total_in_class > 0:
                        male_pct = (male_count / total_in_class * 100)
                        female_pct = (female_count / total_in_class * 100)
                        lines.append(f"Class {class_num}:\n")
                        lines.append(f"• Male: {male_count} ({male_pct:.1f}%)\n")
                        lines.append(f"• Female: {female_count} ({female_pct:.1f}%)\n\n")
            return {"answer": "".join(lines)}
        
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
                response = response + f"• {title}: {row['Survival_Rate']:.1f}% ({int(row['Count'])} passengers)\n"
            return {"answer": response, "image": img}
        elif any(word in q for word in ["title", "titles"]) and any(word in q for word in ["distribution", "count", "how many"]):
            title_data = title_survival_analysis(df)
            response = "Passenger title distribution:\n"
            for title, row in title_data.iterrows():
                response = response + f"• {title}: {int(row['Count'])} passengers\n"
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
        
        # Ticket analysis questions
        elif any(word in q for word in ["ticket", "tickets"]) and any(word in q for word in ["prefix", "prefixes", "survival", "rate"]):
            ticket_data = ticket_prefix_survival(df)
            response = "Survival rates by ticket prefix (significant groups only):\n\n"
            for prefix, row in ticket_data.iterrows():
                response += f"• {prefix}: {row['Survival_Rate']:.1f}% ({int(row['Count'])} passengers)\n"
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
                port_survival = df.groupby('Embarked')['Survived'].mean() * 100
                return {"answer": f"Survival rates by embarkation port:\n• Southampton (S): {port_survival.get('S', 0):.1f}%\n• Cherbourg (C): {port_survival.get('C', 0):.1f}%\n• Queenstown (Q): {port_survival.get('Q', 0):.1f}%"}
            else:
                rate = survival_rate(df)
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

        # Class-related questions
        elif any(word in q for word in ["class", "pclass"]) and any(word in q for word in ["distribution", "breakdown", "count"]):
            classes = class_distribution(df)
            img = plot_class_distribution(df)
            return {"answer": f"Passenger class distribution:\n• Class 1 (First): {classes[1]} passengers\n• Class 2 (Second): {classes[2]} passengers\n• Class 3 (Third): {classes[3]} passengers", "image": img}
        
        # Fare-related questions
        elif any(word in q for word in ["fare", "ticket", "price", "cost"]) and any(word in q for word in ["average", "mean"]):
            if "class" in q:
                fares = average_fare_by_class(df)
                return {"answer": f"Average fares by class:\n• Class 1: ${fares[1]}\n• Class 2: ${fares[2]}\n• Class 3: ${fares[3]}"}
            else:
                ans = average_fare(df)
                return {"answer": f"The average ticket fare was ${ans}."}
        
        # Embarkation questions
        elif any(word in q for word in ["embarkation", "port", "departed", "departure"]) and ("class" in q or "pclass" in q):
            cross_tab = passengers_by_embarkation_and_class(df)
            lines = ["Passengers by embarkation port and class:\n\n"]
            port_names = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
            for port in ['S', 'C', 'Q']:
                if port in cross_tab.index:
                    lines.append(f"{port_names[port]}:\n")
                    for class_num in [1, 2, 3]:
                        if class_num in cross_tab.columns:
                            count = cross_tab.loc[port, class_num]
                            lines.append(f"• Class {class_num}: {count} passengers\n")
                    lines.append("\n")
            return {"answer": "".join(lines)}
        
        elif any(word in q for word in ["embarked", "embark", "port", "ports", "departed", "departure"]):
            counts = embarked_counts(df)
            img = plot_embarked_bar(df)
            return {"answer": f"Passengers embarked from each port:\n• Southampton (S): {counts.get('S', 0)} passengers\n• Cherbourg (C): {counts.get('C', 0)} passengers\n• Queenstown (Q): {counts.get('Q', 0)} passengers", "image": img}

        # Family and travel alone questions
        elif "family size" in q and "survival" in q:
            survival_rates = survival_by_family_size(df)
            img = plot_family_size_survival(df)
            response = "Survival rates by family size:\n"
            for size, rate in survival_rates.items():
                family_desc = f"{size} person{'s' if size > 1 else ''}"
                response += f"• {family_desc}: {rate:.1f}%\n"
            return {"answer": response, "image": img}

        # Correlation questions
        elif any(word in q for word in ["correlation", "relationship", "correlation between"]):
            if "age" in q and "survival" in q:
                corr = correlation_age_survival(df)
                return {"answer": f"The correlation between age and survival is {corr}."}
            elif ("fare" in q or "price" in q or "cost" in q) and "survival" in q:
                corr = correlation_fare_survival(df)
                return {"answer": f"The correlation between ticket fare and survival is {corr}."}
            elif ("class" in q or "pclass" in q) and "survival" in q:
                corr = correlation_class_survival(df)
                return {"answer": f"There is a {corr} correlation between passenger class and survival."}
            elif "age" in q and ("class" in q or "pclass" in q):
                corr = correlation_age_class(df)
                return {"answer": f"The correlation between age and passenger class is {corr}."}
            elif "age" in q and ("fare" in q or "price" in q or "cost" in q):
                corr = correlation_age_fare(df)
                return {"answer": f"The correlation between age and ticket fare is {corr}."}
            else:
                return {"answer": "I can calculate correlations between age, fare, class, and survival. Which ones would you like to see?"}

        # Missing data analysis questions
        elif any(word in q for word in ["missing", "null", "nan", "empty"]) and any(word in q for word in ["data", "values", "information"]):
            missing_data = missing_data_analysis(df)
            img = plot_missing_data(df)
            response_lines = ["Missing data analysis:\n\n"]
            for col, row in missing_data.iterrows():
                if row['Missing_Count'] > 0:
                    response_lines.append(f"• {col}: {int(row['Missing_Count'])} missing ({row['Missing_Percentage']:.1f}%)\n")
            return {"answer": "".join(response_lines), "image": img}

        # Passenger Search by ID
        elif "passenger" in q and any(char.isdigit() for char in q):
            ids = re.findall(r'\d+', q)
            if ids:
                p_id = ids[0]
                passenger = get_passenger_by_id(df, p_id)
                if not passenger.empty:
                    row = passenger.iloc[0]
                    res = f"**Passenger Details (ID: {p_id})**\n"
                    res = res + f"• Name: {row['Name']}\n"
                    res = res + f"• Age: {row['Age']}\n"
                    res = res + f"• Sex: {row['Sex']}\n"
                    res = res + f"• Class: {row['Pclass']}\n"
                    res = res + f"• Survived: {('Yes' if row['Survived'] == 1 else 'No')}\n"
                    res = res + f"• Fare: ${row['Fare']}\n"
                    res = res + f"• Port: {row['Embarked']}\n"
                    return {"answer": res}
                else:
                    return {"answer": f"Sorry, no passenger was found with ID {p_id}."}

        # Passenger Search by Name
        elif any(word in q for word in ["who is", "search for", "find passenger", "was there a passenger named", "details for", "about passenger"]):
            name_to_find = q
            for trigger in ["who is", "search for", "find passenger", "was there a passenger named", "details for", "about passenger"]:
                if trigger in q:
                    parts = q.split(trigger)
                    if len(parts) > 1:
                        name_to_find = parts[1].strip()
                    break
            
            if len(name_to_find) > 2:
                results = find_passengers_by_name(df, name_to_find)
                if not results.empty:
                    count = len(results)
                    res = f"Found {count} passenger(s) matching '{name_to_find}':\n\n"
                    for _, row in results.head(5).iterrows():
                        res = res + f"• **{row['Name']}** (ID: {row['PassengerId']})\n"
                        res = res + f"  - Age: {row['Age']}, Sex: {row['Sex']}, Class: {row['Pclass']}, Survived: {('Yes' if row['Survived'] == 1 else 'No')}\n"
                    if count > 5:
                        res = res + f"\n...and {count - 5} more."
                    return {"answer": res}
                else:
                    return {"answer": f"I couldn't find any passengers named '{name_to_find}'."}

        # Column Totals
        elif "total" in q or "sum of" in q:
            if "fare" in q or "price" in q or "cost" in q:
                total = column_total(df, 'Fare')
                if total is not None:
                    return {"answer": f"The total amount paid in fares by all passengers was ${total:,.2f}."}
            elif "age" in q:
                total = column_total(df, 'Age')
                if total is not None:
                    return {"answer": f"The sum of all passenger ages is {total:,.0f} years."}
            elif "siblings" in q or "spouses" in q or "sibsp" in q:
                total = column_total(df, 'SibSp')
                if total is not None:
                    return {"answer": f"Total number of siblings/spouses on board: {total}."}
            elif "parents" in q or "children" in q or "parch" in q:
                total = column_total(df, 'Parch')
                if total is not None:
                    return {"answer": f"Total number of parents/children on board: {total}."}
            
            return {"answer": "I couldn't calculate that total. Make sure you are asking about a valid numeric column like age, fare, siblings, or parents."}

        # Comprehensive overview
        elif any(word in q for word in ["comprehensive", "complete", "full", "all", "everything"]) and any(word in q for word in ["overview", "summary", "statistics", "stats", "data", "info", "about"]):
            stats = comprehensive_statistics(df)
            response = f"🎯 **COMPREHENSIVE TITANIC STATISTICS**\n\n"
            response += f"📊 **Basic Counts:**\n"
            response += f"• Total Passengers: {stats['total_passengers']}\n"
            response += f"• Survived: {stats['survived']} ({stats['survival_rate']:.1f}%)\n\n"
            
            y_names = ", ".join(stats['youngest_names'][:3]) + ("..." if len(stats['youngest_names']) > 3 else "")
            o_names = ", ".join(stats['oldest_names'][:3]) + ("..." if len(stats['oldest_names']) > 3 else "")
            
            response += f"🎂 **Age:** Mean {stats['age_mean']:.1f}, Median {stats['age_median']:.1f}\n"
            response += f"• Youngest: {stats['age_min']} years ({y_names})\n"
            response += f"• Oldest: {stats['age_max']} years ({o_names})\n\n"
            
            response += f"💰 **Fare:** Mean ${stats['fare_mean']:.2f}, Median ${stats['fare_median']:.2f}\n"
            return {"answer": response}

        # Dataset overview (general fallback for 'tell me about' etc)
        elif any(word in q for word in ["overview", "summary", "tell me about", "all statistics", "everything about"]):
            survival = survival_rate(df)
            male_pct = get_percentage_male(df)
            avg_age = age_statistics(df)['mean']
            avg_fare = average_fare(df)
            return {"answer": f"Titanic Dataset Overview:\n• Total Passengers: {len(df)}\n• Survival Rate: {survival}%\n• Male/Female: {male_pct}% / {round(100-male_pct, 2)}%\n• Average Age: {avg_age} years\n• Average Fare: ${avg_fare}"}

        # Default help
        return {"answer": "I can help you explore the Titanic dataset! Ask me about survival rates, passenger classes, demographics, or search for specific passengers."}

    except Exception as e:
        print(f"Error processing question: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"answer": "I encountered an error while processing your question. Please try rephrasing it!"}