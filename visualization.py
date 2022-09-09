import pandas as pd
import itertools
from scipy import misc
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from journals import Journals
import os


class Visualization:

    def plot_dist(self,df, by, bins, title, xLabel=None, yLabel=None, save_fig_name=None):
        df[by].hist(bins=bins)
        if not xLabel:
            xLabel=by+' value'
        if not yLabel:
            yLabel='Num authors'
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        # plt.show()
        if (save_fig_name!=None):
            plt.savefig(save_fig_name)
        plt.close()



    def normalize_values(self,df,by):
        df[by+" standarized"]=0
        df[by+" standarized"] = (df[by]-df[by].mean()) / df[by].std()
        df[by+" normalized"] = (df[by] - df[by].min()) / (df[by].max() - df[by].min())
        print(by)
        print(df[by].sum())
        # print(df.loc[0:29,by].sum())
        print(df[by+" normalized"].sum())

    def author_dist(self,df):
        df['num authors']=df.apply(lambda row: pd.Series(row['Author(s) ID'].count(';')),axis=1)
        self.plot_dist(df,by='num authors', bins=10, title='distribution of number of authors per article',
                       xLabel='Num authors',yLabel='Num papers')
        self.plot_dist(df, by='Cited by', bins=30, title='distribution of number of citations per article',
                       xLabel='Num citations', yLabel='Num papers')

    def shapley_star_dist(self, df):
        ax=df['Shapley_star'].plot(title='shapley star values',use_index=True)
        # ax.set_yticks(range(-1,3))
        # plt.title(title)
        plt.ylabel('Shapley value')
        plt.xlabel('Num authors')
        plt.show()

        return


if __name__ == '__main__':
    #name = dirs[5]
    journals = Journals()
    for current_journal in journals.dirsIS:
        for file in os.listdir(path=journals.file_path+current_journal):
            if not file.startswith('shap_full_star_all_authors.csv'):
                continue
            print('now creating for {}'.format(current_journal))
            obj_path = os.path.join(journals.file_path+current_journal, file)
            df_shap = pd.read_csv(obj_path)
            df_shap.reset_index(inplace=True)
            vis = Visualization()
            vis.plot_dist(df_shap, by="Shapley_star", bins=15, title="shapley star distribution " + current_journal,
                          save_fig_name=journals.file_path + current_journal + '\\shapley star distribution.jpg')

    #          current_journal=journals.dirsIS[3]
    #         file_name =  current_journal + '\\' +  'shap_full_star_all_authors.csv'  # international journal of law...
    # file_path='C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\'
    # pi_ban=file_path+'ASLIB_Journal_of_info_manage\\power_index\\ban_fractional_10_30_005_cites_over_3_q4.csv'
    # file_name='ASLIB_Journal_of_info_manage\\ASLIB_Journal_of_info_manage_2018-2021_scopus.csv'
    # file_name = 'First_monday\\First_Monday_2018_issues_11_scopus.csv'
    #     df=pd.read_csv(journals.file_path+file_name, index_col=0)

    exit(0)

    df = pd.read_csv(pi_ban, index_col=0)
    vis=Visualization()
    # vis.plot_dist(df,'Banzhaf',15, 'Banzhaf power index distribution')
    vis.normalize_values(df,'Banzhaf')
    vis.plot_dist(df, by="Banzhaf normalized", bins=15, title="Normalized Banzhaf power index distribution")

    pi_shap=file_path+'ASLIB_Journal_of_info_manage\\power_index\\shap_fractional_10_30_005_cites_over_3_q4.csv'
    df = pd.read_csv(pi_shap, index_col=0)
    vis = Visualization()
    vis.normalize_values(df,'Shapley')
    # vis.plot_dist(df, 'Shapley', 15, 'Shapley power index distribution')
    vis.plot_dist(df,by="Shapley normalized",bins=15,title="Normalized Shapley power index distribution")

    exit(0)
    frac_file = file_path + 'ASLIB_Journal_of_info_manage\\shapley_value\\fractional_values_cites_over_3.csv'
    df = pd.read_csv(frac_file, index_col=0)
    vis = Visualization()
    vis.normalize_values(df,'Fractional')
    # vis.plot_dist(df, 'Fractional', 15, 'Fractional value distribution')
    vis.plot_dist(df, by="Fractional normalized", bins=15, title="Normalized fractional distribution")

    frac_file_norm = file_path + 'ASLIB_Journal_of_info_manage\\shapley_value\\fractional_values_cites_over_3_normalized.csv'
    df = pd.read_csv(frac_file_norm, index_col=0)
    vis = Visualization()
    vis.normalize_values(df,'Fractional')
    # vis.plot_dist(df, 'Fractional', 15, 'Normalized Fractional value distribution')
    vis.plot_dist(df, by="Fractional normalized", bins=15, title="Normalized fractional distribution")

    full_file = file_path + 'ASLIB_Journal_of_info_manage\\shapley_value\\full_values_cites_over_3.csv'
    df = pd.read_csv(full_file, index_col=0)
    vis = Visualization()
    vis.normalize_values(df, 'Full')
    # vis.plot_dist(df, 'Full', 15, 'Normalized Full value distribution')
    vis.plot_dist(df, by="Full normalized", bins=15, title="Normalized Full value distribution")


    full_file_norm = file_path + 'ASLIB_Journal_of_info_manage\\shapley_value\\full_values_cites_over_3_normalized.csv'
    df = pd.read_csv(full_file_norm, index_col=0)
    vis = Visualization()
    vis.normalize_values(df, 'Full')
    vis.plot_dist(df, by="Full normalized", bins=15, title="Normalized Full value distribution")



