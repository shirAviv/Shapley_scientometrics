import pandas as pd
import itertools
from scipy import misc
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler,StandardScaler




class Visualization:
    def plot_dist(self,df, by, bins, title):
        df[by].hist(bins=bins)
        plt.xlabel(by+' value')
        plt.ylabel('Num authors')
        plt.title(title)
        plt.show()



    def normalize_values(self,df,by):
        df[by+" standarized"]=0
        df[by+" standarized"] = (df[by]-df[by].mean()) / df[by].std()
        df[by+" normalized"] = (df[by] - df[by].min()) / (df[by].max() - df[by].min())
        print(by)
        print(df[by].sum())
        # print(df.loc[0:29,by].sum())
        print(df[by+" normalized"].sum())



if __name__ == '__main__':
    file_path='C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\ASLIB_Journal_of_info_manage\\'
    pi_ban=file_path+'power_index\\ban_4_16_005_cites_over_3_q4.csv'
    df = pd.read_csv(pi_ban, index_col=0)
    vis=Visualization()
    # vis.plot_dist(df,'Banzhaf',15, 'Banzhaf power index distribution')
    vis.normalize_values(df,'Banzhaf')
    vis.plot_dist(df, by="Banzhaf normalized", bins=15, title="Normalized Banzhaf power index distribution")

    pi_shap=file_path+'power_index\\shap_4_16_005_cites_over_3_q4.csv'
    df = pd.read_csv(pi_shap, index_col=0)
    vis = Visualization()
    vis.normalize_values(df,'Shapley')
    # vis.plot_dist(df, 'Shapley', 15, 'Shapley power index distribution')
    vis.plot_dist(df,by="Shapley normalized",bins=15,title="Normalized Shapley power index distribution")

    frac_file = file_path + 'shapley_value\\fractional_values_cites_over_3.csv'
    df = pd.read_csv(frac_file, index_col=0)
    vis = Visualization()
    vis.normalize_values(df,'Fractional')
    # vis.plot_dist(df, 'Fractional', 15, 'Fractional value distribution')
    vis.plot_dist(df, by="Fractional normalized", bins=15, title="Normalized fractional distribution")

    frac_file_norm = file_path + 'shapley_value\\fractional_values_cites_over_3_normalized.csv'
    df = pd.read_csv(frac_file_norm, index_col=0)
    vis = Visualization()
    vis.normalize_values(df,'Fractional')
    # vis.plot_dist(df, 'Fractional', 15, 'Normalized Fractional value distribution')
    vis.plot_dist(df, by="Fractional normalized", bins=15, title="Normalized fractional distribution")

    full_file = file_path + 'shapley_value\\full_values_cites_over_3.csv'
    df = pd.read_csv(full_file, index_col=0)
    vis = Visualization()
    vis.normalize_values(df, 'Full')
    # vis.plot_dist(df, 'Full', 15, 'Normalized Full value distribution')
    vis.plot_dist(df, by="Full normalized", bins=15, title="Normalized Full value distribution")


    full_file_norm = file_path + 'shapley_value\\full_values_cites_over_3_normalized.csv'
    df = pd.read_csv(full_file_norm, index_col=0)
    vis = Visualization()
    vis.normalize_values(df, 'Full')
    vis.plot_dist(df, by="Full normalized", bins=15, title="Normalized Full value distribution")



