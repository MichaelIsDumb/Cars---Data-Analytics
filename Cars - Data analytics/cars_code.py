import pandas as pd
import matplotlib.pyplot as plt
from random import randint

cars_df = pd.read_csv("cars_data.csv")
print(cars_df.info())

#Shortening brands' names
cars_df["Make"] = cars_df["Make"].replace({
    "Mercedes-Benz": "Mercedes",
    "Land Rover": "Land.R",
    "Maruti Suzuki": "Suzuki",
    "Lamborghini": "Lambo"
})

#Creating new columns
def featuring_engine(engine):
    try:
        return int(engine.split()[0])
    except Exception as e:
        print("Error:", e)
cars_df["Engine_new"] = cars_df["Engine"].apply(featuring_engine)

def split_columns(df):
    a = df["Max Power"].str.split(expand = True)[0]
    b = df["Max Power"].str.split(expand = True)[3]
    c = df["Max Torque"].str.split(expand = True)[0]
    d = df["Max Torque"].str.split(expand = True)[3]
    df["BHP"] = pd.to_numeric(a, errors = 'coerce')
    df["RPM_power"] = pd.to_numeric(b, errors = 'coerce')
    df["NM"] = pd.to_numeric(c, errors = 'coerce')
    df["RPM_torque"] = pd.to_numeric(d, errors = 'coerce')
    product = (df["Length"]*df["Width"]*df["Height"])/1000000000
    df["Volume"] = pd.to_numeric(product, errors = 'coerce')
    total = df["RPM_power"] + df["RPM_torque"]
    df["Total_RPM"] = pd.to_numeric(total, errors = 'coerce')
    return df

cars_df = split_columns(cars_df)

#Filling missing values for each column
cars_df["Engine_new"].fillna(round(cars_df["Engine_new"].mean()), inplace = True)
cars_df["Seating Capacity"].fillna(round(cars_df["Seating Capacity"].mean()), inplace = True)
cars_df["Fuel Tank Capacity"].fillna(round(cars_df["Fuel Tank Capacity"].mean()), inplace = True)
cars_df["BHP"].fillna(round(cars_df["BHP"].mean()), inplace = True)
cars_df["NM"].fillna(round(cars_df["NM"].mean()), inplace = True)
cars_df["RPM_power"].fillna(round(cars_df["RPM_power"].mean()), inplace = True)
cars_df["RPM_torque"].fillna(round(cars_df["RPM_torque"].mean()), inplace = True)
cars_df["Length"].fillna(round(cars_df["Length"].mean()), inplace = True)
cars_df["Width"].fillna(round(cars_df["Width"].mean()), inplace = True)
cars_df["Height"].fillna(round(cars_df["Height"].mean()), inplace = True)

drivetrain_list = ['FWD', 'RWD', 'AWD']

for i in range(136):
    random_number = randint(0, 2)
    cars_df["Drivetrain"].fillna(drivetrain_list[random_number], inplace = True)

#Checking the result of cleaning
print(cars_df.info())
print(cars_df.head())
print("Missing value:", cars_df.isnull().sum())

#A table of basic statistics for each car brand
car_brand_table = cars_df.groupby("Make").agg(
    Avg_price = ("Price", "mean"),
    Max_price = ("Price", "max"),
    Min_price = ("Price", "min"),
    Avg_consumption = ("Kilometer", "mean"),
    Avg_fuel_capacity = ("Fuel Tank Capacity", "mean"),
    Avg_bhp = ("BHP", "mean"),
    Avg_RPMpower = ("RPM_power", "mean"),
    Avg_NM = ("NM", "mean"),
    Avg_RPMtorque = ("RPM_torque", "mean")
)
print(car_brand_table)

#Data analysis

#Total amount of cars being sold each year
fig, axs = plt.subplots(2, 3, figsize = (13, 8))
axs[0, 0].hist(cars_df["Year"], bins = 20, color = "darkblue")
axs[0, 0].set_title("Amount of Cars Sold Each Year")
axs[0, 0].set_xlabel("Year")
axs[0, 0].set_ylabel("Amount Sold")

#Average price of each year sold
avg_price_per_year = cars_df.groupby(by = "Year")["Price"].mean()
axs[0, 1].bar(cars_df["Year"].unique(), avg_price_per_year, color = "orange")
axs[0, 1].set_title("Average Price Each Year")
axs[0, 1].set_xlabel("Year")
axs[0, 1].set_ylabel("Average Price")

#Correlation between engine and price
avg_price_over_engine = cars_df[(cars_df["Engine_new"] >= 2000) & (cars_df["Engine_new"] <= 6000)].groupby(by = "Engine_new")["Price"].mean()
axs[0, 2].scatter(avg_price_over_engine.index, avg_price_over_engine, color = "black")
axs[0, 2].set_title("Relationship of Engine and Price")
axs[0, 2].set_xlabel("Engine (cc)")
axs[0, 2].set_ylabel("Average Price")

#Top 10 brands with most sales in year 2020
recent_year_sales = cars_df[cars_df["Year"] == 2020].groupby(by = "Make").size()
recent_year_sales = recent_year_sales.sort_values(ascending = False).head(10)
axs[1, 0].pie(recent_year_sales, labels = recent_year_sales.index, autopct = "%1.1f%%")
axs[1, 0].set_title("Sales chart of Brands in 2020")

#Finding the frequencies of unique ratios of volume per seat
axs[1, 1].hist(cars_df["Volume"]/cars_df["Seating Capacity"], color = "green")
axs[1, 1].set_title("Ratio of Volume over Seating Capacity")
axs[1, 1].set_xlabel("Ratio (volume m3 per seat)")
axs[1, 1].set_ylabel("Frequencies")

#Finding top 5 car brands with highest total RPM and price above average
expensive_car = cars_df[cars_df["Price"] > cars_df["Price"].mean()].groupby(by = "Make")["Total_RPM"].mean()
top_5 = expensive_car.sort_values(ascending = False).head(5)
top_5_rpm = expensive_car[top_5.index]
axs[1, 2].bar(top_5.index, top_5_rpm, color = "purple")
axs[1, 2].set_title("Total RPM of Expensive Brands")
axs[1, 2].set_xlabel("Car brands")
axs[1, 2].set_ylabel("Total RPM (torque + power)")

plt.tight_layout()
plt.show()