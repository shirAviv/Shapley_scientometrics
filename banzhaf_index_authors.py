import pandas as pd
import itertools
from scipy import misc
import math
import numpy as np
from pybliometrics.scopus import AuthorRetrieval
from itertools import chain,combinations
from datetime import date,datetime,timedelta



class Banzhaf_index:
    q4_quota=0.4
    q2_quota=2.2


    def extract_data(self, file):
        df=pd.read_csv(file)
        df=df.loc[df['Document Type'].isin(['Article','Review'])]
        print(df.head())
        return df

    def remove_low_citation_papers(self, df):
        df1=df[df.loc[:,'Cited by']>10].copy()
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
            zero_citations = True
            for citation in author_citations:
                if citation > 9:
                    zero_citations = False
                    break
            if zero_citations:
                continue
            paper_count = len(author_papers)

            id_location = list(author_data['Author(s) ID'].str.split(';').values)[0].index(author)
            author_name = list(author_data['Authors'].str.split(',').values)[0][id_location].strip()
            author_coauthors = pd.DataFrame(author_data.loc[:, 'Author(s) ID']).copy()
            record = {'Author Name': author_name, 'Author Id': author, 'Num papers': paper_count,
                      'Num citations': author_citations, 'Coauthors': author_coauthors['Author(s) ID'].values}
            authors_df = authors_df.append(record, ignore_index=True)
        return authors_df


    def get_subsets(self,df):
        authors_ids=list(df['Author Id'])
        subsets = chain.from_iterable(combinations(authors_ids, r) for r in range(6, 7))
        return subsets

    def calc_subset_value(self, authors_df, subset):
        total_val=0
        authors_val=dict()
        for author_id in subset:
            authors_val[author_id]=0
            author_data=authors_df[authors_df['Author Id'] == author_id]
            if author_data['Num papers'].values[0]>1:
                print('more than 1 paper')
            authors_contrib=0
            for idx,paper_citations in enumerate(author_data['Num citations']):
                # count_coauthors_in_current_subset=0
                coauthors_set = set()
                coauthors = author_data['Coauthors'].iloc[0][idx].split(';')
                coauthors.remove('')
                coauthors.remove(author_id)
                coauthors_set.update(set(coauthors))
                num_coauthors = len(coauthors_set)
                count_coauthors_in_current_subset=len(coauthors_set.intersection(subset))

                # if  not author_id in coauthors_set:
                # authors_contrib+=paper_citations[0]/(count_coauthors_in_current_subset+1)
                authors_contrib+=paper_citations[0]/(num_coauthors+1)

            authors_val[author_id]+=authors_contrib
            total_val+=authors_contrib
                # else:
                #     print('co author found')
        value=total_val/num_papers
        # print(value)
        if value>self.q4_quota:
            print('over quota - subset {}'.format(subset))
            for author,author_val in authors_val.items():
                if value-(author_val/num_papers)<self.q4_quota:
                    print('author {} is critical'.format(author))
                    authors_df.loc[authors_df['Author Id'] == author,'Num critical coalitions']+=1

    def iterate_subsets(self,authors_df, subsets):
        counter=0
        for subset in subsets:
            self.calc_subset_value(authors_df, subset)
            counter+=1
        print("count subsets is {}".format(counter))

if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    file_path='C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\ASLIB_Journal_of_info_manage\\ASLIB_Journal_of_info_manage_2018-2021_scopus.csv'
    bi=Banzhaf_index()
    df = bi.extract_data(file_path)
    num_papers = len(df)
    print('num papers is {}'.format(num_papers))
    # df_for_banzhaf=bi.remove_low_citation_papers(df)
    df_for_banzhaf = df
    authors_df = bi.get_authors_df(df_for_banzhaf)
    authors_df['Num critical coalitions'] = 0
    authors_df['banzhaf'] = 0
    subsets=bi.get_subsets(authors_df)
    bi.iterate_subsets(authors_df,subsets)
    authors_df = authors_df.sort_values(by="Num critical coalitions", ascending=False)
    print(authors_df)
    authors_df.to_csv('authors_power_index_subsets_6.csv')

    print(authors_df)
    # authors_df=authors_df.sort_values(by="Num citations",ascending=False)
    end_time = datetime.now()
    print(start_time)
    print(end_time)



