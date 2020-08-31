import pandas as pd


class DF_Corona:
    """
    Class which grabs the data live from the ECDC and returns it in a pandas dataframe
    """

    def __init__(self):
        """
        Creating the pandas dataframe of the ECDC JSON data
        """
        self.datasource = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        self.df = pd.read_csv(self.datasource, parse_dates=True)

    def _instantiate_dataframe(self):
        """
        Converting the dtypes from object to int for ints, and date to date
        Also renames the columns to more user-friendly names
        :return: None
        """
        cols_rename = 'date day month year cases deaths country geo_id country_id population continent two_week_per_100k'.split()
        cols_rename = [s.capitalize() for s in cols_rename]
        self.df.columns = cols_rename
        self.df['Country'] = self.df['Country'].str.replace('_', ' ')
        self.df['Continent'] = self.df['Continent'].str.replace('America', 'Americas')
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d/%m/%Y')
        self.df.insert(loc=6, column='Deaths_Capita', value=(self.df["Deaths"] / self.df["Population"]) * 100000,
                       allow_duplicates=True)

    def return_df_all(self):
        """
        :return: pandas DataFrame
        """
        self._instantiate_dataframe()
        return self.df

    def return_df_sum_country(self):
        self._instantiate_dataframe()
        # need to insert min of population else it will sum for all entries
        population_column = self.df.groupby('Country').min()['Population']
        df_max = self.df.groupby('Country').sum()
        df_max['Population'] = population_column
        df_max.reset_index(inplace=True)
        return df_max

    def return_df_min_country(self):
        self._instantiate_dataframe()
        df_min = self.df.groupby('Country').min()
        df_min.reset_index(inplace=True)
        return df_min

    def return_df_sum_continent(self):
        self._instantiate_dataframe()
        # need to insert min of population else it will sum for all entries
        population_column = self.df.groupby('Country').min()['Population']
        df_max = self.df.groupby('Continent').sum()
        df_max['Population'] = population_column
        df_max.reset_index(inplace=True)
        return df_max

    def return_df_rolling_deaths(self):
        self._instantiate_dataframe()
        df_roll = self.df.rolling(len(self.df), min_periods=1, on='Date').sum()
        df_roll.insert(loc=0, column='Country', value=self.df['Country'])
        df_roll.insert(loc=0, column='Continent', value=self.df['Continent'])
        return df_roll
