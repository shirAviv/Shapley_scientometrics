import pandas as pd
import itertools
from scipy import misc
import math
import numpy as np
from pybliometrics.scopus import AuthorRetrieval
from itertools import chain,combinations
from datetime import date,datetime,timedelta
import random

class Analysis:
    def get_complete_authors_df(self,df):
        authors = set(''.join(list(df.loc[:, 'Author(s) ID'])).split(';'))
        authors.remove('')
        authors_df = pd.DataFrame(columns=['Author Name', 'Author Id', 'Num papers', 'Num citations', 'Coauthors'])
        index = 0

        for author in authors:
            author_data = df[df['Author(s) ID'].str.contains(author)]
            author_papers = author_data.index.values
            author_citations = author_data.loc[:, 'Cited by'].values
            zero_citations=True
            # for citation in author_citations:
            #     if citation>3:
            #         zero_citations=False
            #         break
            # if zero_citations:
            #     continue
            paper_count = len(author_papers)

            id_location = list(author_data['Author(s) ID'].str.split(';').values)[0].index(author)
            author_name = list(author_data['Authors'].str.split(',').values)[0][id_location].strip()
            author_coauthors = pd.DataFrame(author_data.loc[:, 'Author(s) ID']).copy()
            record = {'Author Name': author_name, 'Author Id': author, 'Num papers': paper_count,
                      'Num citations': author_citations, 'Coauthors': author_coauthors['Author(s) ID'].values}
            authors_df = authors_df.append(record, ignore_index=True)
        return authors_df

    def analyse(self, df):
        # df_by = ['Num critical coalitions', 'Author Id']
        df_by = ['Full', 'Author Id']
        df_sorted=df.sort_values(by=df_by, ascending=[False,False], ignore_index=True, key=None)
        top_20_per_of_analysed_authors=df_sorted[0:30]
        df_sorted_sum=df_sorted['Full'].sum()
        top_20_per_of_analysed_authors_sum=top_20_per_of_analysed_authors['Full'].sum()
        top_20_per_of_all_authors=df_sorted[0:103]
        top_20_per_of_all_authors_sum=top_20_per_of_all_authors['Full'].sum()
        all_authors_sum=1936
        print('Full contribution: top 20% of analysed authors (30) sum contributions {}, percentage of contribution {}'.format(top_20_per_of_analysed_authors_sum, 100*(top_20_per_of_analysed_authors_sum/df_sorted_sum)))
        print('Full contribution: top 20% of all authors (102) sum contributions {}, percentage of contribution {}'.format(top_20_per_of_all_authors_sum, 100*(top_20_per_of_all_authors_sum/all_authors_sum)))
        # print(top_20_sum/df_sorted_sum)
        # print(top_20_sum / all_authors_sum)

        # print(top_20_per_of_analysed_authors['Author Name'].values)

        df_by = ['Shap Full', 'Author Id']
        df_sorted = df.sort_values(by=df_by, ascending=[False, False], ignore_index=True, key=None)
        top_20_per_of_analysed_authors = df_sorted[0:30]
        df_sorted_sum = df_sorted['Shap Full'].sum()
        top_20_per_of_analysed_authors_sum = top_20_per_of_analysed_authors['Shap Full'].sum()
        # 175 authors with 0 cites, 176 not in selected authors, estimated value is the lowest shapley of selected authors
        all_authors_sum=175*0+176*0.022365017+df_sorted_sum
        top_20_per_of_all_authors = df_sorted[0:103]
        top_20_per_of_all_authors_sum = top_20_per_of_all_authors['Shap Full'].sum()
        print(
            'Shapley Full contribution: top 20% of analysed authors (30) sum contributions {}, percentage of contribution {}'.format(
                top_20_per_of_analysed_authors_sum, 100 * (top_20_per_of_analysed_authors_sum / df_sorted_sum)))
        print(
            'Shapley Full contribution: top 20% of all authors (102) sum contributions {}, percentage of contribution {}'.format(
                top_20_per_of_all_authors_sum, 100 * (top_20_per_of_all_authors_sum / all_authors_sum)))

        # print(top_20_sum / df_sorted_sum)
        # print(top_20_sum / all_authors_sum)
        # print(top_20_per_of_analysed_authors['Author Name'].values)

        df_by = ['Fractional', 'Author Id']
        df_sorted = df.sort_values(by=df_by, ascending=[False, False], ignore_index=True, key=None)
        top_20_per_of_analysed_authors = df_sorted[0:30]
        df_sorted_sum = df_sorted['Fractional'].sum()
        top_20_per_of_analysed_authors_sum = top_20_per_of_analysed_authors['Fractional'].sum()
        all_authors_sum=729
        top_20_per_of_all_authors = df_sorted[0:103]
        top_20_per_of_all_authors_sum = top_20_per_of_all_authors['Fractional'].sum()
        print(
            'Fractional contribution: top 20% of analysed authors (30) sum contributions {}, percentage of contribution {}'.format(
                top_20_per_of_analysed_authors_sum, 100 * (top_20_per_of_analysed_authors_sum / df_sorted_sum)))
        print(
            'Fractional contribution: top 20% of all authors (102) sum contributions {}, percentage of contribution {}'.format(
                top_20_per_of_all_authors_sum, 100 * (top_20_per_of_all_authors_sum / all_authors_sum)))

        # print(top_20_sum / df_sorted_sum)
        # print(top_20_sum / all_authors_sum)
        # print(top_20_per_of_analysed_authors['Author Name'].values)

        df_by = ['Shap Fractional', 'Author Id']
        df_sorted = df.sort_values(by=df_by, ascending=[False, False], ignore_index=True, key=None)
        top_20_per_of_analysed_authors = df_sorted[0:30]
        df_sorted_sum = df_sorted['Shap Fractional'].sum()
        top_20_per_of_analysed_authors_sum = top_20_per_of_analysed_authors['Shap Fractional'].sum()
        # 175 authors with 0 cites, 176 not in selected authors, estimated value is the lowest shapley of selected authors
        all_authors_sum=175*0+176*0.009104565+df_sorted_sum
        top_20_per_of_all_authors = df_sorted[0:103]
        top_20_per_of_all_authors_sum = top_20_per_of_all_authors['Shap Fractional'].sum()
        print(
            'Shapley Fractional contribution: top 20% of analysed authors (30) sum contributions {}, percentage of contribution {}'.format(
                top_20_per_of_analysed_authors_sum, 100 * (top_20_per_of_analysed_authors_sum / df_sorted_sum)))
        print(
            'Shapley Fractional contribution: top 20% of all authors (102) sum contributions {}, percentage of contribution {}'.format(
                top_20_per_of_all_authors_sum, 100 * (top_20_per_of_all_authors_sum / all_authors_sum)))

        # print(top_20_sum / df_sorted_sum)
        # print(top_20_sum / all_authors_sum)
        # print(top_20_per_of_analysed_authors['Author Name'].values)


if __name__ == '__main__':
    analysis=Analysis()
    file_path = 'C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\ASLIB_Journal_of_info_manage\\'
    # pi_ban_full=file_path+'power_index\\ban_full_4_18_005_cites_over_3_q4.csv'
    complete_values_file=file_path+'shapley_value\\authors_cites_over_3_complete.csv'
    aslib_journal_file='ASLIB_Journal_of_info_manage_2018-2021_scopus.csv'
    df_journal = pd.read_csv(file_path+aslib_journal_file)
    num_papers=len(df_journal)
    print('num papers is {}'.format(num_papers))
    df_authors=analysis.get_complete_authors_df(df_journal)
    # df_authors.to_csv(file_path+'complete_authors.csv')

    df = pd.read_csv(complete_values_file)

    analysis.analyse(df)


