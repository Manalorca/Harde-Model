import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

initial_year=1880
final_year=2016

en0=93.3 #ppm/yr
taur0=3 #yr 
be=10 #ppm/yr/°C
btau=0.37 #yr/°C
C0=290 #ppm

# Read the CSV file into a DataFrame
df = pd.read_csv('C:\\Users\\matth\\Desktop\\Tout\\Dossier\\Changement climatique\\mean_temperature.csv',sep=',')


# Read the CSV file into a DataFrame
df2 = pd.read_csv("C:\\Users\\matth\\Desktop\\Tout\\Dossier\\Changement climatique\\owid-co2-data.csv")

# Filter the data for the country 'World'
world_co2_emissions = df2[df2['country'] == 'World']

# Create a dictionary with years as keys and 'co2' emissions as values
co2_emissions_dict = dict(zip(world_co2_emissions['year'], world_co2_emissions['co2']))



co2_emission=[]
for t in range(final_year-initial_year):
    co2_emission.append(co2_emissions_dict[initial_year+t]/(2.12*1000))

# Create an empty dictionary to store the temperature values
temperature_dict = {}

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    year = row['Year']
    mean = row['Mean']
    temperature_dict[year] = mean


for t in range(initial_year,final_year+1):
    temperature_dict[t]=temperature_dict[t]+0.35

# Create a new dictionary for smoothed temperature data
smoothed_temperature_dict = {}

# Set the window size for the moving average
window_size = 5

# Iterate through the years
for year in range(initial_year,initial_year+window_size+1):
    # Calculate the moving average for the current year
    moving_average = sum(temperature_dict.get(year - i, 0) for i in range(year-initial_year+1))
    moving_average += sum(temperature_dict.get(year + i, 0) for i in range(1,window_size+1))
    moving_average /= (window_size+year-initial_year+1)
    
    # Update the smoothed_temperature_dict
    smoothed_temperature_dict[year] = moving_average

for year in range(final_year-window_size,final_year+1):
    # Calculate the moving average for the current year
    moving_average = sum(temperature_dict.get(year - i, 0) for i in range(window_size+1))
    moving_average += sum(temperature_dict.get(year + i, 0) for i in range(1,final_year-year+1))
    moving_average /= (window_size+final_year-year+1)
    
    # Update the smoothed_temperature_dict
    smoothed_temperature_dict[year] = moving_average

for year in range(initial_year+window_size+1, final_year-window_size):
    # Calculate the moving average for the current year
    moving_average = sum(temperature_dict.get(year - i, 0) for i in range(window_size+1))
    moving_average += sum(temperature_dict.get(year + i, 0) for i in range(1,window_size+1))
    moving_average /= (2*window_size+1)
    
    # Update the smoothed_temperature_dict
    smoothed_temperature_dict[year] = moving_average


def en(t):
    return en0 + be*smoothed_temperature_dict[t]

def taur(t):
    return taur0 + btau*smoothed_temperature_dict[t]

def ea(t):
    return co2_emissions_dict[t]/(1000*2.12)
    #return 0

def d_CO2(t,C):
    return en(t)+ea(t)-C/taur(t)



years=[initial_year]

C=[C0]
natural_emission=[en(initial_year)]
anthropogentic_emission=[ea(initial_year)]
absorption=[-C0/taur(initial_year)]
temperature=[smoothed_temperature_dict[initial_year]]
natural_net_balance=[en(initial_year)-C0/taur(initial_year)]
total_net_balance=[natural_net_balance[0]+anthropogentic_emission[0]]

for year in range(initial_year+1,final_year+1):
    years.append(year)
    C.append(C[-1]+d_CO2(year,C[-1]))
    natural_emission.append(en(year))
    anthropogentic_emission.append(ea(year))
    absorption.append(-C[-1]/taur(year))
    temperature.append(smoothed_temperature_dict[year])
    natural_net_balance.append((en(year)-C[-1]/taur(year)))
    total_net_balance.append(natural_net_balance[-1]+anthropogentic_emission[-1])


# Create a line plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

plt.subplot(3, 1, 1)
# plt.plot(years, [x - C[0] for x in C], marker='o', linestyle='-',label='CO2')
# plt.plot(years, [x - natural_emission[0] for x in natural_emission], marker='o', linestyle='-',label='natural emission')
plt.plot(years, anthropogentic_emission, marker='+', linestyle='-',label='anthropogenic emission')
# plt.plot(years, [x - absorption[0] for x in absorption], marker='o', linestyle='-',label='absorption')
plt.plot(years, natural_net_balance, marker='+', linestyle='-',label='natural net balance')
plt.plot(years, total_net_balance, marker='+', linestyle='-',label='total net balance')
plt.legend(loc="upper left")
# Add labels and a title
#plt.xlabel('Year')
plt.ylabel('CO2 in ppm')
#plt.title('CO2 balance')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(years, C, marker='+', linestyle='-',label='CO2 in atmosphere',color='r')
plt.legend(loc="upper left")
#plt.xlabel('Year')
plt.ylabel('CO2 in ppm')
#plt.title('CO2 in atmospher')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(years, temperature, marker='+', linestyle='-',label='temperature',color='k')
plt.legend(loc="upper left")
#plt.xlabel('Year')
plt.ylabel('temperature')
#plt.title('temperature')
plt.grid(True)


# Show the plot

plt.tight_layout()
plt.show()


print(en(1880))
print(en(2016))

print(C[0]/taur(1880))
print(C[135]/taur(2016))