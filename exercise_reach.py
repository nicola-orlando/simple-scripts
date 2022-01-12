import numpy as np
import uproot
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

dataset = "/afs/cern.ch/user/o/orlando/reach_examples/Data_Analysis_Officer_test/Annex_1_REACH_Assessment_Test_Database_DataAnalyst_v2.csv"

def make_text_freq_plot_1d(title_simple,indexes,plot_title,is_log_y,y_axis_name,is_grid,width,tick_size=0):
    legend = title_simple
    color = 'lavender' 
    plt.bar(indexes, width, color=color, linewidth=0.5,edgecolor='black',label=legend)
    ax=plt.axes()
    if is_log_y:
        plt.yscale('log')
    plt.ylabel(y_axis_name)
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig(plot_title)
    plt.close()

df = pd.read_csv(dataset, engine='python')

# print("Prining head of the file to see how it looks")
print(df.head())
print("Prining data types")
print(df.dtypes)

# Renaniming some coulmns for convenience (accessing data directly from dataframe)
df = df.rename(columns={'Marital status - Head of Household':'marital_status_head_of_household'})
df = df.rename(columns={'Number household member boy under5 years old':'household_boy_under5'})
df = df.rename(columns={'Number household member _girl_under5 years old':'household_girl_under5'})
df = df.rename(columns={'Number household member boy_5_17 years old':'household_boy_5_17'})
df = df.rename(columns={'household_girl_5_17':'household_girl_5_17'})
df = df.rename(columns={'number adult household members years old':'adult_household_members_years_old'})
df = df.rename(columns={'Total household number':'total_household_number'})
df = df.rename(columns={'drinking water source other':'drinking_water_source_other'})
df = df.rename(columns={'Households use bottled water as drinking water source':'households_use_bottled_water_as_drinking_water_source'})
df = df.rename(columns={'Household treating water':'household_treating_water'})
df = df.rename(columns={'Household praticing open defecation':'household_praticing_open_defecation'})
df = df.rename(columns={'Frequency respondant report handwhashing a day':'frequency_respondant_report_handwhashing_a_day'})

# Cleaning and sorting the dataset 
df = df.sort_values(by='InterviewID')
print(df.head())

# Look for a specific Nan I think is in there..
df = df.fillna('I_am_a_NaN')

make_text_freq_plot_1d('InterviewID',df.InterviewID,'InterviewID.png',False,'InterviewID',False,0.8,5.0)
make_text_freq_plot_1d('data_collection_round',df.data_collection_round,'data_collection_round.png',False,'data_collection_round',False,0.8,5.0)
make_text_freq_plot_1d('marital_status_head_of_household',df.marital_status_head_of_household,'marital_status_head_of_household.png',False,'marital_status_head_of_household',False,0.8,5.0)
make_text_freq_plot_1d('single_headed_household',df.single_headed_household,'single_headed_household.png',False,'single_headed_household',False,0.8,5.0)
make_text_freq_plot_1d('household_boy_under5',df.household_boy_under5,'household_boy_under5.png',False,'household_boy_under5',False,0.8,5.0)
make_text_freq_plot_1d('household_girl_under5',df.household_girl_under5,'household_girl_under5.png',False,'household_girl_under5',False,0.8,5.0)
make_text_freq_plot_1d('household_boy_5_17',df.household_boy_5_17,'household_boy_5_17.png',False,'household_boy_5_17                                        ',False,0.8,5.0)
make_text_freq_plot_1d('household_girl_5_17',df.household_girl_5_17,'household_girl_5_17.png',False,'household_girl_5_17',False,0.8,5.0)
make_text_freq_plot_1d('adult_household_members_years_old',df.adult_household_members_years_old,'adult_household_members_years_old.png',False,'adult_household_members_years_ol#d',False,0.8,5.0)
make_text_freq_plot_1d('total_household_number',df.total_household_number,'total_household_number.png',False,'total_household_number',False,0.8,5.0)
make_text_freq_plot_1d('diarrhea_under_5',df.diarrhea_under_5,'diarrhea_under_5.png',False,'diarrhea_under_5',False,0.8,5.0)
make_text_freq_plot_1d('house_type',df.house_type,'house_type.png',False,'house_type',False,0.8,5.0)
make_text_freq_plot_1d('drinking_water_source',df.drinking_water_source,'drinking_water_source.png',False,'drinking_water_source',False,0.8,5.0)
make_text_freq_plot_1d('drinking_water_source_other',df.drinking_water_source_other,'drinking_water_source_other.png',False,'drinking_water_source_other',False,0.8,5.0)
make_text_freq_plot_1d('households_use_bottled_water_as_drinking_water_source',df.households_use_bottled_water_as_drinking_water_source,'households_use_bottled_water_as_drinking_water_source.png',False,'households_use_bottled_water_as_drinking_water_source',False,0.8,5.0)
make_text_freq_plot_1d('household_treating_water',df.household_treating_water,'household_treating_water.png',False,'household_treating_water',False,0.8,5.0)
make_text_freq_plot_1d('Improvedsanitationfacility',df.Improvedsanitationfacility,'Improvedsanitationfacility.png',False,'Improvedsanitationfacility',False,0.8,5.0)
make_text_freq_plot_1d('Mentionedafterdefecating',df.Mentionedafterdefecating,'Mentionedafterdefecating.png',False,'Mentionedafterdefecating',False,0.8,5.0)
make_text_freq_plot_1d('Mentionedbeforeeating',df.Mentionedbeforeeating,'Mentionedbeforeeating.png',False,'Mentionedbeforeeating',False,0.8,5.0)
make_text_freq_plot_1d('Mentionedbeforeeatingafterdefecating',df.Mentionedbeforeeatingafterdefecating,'Mentionedbeforeeatingafterdefecating.png',False,'Mentionedbeforeeatingafterdefecating',False,0.8,5.0)
make_text_freq_plot_1d('Mentionedbeforefeedingchild',df.Mentionedbeforefeedingchild,'Mentionedbeforefeedingchild.png',False,'Mentionedbeforefeedingchild',False,0.8,5.0)
make_text_freq_plot_1d('handwashingfull',df.handwashingfull,'handwashingfull.png',False,'handwashingfull',False,0.8,5.0)
make_text_freq_plot_1d('household_praticing_open_defecation',df.household_praticing_open_defecation,'household_praticing_open_defecation.png',False,'household_praticing_open_defecation',False,0.8,5.0)
make_text_freq_plot_1d('frequency_respondant_report_handwhashing_a_day',df.frequency_respondant_report_handwhashing_a_day,'frequency_respondant_report_handwhashing_a_day.png',False,'frequency_respondant_report_handwhashing_a_day',False,0.8,5.0)



