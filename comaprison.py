from datetime import date,datetime,timedelta
import pandas as pd
from scipy import stats



class Comparison:

    def extract_data(self, file1, file2):
        df1=pd.read_csv(file1)
        df2=pd.read_csv(file2)

        # print(df1.head())
        # print(df2.head())

        return df1, df2


    def compare_frac_full_pi_partial(self,df_frac,df_pi, banzhaf=False):
        for idx, author_data in df_frac.iterrows():
            author=author_data.loc['Author Id']
            frac=author_data['fractional value']
            author_data_pi=df_pi[df_pi['Author Id']==author]
            if len(author_data_pi)>0:
                if banzhaf:
                    pi=author_data_pi['banzhaf']
                else:
                    pi=author_data_pi['shapley']

            else:
                if frac>1:
                    print('for author {} no pi but frac is {}'.format(author,frac))

    def sort(self,df1,df2, df1_by, df2_by):
        df1_sorted=df1.sort_values(by=df1_by, ascending=[False,False], ignore_index=True, key=None)
        df2_sorted=df2.sort_values(by=df2_by, ascending=[False,False], ignore_index=True, key=None)

        # print(df1_sorted)
        # print(df2_sorted)
        return df1_sorted,df2_sorted

    def gen_ranks(self,df1,df2):

        rank_array1=list(df1.index.values)
        rank_array2 = []
        for idx in range(rank_array1[-1]+1):
            author_id=df1.iloc[idx,:]['Author Id']
            df2_idx=df2.loc[df2['Author Id'] == author_id].index.values[0]
            rank_array2.append(df2_idx)
        rank_array1 = [x + 1 for x in rank_array1]
        rank_array2 = [x + 1 for x in rank_array2]
        # print(rank_array1)
        # print(rank_array2)
        return rank_array1,rank_array2

    def calc_kendall_tau(self,rank1,rank2):
        tau, p_value = stats.kendalltau(rank1, rank2)
        print('tau {}, pVal {}'.format(tau,p_value))
        return tau,p_value

if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    file_path='C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\ASLIB_Journal_of_info_manage\\'
    pi_ban=file_path+'power_index\\ban_fractional_4_16_005_cites_over_3_q4.csv'
    pi_shap=file_path+'power_index\\shap_fractional_4_16_005_cites_over_3_q4.csv'

    frac_file=file_path+'shapley_value\\fractional_values_cites_over_3.csv'
    frac_file_norm=file_path+'shapley_value\\fractional_values_cites_over_3_normalized.csv'

    full_file = file_path + 'shapley_value\\full_values_cites_over_3.csv'
    full_file_norm = file_path + 'shapley_value\\full_values_cites_over_3_normalized.csv'

    comp=Comparison()
    # df_ban,df_shap=comp.extract_data(pi_ban,pi_shap)
    # df_ban,df_shap=comp.sort(df_ban,df_shap,df1_by=['Num critical groups','Author Id'], df2_by=['Num critical groups','Author Id'])
    # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
    # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
    # ban_rank,shap_rank=comp.gen_ranks(df_ban,df_shap)
    # print('kendall tau for banzhaf and shapley')
    # comp.calc_kendall_tau(ban_rank,shap_rank)

    # df_shap, df_frac = comp.extract_data(pi_shap, frac_file)
    # df_shap, df_frac=comp.sort(df_shap,df_frac,df1_by=['Num critical groups','Author Id'], df2_by=['Fractional','Author Id'])
    # print(df_frac[['Author Id','fractional value']].head(10))
    # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
    # shap_rank, frac_rank = comp.gen_ranks(df_shap, df_frac)
    # print('kendall tau for shapley and fractional')
    # comp.calc_kendall_tau(shap_rank, frac_rank)

    # df_ban, df_frac = comp.extract_data(pi_ban, frac_file)
    # df_ban, df_frac = comp.sort(df_ban, df_frac, df1_by=['Num critical groups', 'Author Id'],
    #                                  df2_by=['Fractional', 'Author Id'])
    # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
    # print(df_frac_norm[['Author Id','fractional value']].head(10))
    # ban_rank, frac_rank = comp.gen_ranks(df_ban, df_frac)
    # print('kendall tau for Banzhaf and fractional ')
    # comp.calc_kendall_tau(ban_rank, frac_rank)

    # df_ban,df_frac_norm=comp.extract_data(pi_ban,frac_file_norm)
    # df_ban, df_frac_norm=comp.sort(df_ban,df_frac_norm,df1_by=['Num critical groups','Author Id'], df2_by=['Fractional','Author Id'])
    # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
    # print(df_frac_norm[['Author Id','fractional value']].head(10))
    # ban_rank,frac_norm_rank=comp.gen_ranks(df_ban,df_frac_norm)
    # print('kendall tau for Banzhaf and fractional normalized')
    # comp.calc_kendall_tau(ban_rank,frac_norm_rank)

    # df_shap, df_frac_norm = comp.extract_data(pi_shap, frac_file_norm)
    # df_shap, df_frac_norm=comp.sort(df_shap,df_frac_norm,df1_by=['Num critical groups','Author Id'], df2_by=['Fractional','Author Id'])
    # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
    # print(df_frac_norm[['Author Id','fractional value']].head(10))
    # shap_rank, frac_norm_rank = comp.gen_ranks(df_shap, df_frac_norm)
    # print('kendall tau for shapley and fractional normalized')
    # comp.calc_kendall_tau(shap_rank, frac_norm_rank)

    # df_frac, df_frac_norm = comp.extract_data(frac_file, frac_file_norm)
    # df_frac, df_frac_norm = comp.sort(df_frac, df_frac_norm, df1_by=['Fractional', 'Author Id'],
    #                                   df2_by=['Fractional', 'Author Id'])
    # print(df_frac[['Author Id', 'fractional value']].head(10))
    # print(df_frac_norm[['Author Id', 'fractional value']].head(10))
    # frac_rank, frac_norm_rank = comp.gen_ranks(df_frac, df_frac_norm)
    # print('kendall tau for fractional and fractional normalized')
    # comp.calc_kendall_tau(frac_rank, frac_norm_rank)

    df_shap, df_full = comp.extract_data(pi_shap, full_file)
    df_shap, df_full = comp.sort(df_shap, df_full, df1_by=['Num critical groups', 'Author Id'],
                                 df2_by=['Full', 'Author Id'])
    # print(df_frac[['Author Id','fractional value']].head(10))
    # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
    shap_rank, full_rank = comp.gen_ranks(df_shap, df_full)
    print('kendall tau for shapley and full')
    comp.calc_kendall_tau(shap_rank, full_rank)

    df_shap, df_full_norm = comp.extract_data(pi_shap, full_file_norm)
    df_shap, df_full_norm = comp.sort(df_shap, df_full_norm, df1_by=['Num critical groups', 'Author Id'],
                                      df2_by=['Full', 'Author Id'])
    # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
    # print(df_frac_norm[['Author Id','fractional value']].head(10))
    shap_rank, full_norm_rank = comp.gen_ranks(df_shap, df_full_norm)
    print('kendall tau for shapley and full normalized')
    comp.calc_kendall_tau(shap_rank, full_norm_rank)

    # df_shap.to_csv('shap_4_16_005_cites_over_3_q4.csv')
    # df_ban.to_csv('ban_4_16_005_cites_over_3_q4.csv')
    # df_frac.to_csv('frac_cites_over_3.csv')
    # df_frac_norm.to_csv('frac_normalized_cites_over_3.csv')


    # comp.compare_frac_full_pi_partial(df_frac,df_pi, banzhaf=True)
