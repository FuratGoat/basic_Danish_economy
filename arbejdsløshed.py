import matplotlib.pyplot as plt
import pandas as pd

arbejdsløshed_filepath = '/Users/furatnassaralha/Desktop/Programmering/Programmering/Arbedsløshed/arbejdsløshed_dkstatistik.xlsx'
bnp_filepath = '/Users/furatnassaralha/Desktop/Programmering/Programmering/Arbedsløshed/bnp.xlsx'
rente_filepath = '/Users/furatnassaralha/Desktop/Programmering/Programmering/Arbedsløshed/rente.xlsx'

def load_and_clean_arbejdsløshed(filepath):
    df = pd.read_excel(filepath)
    df = df.drop(columns='Ledighedsindikator efter sæsonkorrigering og faktiske tal, tid og ydelsestype')
    df = df.rename(columns={'Unnamed: 1': 'Tid', 'Unnamed: 2': 'Antal Ledige'})
    df['Antal Ledige'] = pd.to_numeric(df['Antal Ledige'], errors='coerce')
    df = df.dropna()
    df['Tid'] = pd.to_datetime(df['Tid'], format='%YM%m')
    return df.set_index('Tid')

def load_and_clean_bnp(filepath):
    df = pd.read_excel(filepath)
    df = df.rename(columns={'Unnamed: 0': 'Tid', 'Unnamed: 1': 'BNP'})
    df['BNP'] = pd.to_numeric(df['BNP'], errors='coerce')
    df = df.dropna()
    df['Tid'] = pd.to_datetime(df['Tid'], format='%Y')
    return df.set_index('Tid')

def load_and_clean_rente(filepath):
    df = pd.read_excel(filepath)
    df = df.drop(df.columns[0], axis=1)  # Drop the first unnamed column
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

    ax1.plot(df1.index, df1[col1], color='blue', label=col1)
    ax1.set_xlabel('År')
    ax1.set_ylabel(y1_label, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(df2.index, df2[col2], color='green', label=col2)
    ax2.set_ylabel(y2_label, color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    for event in events:
        ax1.axvspan(pd.to_datetime(event["start"]), pd.to_datetime(event["end"]), 
                    color=event["color"], alpha=0.3, label=event["label"])

    fig.suptitle(title)
    ax1.legend(loc="upper left")
    fig.tight_layout()
    plt.show()

df_arbejdsløshed = load_and_clean_arbejdsløshed(arbejdsløshed_filepath)
df_bnp = load_and_clean_bnp(bnp_filepath)
df_ny_rente = load_and_clean_rente(rente_filepath)

dual_axis_plot_with_events(df_arbejdsløshed, 'Antal Ledige', df_bnp, 'BNP', 
                           'Arbejdsløshed vs. BNP', 'Antal ledige', 'BNP', events)

dual_axis_plot_with_events(df_arbejdsløshed, 'Antal Ledige', df_ny_rente, 
                           'Nationalbankens rente - Udlån', 'Arbejdsløshed vs. Rente', 
                           'Antal ledige', 'Rente i %', events)

dual_axis_plot_with_events(df_bnp, 'BNP', df_ny_rente, 'Nationalbankens rente - Udlån', 
                           'BNP vs. Rente', 'BNP', 'Rente i %', events)
