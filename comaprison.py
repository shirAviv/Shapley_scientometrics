from datetime import date,datetime,timedelta
import pandas as pd
from scipy import stats
import numpy as np
from matplotlib import pyplot as plt
import math
from journals import Journals
import os



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

    def calc_tau_for_shapley_and_ban(self):
        file_path = 'C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\ASLIB_Journal_of_info_manage\\'
        pi_ban_full = file_path + 'power_index\\ban_full_4_18_005_cites_over_3_q4.csv'
        pi_shap_full = file_path + 'power_index\\shap_full_4_18_005_cites_over_3_q4.csv'

        pi_ban_fractional = file_path + 'power_index\\ban_fractional_10_30_005_cites_over_3_q4.csv'
        pi_shap_fractional = file_path + 'power_index\\shap_fractional_10_30_005_cites_over_3_q4.csv'

        pi_ban_relative = file_path + 'power_index\\ban_relative_10_30_005_cites_over_3_q4.csv'
        pi_shap_relative = file_path + 'power_index\\shap_relative_10_30_005_cites_over_3_q4.csv'

        frac_file = file_path + 'shapley_value\\fractional_values_cites_over_3.csv'
        frac_file_norm = file_path + 'shapley_value\\fractional_values_cites_over_3_normalized.csv'

        full_file = file_path + 'shapley_value\\full_values_cites_over_3.csv'
        full_file_norm = file_path + 'shapley_value\\full_values_cites_over_3_normalized.csv'

        complete_values_file = file_path + 'shapley_value\\authors_cites_over_3_complete.csv'

        comp = Comparison()
        # df_ban,df_shap=comp.extract_data(pi_ban_fractional,pi_shap_fractional)
        # df_ban,df_shap=comp.sort(df_ban,df_shap,df1_by=['Num critical coalitions','Author Id'], df2_by=['Num critical permutations','Author Id'])
        # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
        # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
        # ban_rank,shap_rank=comp.gen_ranks(df_ban,df_shap)
        # print('kendall tau for banzhaf fractional and shapley fractional')
        # comp.calc_kendall_tau(ban_rank,shap_rank)

        # df_pi_frac, df_pi_rel = comp.extract_data(pi_ban_relative, pi_shap_relative)
        # df_pi_frac, df_pi_rel=comp.sort(df_pi_frac, df_pi_rel,df1_by=['Num critical coalitions','Author Id'], df2_by=['Num critical permutations','Author Id'])
        # print(df_frac[['Author Id','fractional value']].head(10))
        # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
        # pi_frac_rank, pi_rel_rank = comp.gen_ranks(df_pi_frac,df_pi_rel)
        # print('kendall tau for banzhaf relative and shapley relative')
        # comp.calc_kendall_tau(pi_frac_rank, pi_rel_rank)

        # df_pi_full, df_full = comp.extract_data(pi_ban_full, full_file)
        # df_pi_full, df_full = comp.sort(df_pi_full, df_full, df1_by=['Num critical coalitions', 'Author Id'],
        #                                  df2_by=['Full', 'Author Id'])
        # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
        # print(df_frac_norm[['Author Id','fractional value']].head(10))
        # pi_full_rank, full_rank = comp.gen_ranks(df_pi_full, df_full)
        # print('kendall tau for banzhaf full and full ')
        # comp.calc_kendall_tau(pi_full_rank, full_rank)

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

        df_frac, df_pi = comp.extract_data(frac_file, pi_shap_relative)
        df_frac, df_pi = comp.sort(df_frac, df_pi, df1_by=['Fractional', 'Author Id'],
                                   df2_by=['Num critical permutations', 'Author Id'])
        # print(df_frac[['Author Id', 'fractional value']].head(10))
        # print(df_frac_norm[['Author Id', 'fractional value']].head(10))
        frac_rank, pi_rank = comp.gen_ranks(df_frac, df_pi)
        print('kendall tau for Fractional and shapley relative')
        comp.calc_kendall_tau(frac_rank, pi_rank)

        # df_shap, df_full = comp.extract_data(pi_shap_fractional, full_file)
        # df_shap, df_full = comp.sort(df_shap, df_full, df1_by=['Num critical permutations', 'Author Id'],
        #                              df2_by=['Full', 'Author Id'])
        # print(df_frac[['Author Id','fractional value']].head(10))
        # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
        # shap_rank, full_rank = comp.gen_ranks(df_shap, df_full)
        # print('kendall tau for shapley fractional and full')
        # comp.calc_kendall_tau(shap_rank, full_rank)

        # df_shap, df_full_norm = comp.extract_data(pi_shap_full, full_file_norm)
        # df_shap, df_full_norm = comp.sort(df_shap, df_full_norm, df1_by=['Num critical permutations', 'Author Id'],
        #                                   df2_by=['Full', 'Author Id'])
        # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
        # print(df_frac_norm[['Author Id','fractional value']].head(10))
        # shap_rank, full_norm_rank = comp.gen_ranks(df_shap, df_full_norm)
        # print('kendall tau for shapley full and full normalized')
        # comp.calc_kendall_tau(shap_rank, full_norm_rank)

        # df_shap.to_csv('shap_4_16_005_cites_over_3_q4.csv')
        # df_ban.to_csv('ban_4_16_005_cites_over_3_q4.csv')
        # df_frac.to_csv('frac_cites_over_3.csv')
        # df_frac_norm.to_csv('frac_normalized_cites_over_3.csv')

        # df_complete, df_pi_relative = comp.extract_data(complete_values_file, pi_shap_relative)
        # df_complete, df_pi_relative = comp.sort(df_complete, df_pi_relative, df1_by=['h_index', 'Author Id'],
        #                             df2_by=['Num critical permutations', 'Author Id'])
        # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
        # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
        # hindex_rank, pi_rank = comp.gen_ranks(df_complete, df_pi_relative)
        # print('kendall tau for h-index and shapley relative')
        # comp.calc_kendall_tau(hindex_rank, pi_rank)

        # df_complete, df_pi_fractional = comp.extract_data(complete_values_file, pi_ban_fractional)
        # df_complete, df_pi_fractional = comp.sort(df_complete, df_pi_fractional, df1_by=['h_index', 'Author Id'],
        #                                       df2_by=['Num critical coalitions', 'Author Id'])
        # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
        # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
        # hindex_rank, pi_rank = comp.gen_ranks(df_complete, df_pi_fractional)
        # print('kendall tau for h-index and banzhaf fractional')
        # comp.calc_kendall_tau(hindex_rank, pi_rank)

        # df_complete, df_full = comp.extract_data(complete_values_file, full_file)
        # df_complete, df_full = comp.sort(df_complete, df_full, df1_by=['h_index', 'Author Id'],
        #                                       df2_by=['Full', 'Author Id'])
        # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
        # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
        # hindex_rank, full_rank = comp.gen_ranks(df_complete, df_full)
        # print('kendall tau for h-index and full')
        # comp.calc_kendall_tau(hindex_rank, full_rank)

        # df_complete, df_frac = comp.extract_data(complete_values_file, frac_file)
        # df_complete, df_frac = comp.sort(df_complete, df_frac, df1_by=['h_index', 'Author Id'],
        #                                  df2_by=['Fractional', 'Author Id'])
        # print(df_ban[['Author Id','Num critical groups','banzhaf']].head(10))
        # print(df_shap[['Author Id','Num critical groups','shapley']].head(10))
        # hindex_rank, frac_rank = comp.gen_ranks(df_complete, df_frac)
        # print('kendall tau for h-index and fractional')
        # comp.calc_kendall_tau(hindex_rank, frac_rank)

        # comp.compare_frac_full_pi_partial(df_frac,df_pi, banzhaf=True)

    def calc_tau_for_shapley_star(self, file):

        df, df_shap_star = comp.extract_data(file, file)
        df, df_shap_star = comp.sort(df, df_shap_star, df1_by=['Fractional', 'Author Id'],
                                   df2_by=['Shapley_star', 'Author Id'])
        frac_rank, shap_star_rank = comp.gen_ranks(df, df_shap_star)
        print('kendall tau for Fractional and shapley star')
        tau_frac,p_value_frac=comp.calc_kendall_tau(frac_rank, shap_star_rank)
        df, df_shap_star = comp.sort(df, df_shap_star, df1_by=['Full', 'Author Id'],
                                          df2_by=['Shapley_star', 'Author Id'])
        full_rank, shap_star_rank = comp.gen_ranks(df, df_shap_star)
        print('kendall tau for Full and shapley star')
        tau_full,p_value_full=comp.calc_kendall_tau(full_rank, shap_star_rank)
        df, df_shap_star = comp.sort(df, df_shap_star, df1_by=['citation_to_papers_ratio', 'Author Id'],
                                     df2_by=['Shapley_star', 'Author Id'])
        ratio_rank, shap_star_rank = comp.gen_ranks(df, df_shap_star)
        print('kendall tau for Citation to paper ratio and shapley star')
        tau_cite_pap_ratio,p_value_cite_pap_ratio=comp.calc_kendall_tau(ratio_rank, shap_star_rank)
        df, df_shap_star = comp.sort(df, df_shap_star, df1_by=['Num papers', 'Author Id'],
                                     df2_by=['Shapley_star', 'Author Id'])
        # num_papers_rank, shap_star_rank = comp.gen_ranks(df, df_shap_star)
        # print('kendall tau for number of papers and shapley star')
        # comp.calc_kendall_tau(num_papers_rank, shap_star_rank)
        IF=df['Shapley_star'].sum()
        print('Shapley star sum=IF= '+str(IF))


        record={'JIF':IF,'tau_frac':tau_frac,'p_value_frac':p_value_frac,'tau_full':tau_full,'p_value_full':p_value_full,
                                        'tau_cite_pap_ratio':tau_cite_pap_ratio,'p_value_cite_pap_ratio':p_value_cite_pap_ratio,'% neg values':0}
        return record

    def gini(self,x):
        total = 0
        for i, xi in enumerate(x[:-1], 1):
            total += np.sum(np.abs(xi - x[i:]))
        total2 = 0
        for xi in x[:-1]:
            for xj in x[:-1]:
                total2 += np.abs(xi - xj)

        return total2 / (2*((len(x) ** 2) * np.mean(x)))

    def gini2_pos_vals(self,x):
        ## first sort
        sorted_arr = x.copy()
        sorted_arr.sort()
        n = x.size
        mean=np.mean(x)
        print(mean)
        coef_ = 2. / n
        const_ = (n + 1.) / n
        weighted_sum = sum([(i + 1) * yi for i, yi in enumerate(sorted_arr)])
        return coef_ * weighted_sum / (sorted_arr.sum()) - const_

    def gini_neg(self,x):

        # sorted_arr = x.copy()
        # sorted_arr.sort()
        n = x.size
        total_net=x.sum()
        total_pos_net=x.loc[x>0].sum()
        total_neg_net = abs((x.loc[x<0].sum()))

        total=0
        for xi in x[:-1]:
            for xj in x[:-1]:
                total += np.abs(xi - xj )

        gini=total/(2*(n-1)*(total_pos_net+total_neg_net))
        gini = total / (2 * n  * (total_pos_net + total_neg_net))
        return gini


    def lorenz_curve(self,x1, x2,x3, journal_name):
        X1_lorenz = x1.cumsum()
        X1_lorenz = np.insert(X1_lorenz, 0, 0)
        X1_lorenz[0], X1_lorenz[-1]
        X2_lorenz = x2.cumsum()
        X2_lorenz = np.insert(X2_lorenz, 0, 0)
        X2_lorenz[0], X2_lorenz[-1]
        X3_lorenz = x3.cumsum()
        X3_lorenz = np.insert(X3_lorenz, 0, 0)
        X3_lorenz[0], X3_lorenz[-1]

        fig, ax = plt.subplots(figsize=[6, 6])
        ## scatter plot of Lorenz curve
        ax.scatter(np.arange(X1_lorenz.size) / (X1_lorenz.size - 1), X1_lorenz,
                   marker='x', color='cyan', s=20, label='Shapley star')
        ax.scatter(np.arange(X2_lorenz.size) / (X2_lorenz.size - 1), X2_lorenz,
                   marker='o', color='darkblue', s=20, label='Fractional')
        ax.scatter(np.arange(X3_lorenz.size) / (X3_lorenz.size - 1), X3_lorenz,
                   marker='^', color='red', s=20, label='Full')

        ## line plot of equality
        ax.plot([0, 1], [0, x1.sum()], color='blue')
        ax.plot([0, 1], [0, x3.sum()], color='k')

        # set the x-spine
        ax.spines['left'].set_position('zero')

        # turn off the right spine/ticks
        ax.spines['right'].set_color('none')
        ax.yaxis.tick_left()

        # set the y-spine
        ax.spines['bottom'].set_position('zero')

        # turn off the top spine/ticks
        ax.spines['top'].set_color('none')
        ax.xaxis.tick_bottom()

        plt.xlabel('Cumalative share of authors marginal contribution')
        plt.ylabel('Cumalative IF')
        plt.title('Lorenz curve for authors citation contribution - '+journal_name)

        plt.legend(loc=(0.1, 0.8))

        plt.show()


    def percent_neg_values(self,df):
        shap_neg=sum(df['Shapley_star']<0)*100/len(df)
        return shap_neg






if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    comp=Comparison()
    journals = Journals()

    journals = Journals()
    df_stats=pd.DataFrame()
    for current_journal in journals.dirsIS:
        if current_journal=='test':
            continue
        for file in os.listdir(path=journals.file_path + current_journal):
            if not file.startswith('shap_full_star_all_authors.csv'):
                continue
            print('now creating for {}'.format(current_journal))
            obj_path = os.path.join(journals.file_path + current_journal, file)
            df_shap = pd.read_csv(obj_path)
            df_shap.reset_index(inplace=True)
            record=comp.calc_tau_for_shapley_star(obj_path)
            per = comp.percent_neg_values(df_shap)
            print('per is {}%'.format(per))
            record['% neg values']=per
            record['journal name']=current_journal
            df_stats=df_stats.append(record, ignore_index=True)
    df_stats.set_index('journal name', inplace=True)
    df_stats.to_csv(journals.file_path+'\\'+'shap_full_star_stats.csv')

    # file_path = 'C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\'
    # journal_name = journals.dirsIS[9]

    # file_name = journal_name + '\\' + 'shap_full_star_all_authors.csv'  # international journal of law...
    # orig_file_name=file_path+journal_name+'\\'+journal_name+'.csv'


            # df, df_papers_=comp.extract_data(file_path+file_name, orig_file_name)
            # num_papers=len(df_papers_)

    exit(0)
    df['Full_normalized']=df['Full']/num_papers
    df['Fractional_normalized'] = df['Fractional'] / num_papers
    df.to_csv(file_path+journal_name+'\\'+'shap_full_star_all_authors.csv')

    df['Shapley_star'].values.sort()
    gini=comp.gini(df['Shapley_star'].values)
    print('Shapley_star gini is {}'.format(gini))
    gini = comp.gini_neg(df['Shapley_star'])
    print('Shapley_star gini_neg is {}'.format(gini))
    shap_values_sorted=df['Shapley_star'].values.copy()
    # comp.lorenz_curve(df['Shapley_star'].values)
    df['Fractional_normalized'].values.sort()
    frac_values_sorted=df['Fractional_normalized'].values.copy()
    gini = comp.gini(df['Fractional_normalized'].values)
    print('Fractional_normalized gini is {}'.format(gini))
    gini = comp.gini_neg(df['Fractional_normalized'])
    print('Fractional_normalized gini_neg is {}'.format(gini))
    df['Full_normalized'].values.sort()
    full_values_sorted = df['Full_normalized'].values.copy()
    gini = comp.gini(df['Full_normalized'].values)
    print('Full_normalized gini is {}'.format(gini))
    gini = comp.gini_neg(df['Full_normalized'])
    print('Full_normalized gini_neg is {}'.format(gini))

    # df['Shapley_star_offset'].values.sort()
    # gini = comp.gini(df['Shapley_star_offset'].values)
    # print('Shapley_star_offset gini is {}'.format(gini))
    # gini = comp.gini_neg(df['Shapley_star_offset'])
    # print('Shapley_star_offset gini_neg is {}'.format(gini))
    # shap_values_sorted = df['Shapley_star_offset'].values.copy()

    comp.lorenz_curve(shap_values_sorted,frac_values_sorted,full_values_sorted,journal_name)