from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd


class Accounts:

    def __init__(self):
        """
        Constructor attribute. To instance class (ex: instance = Accounts()).

        """
        self.__accounts = self.__select_accounts_file()
        self.__general_ledger = self.__select_general_ledger_file()
        self.merged_file = self.__merge_files()
        self.clear_df = self.__sum_account_values().reset_index()
        self.lists = self.__group_by_accounts()
        self._sum_lists = self.__sum_grouped_lists()
        self.sum_df = self.__create_df().rename(columns={0: "Sum_Values"})
        self.sum_df = self.__create_column()
        self.__save_file()

    def __select_accounts_file(self):
        """
        Select your accounts chart file.

        """
        Tk().withdraw()
        print("Please, select your Chart of Accounts file!!")
        self.__accounts = pd.read_excel(askopenfilename())
        return self.__accounts

    def __select_general_ledger_file(self):
        """
        Select your General Ledger chart file.

        """
        print("Please, select your General Ledger file!!")
        self.__general_ledger = pd.read_excel(askopenfilename())
        return self.__general_ledger

    def __merge_files(self):
        """
        Method to merge the selected Dataframe.

        """
        self.merge_file = self.__general_ledger.merge(self.__accounts, on='account')
        return self.merge_file

    def __sum_account_values(self):
        """
        Method to group the selected Dataframe, by summarizing.

        """
        return self.merged_file.groupby('account').sum()

    def __group_by_accounts(self):
        """
        Method to segregate the data in lists.

        """
        self.list1 = [value for account, value in self.clear_df.values if account.startswith('01')]
        self.list2 = [value for account, value in self.clear_df.values if account.startswith('02')]
        self.list3 = [value for account, value in self.clear_df.values if account.startswith('03')]
        self.list4 = [value for account, value in self.clear_df.values if account.startswith('04')]
        self.list5 = [value for account, value in self.clear_df.values if account.startswith('05')]
        return self.list1, self.list2, self.list3, self.list4, self.list5

    def __sum_grouped_lists(self):
        """
        Method to summarize the Value data by account.

        """
        return [sum(self.list1), sum(self.list2), sum(self.list3), sum(self.list4), sum(self.list5)]

    def __create_df(self):
        """
        Method to create a new Dataframe.

        """
        return pd.DataFrame(self._sum_lists)

    def __create_column(self):
        """
        Method to create a new column.

        """
        self.sum_df["Account"] = ['1', '2', '3', '4', '5']
        return self.sum_df.groupby("Account").sum()

    def __save_file(self):
        """
        Method to export and save new files.

        """
        print("The dataframes were saved in root!!")
        return self.clear_df.to_excel("summarized_df1.xlsx"), self.sum_df.to_excel("summarized_df2.xlsx")
