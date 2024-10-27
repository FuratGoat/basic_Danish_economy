import matplotlib.pyplot as plt
import pandas as pd

unemployment_filepath = '/Users/furatnassaralha/Desktop/Programmering/Programmering/Arbedsløshed/arbejdsløshed_dkstatistik.xlsx'
gdp_filepath = '/Users/furatnassaralha/Desktop/Programmering/Programmering/Arbedsløshed/bnp.xlsx'
interest_rate_filepath = '/Users/furatnassaralha/Desktop/Programmering/Programmering/Arbedsløshed/rente.xlsx'

def load_and_clean_unemployment(filepath):
    df = pd.read_excel(filepath)
    df = df.drop(columns='Ledighedsindikator efter sæsonkorrigering og faktiske tal, tid og ydelsestype')
    df = df.rename(columns={'Unnamed: 1': 'Tid', 'Unnamed: 2': 'Antal Ledige'})
    df['Antal Ledige'] = pd.to_numeric(df['Antal Ledige'], errors='coerce')
    df = df.dropna()
    df['Tid'] = pd.to_datetime(df['Tid'], format='%YM%m')
    return df.set_index('Tid')

def load_and_clean_gdp(filepath):
    df = pd.read_excel(filepath)
    df = df.rename(columns={'Unnamed: 0': 'Time', 'Unnamed: 1': 'GDP'})
    df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')
    df = df.dropna()
    df['Time'] = pd.to_datetime(df['Time'], format='%Y')
    return df.set_index('Time')

def load_and_clean_interest_rate(filepath):
    df = pd.read_excel(filepath)
    df = df.drop(df.columns[0], axis=1)
    df = df.rename(columns={'Unnamed: 2': 'Tid', 'Unnamed: 3': 'Procent'})

    df['Tid'] = df['Tid'].drop_duplicates().dropna().reset_index(drop=True)

    df_first_part = df.loc[0:298, "Procent"].reset_index(drop=True)
    df_second_part = df.loc[299:453, "Procent"].reset_index(drop=True)
    tid_column = df['Tid'].iloc[:len(df_first_part)].reset_index(drop=True)

    df_ny_rente = pd.DataFrame({
        'Tid': tid_column,
        'Nationalbankens rente - Udlån': pd.to_numeric(df_first_part, errors='coerce'),
        'Obligationsrente 1987-nov. 2012': pd.to_numeric(df_second_part, errors='coerce')
    })

    df_ny_rente['Tid'] = pd.to_datetime(df_ny_rente['Tid'], format='%YM%m')
    return df_ny_rente.set_index('Tid')

events = [
    {"label": "Dot-com Bubble", "start": "2000-01-01", "end": "2002-01-01", "color": "lightgray"},
    {"label": "Financial Crisis", "start": "2007-12-01", "end": "2009-06-01", "color": "salmon"},
    {"label": "COVID-19 Pandemic", "start": "2020-02-01", "end": "2021-04-01", "color": "lightblue"},
]

def dual_axis_plot_with_events(df1, col1, df2, col2, title, y1_label, y2_label, events):
    fig, ax1 = plt.subplots(figsize=(15, 8))

    line1 = ax1.plot(df1.index, df1[col1], color='blue', label=y1_label)
    ax1.set_xlabel('Year')
    ax1.set_ylabel(y1_label, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    line2 = ax2.plot(df2.index, df2[col2], color='green', label=y2_label)
    ax2.set_ylabel(y2_label, color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    spans = []
    for event in events:
        span = ax1.axvspan(pd.to_datetime(event["start"]), pd.to_datetime(event["end"]), 
                          color=event["color"], alpha=0.3, label=event["label"])
        spans.append(span)

    lines = line1 + line2 + spans
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left")

    fig.suptitle(title)
    fig.tight_layout()
    plt.show()

df_unemployment = load_and_clean_unemployment(unemployment_filepath)
df_gdp = load_and_clean_gdp(gdp_filepath)
df_new_interest_rate = load_and_clean_interest_rate(interest_rate_filepath)

dual_axis_plot_with_events(df_unemployment, 'Antal Ledige', df_gdp, 'GDP', 
                          'Unemployment vs. GDP', 'Number of Unemployed', 'GDP', events)

dual_axis_plot_with_events(df_unemployment, 'Antal Ledige', df_new_interest_rate, 
                          'Nationalbankens rente - Udlån', 'Unemployment vs. Interest Rate', 
                          'Number of Unemployed', 'Interest Rate in %', events)

dual_axis_plot_with_events(df_gdp, 'GDP', df_new_interest_rate, 'Nationalbankens rente - Udlån', 
                          'GDP vs. Interest Rate', 'GDP', 'Interest Rate in %', events)
