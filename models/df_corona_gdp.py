from models.df_corona import DF_Corona
from models.df_gdp import DF_GDP
import pandas as pd


class DF_Corona_GDP():

    def __init__(self):
        self.df_corona = pd.DataFrame()
        self.df_gdp = pd.DataFrame()
        self.df_merged = pd.DataFrame()

    @staticmethod
    def _countries_rename_in_gdp_index():
        return {
            'Bahamas, The': 'Bahamas', 'Cabo Verde': 'Cape Verde',
            'Congo, Dem. Rep.': 'Democratic Republic of the Congo', 'Congo, Rep.': 'Congo',
            "Cote d'Ivoire": 'Cote dIvoire', 'Czech Republic': 'Czechia', 'Europe & Central Asia': 'Egypt',
            'Gambia, The': 'Gambia', 'Guinea-Bissau': 'Guinea Bissau', 'Iran, Islamic Rep.': 'Iran',
            'Korea, Rep.': 'South Korea', 'Kyrgyz Republic': 'Kyrgyzstan', 'Lao PDR': 'Laos',
            'Russian Federation': 'Russia', 'Slovak Republic': 'Slovakia',
            'Tanzania': 'United Republic of Tanzania', 'Timor-Leste': 'Timor Leste',
            'United States': 'United States of America', 'Yemen, Rep.': 'Yemen'
        }

    def _instantiate_dataframes(self):
        """
        Note: Can return different chart types if using different df_corona charts
        This is not programmed in since this was a one-time exercise
        """
        # instantiate and set indexes
        self.df_corona = DF_Corona().return_df_sum_country()
        self.df_corona.set_index('Country', inplace=True)
        self.df_gdp = DF_GDP().return_df_all()
        self.df_gdp.set_index('Country Name', inplace=True)
        # some GDP figures are missing for last few years for some countries
        # these will be filled in from the last value
        self.df_gdp.fillna(axis=0, method='bfill', inplace=True)
        self.df_gdp.rename(mapper=self._countries_rename_in_gdp_index(), inplace=True)
        # create merged df
        self.df_merged = pd.merge(left=self.df_corona, right=self.df_gdp, left_index=True, right_index=True,
                                  how='inner')
        # inserting the per capita GDP column
        gdp_per_capita = self.df_merged['2019'] / self.df_merged['Population']
        self.df_merged.insert(loc=6,
                              column='GDP_Capita',
                              value=gdp_per_capita,
                              allow_duplicates=True)

    def _MAPPING_EXERCISE_gdp_country_names_that_need_changed(self):
        """
        Only for use in the one-time-task of renaming countries in the GDP table
        """
        self._instantiate_dataframes()
        # return a list of index values (country names) where outer join resulted in NaN for 'Day' column
        # these will be used in a dict to rename them later
        filter_merge_fail = (self.df_merged['Day'].isna() == True)
        return [c for c in self.df_merged.loc[filter_merge_fail, :].index.values]

    def _MAPPING_EXERCISE_columns_rename_mapping(self):
        """
        Only for use in the one-time-task of renaming countries in the GDP table
        """
        bad_names = self._MAPPING_EXERCISE_gdp_country_names_that_need_changed()
        good_names = [c for c in self.df_corona.index.values]
        rename_mapping = {
            bad_names[2]: good_names[13],
            bad_names[3]: good_names[36],
            bad_names[7]: good_names[53],
            bad_names[8]: good_names[45],
            bad_names[9]: good_names[47],
            bad_names[11]: good_names[52],
            bad_names[18]: good_names[59],
            bad_names[23]: good_names[73],
            bad_names[24]: good_names[85],
            bad_names[33]: good_names[94],
            bad_names[36]: good_names[177],
            bad_names[37]: good_names[108],
            bad_names[38]: good_names[109],
            bad_names[63]: good_names[159],
            bad_names[66]: good_names[173],
            bad_names[79]: good_names[199],
            bad_names[80]: good_names[189],
            bad_names[85]: good_names[201],
            bad_names[92]: good_names[207]
        }
        return rename_mapping

    def return_main_df(self):
        # instantiates the dataframes and performs cleaning
        self._instantiate_dataframes()
        # returns the primary goal of the whole Class, the merged dataframe
        return self.df_merged
