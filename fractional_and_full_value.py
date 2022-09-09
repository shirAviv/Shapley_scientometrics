import pandas as pd
import itertools
from scipy import misc
import math
import numpy as np
# from pybliometrics.scopus import AuthorRetrieval
from itertools import chain,combinations
from datetime import date,datetime,timedelta
import random



class Fractional_And_Full_value:
    q4_quota=0.4
    q2_quota=2.2

    def extract_data(self, file):
        df=pd.read_csv(file)
        df=df.loc[df['Document Type'].isin(['Article','Review'])]
        print(df.head())
        return df

    def remove_low_citation_papers(self, df):
        df1=df[df.loc[:,'Cited by']>0].copy()
        return df1


    def get_authors_df(self,df):
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

    def get_single_author_fractional_value(self,author, author_data):
        author_contrib = 0
        author_num_papers=len(author_data['papers'].values[0])
        for idx, paper_citations in enumerate(author_data['Num citations'].values[0]):
            # count_coauthors_in_current_subset=0
            coauthors_set = set()
            coauthors = author_data['Coauthors'].iloc[0][idx].split(';')
            coauthors.remove('')
            num_coauthors = len(coauthors)
            author_contrib += paper_citations / (num_coauthors)
        # author_contrib=author_contrib/author_num_papers
        return author_contrib

    def get_authors_fractional_values(self,authors_df):
        authors = set(authors_df.loc[:, 'Author Id'])
        for author in authors:
            author_data = authors_df[authors_df['Author Id'] == author]

            author_fractional_value=self.get_single_author_fractional_value(author,author_data)
            authors_df.loc[authors_df['Author Id'] == author, 'Fractional'] = author_fractional_value

    def check_critical(self,coalition, authors_df, current_author):
        total_val = 0
        # authors_val = dict()
        for author_id in coalition:
            # authors_val[author_id] = 0
            author_data = authors_df[authors_df['Author Id'] == author_id]
            # if author_data['Num papers'].values[0] > 1:
            #     print('more than 1 paper')
            authors_contrib = 0
            for idx, paper_citations in enumerate(author_data['Num citations']):
                # count_coauthors_in_current_subset=0
                coauthors_set = set()
                coauthors = author_data['Coauthors'].iloc[0][idx].split(';')
                coauthors.remove('')
                coauthors.remove(author_id)
                coauthors_set.update(set(coauthors))
                num_coauthors = len(coauthors_set)
                count_coauthors_in_current_subset = len(coauthors_set.intersection(coalition))

                # if  not author_id in coauthors_set:
                authors_contrib += paper_citations[0] / (count_coauthors_in_current_subset + 1)
                if current_author==author_id:
                    current_author_contrib=authors_contrib
                # authors_val[author_id] += authors_contrib
                total_val += authors_contrib
                # else:
                #     print('co author found')
        value = total_val / num_papers
        if value>self.q2_quota:
            print('over quota - subset {}'.format(coalition))
            # for author,author_val in authors_val.items():
            if value-(current_author_contrib/num_papers)<self.q2_quota:
                # print('author {} is critical'.format(current_author))
                authors_df.loc[authors_df['Author Id'] == current_author,'Num critical coalitions']+=1
                return True
        return False

    def get_single_author_full_value(self,author_data):
        author_contrib = 0
        author_num_papers=len(author_data['papers'].values[0])
        for idx, paper_citations in enumerate(author_data['Num citations'].values[0]):
            author_contrib += paper_citations
        # author_contrib = author_contrib / author_num_papers
        author_contrib=author_contrib
        return author_contrib

    def get_authors_full_values(self,authors_df):
        authors = set(authors_df.loc[:, 'Author Id'])
        for author in authors:
            author_data = authors_df[authors_df['Author Id'] == author]

            author_fractional_value = self.get_single_author_full_value(author_data)
            authors_df.loc[authors_df['Author Id'] == author, 'Full'] = author_fractional_value


if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    file_path='C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\ASLIB_Journal_of_info_manage\\ASLIB_Journal_of_info_manage_2018-2021_scopus.csv'
    ffv=Fractional_And_Full_value()
    df=ffv.extract_data(file_path)
    num_papers=len(df)
    print('num papers is {}'.format(num_papers))

    authors_df=ffv.get_authors_df(df)
    authors_df['fractional value'] = 0
    ffv.get_authors_fractional_values(authors_df)
    authors_df = authors_df.sort_values(by="fractional value", ascending=False)
    print(authors_df)
    authors_df.to_csv('all_authors_fractional_values_cites_over_3.csv')

    # authors_df['Full']=0
    # ffv.get_authors_full_values(authors_df)
    # authors_df = authors_df.sort_values(by="Full", ascending=False)
    # print(authors_df)
    # authors_df.to_csv('all_authors_full_values_cites_over_3.csv')
    end_time=datetime.now()
    print(end_time)



