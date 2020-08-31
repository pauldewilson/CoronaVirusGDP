import pandas as pd


class DF_GDP:
    """
    Class which grabs the data live from the ECDC and returns it in a pandas dataframe
    """

    def __init__(self):
        """
        Creating the pandas dataframe of the ECDC JSON data
        """
        self.datasource = "http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=excel"
        self.cols_keep = ['Country Name'] + [str(n) for n in range(1960, 2020)]
        self.df = pd.read_excel(self.datasource, sheet_name='Data', skiprows=3, usecols=self.cols_keep)

    def _instantiate_dataframe(self):
        """
        Converting the dtypes from object to int for ints, and date to date
        Also renames the columns to more user-friendly names
        :return: None
        """
        # rename columns/values if necessary
        # if not necessary (LOL!) then delete this

    def return_df_all(self):
        """
        :return: pandas DataFrame
        """
        self._instantiate_dataframe()
        return self.df
