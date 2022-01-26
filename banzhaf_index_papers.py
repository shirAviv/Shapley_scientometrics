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

            paper_count = len(author_papers)

            id_location = list(author_data['Author(s) ID'].str.split(';').values)[0].index(author)
            author_name = list(author_data['Authors'].str.split(',').values)[0][id_location].strip()
            author_coauthors = pd.DataFrame(author_data.loc[:, 'Author(s) ID']).copy()
            record = {'Author Name': author_name, 'Author Id': author, 'Num papers': paper_count,
                      'Num citations': author_citations, 'Coauthors': author_coauthors['Author(s) ID'].values}
            authors_df = authors_df.append(record, ignore_index=True)
        return authors_df

    def get_subsets(self,df):
        ids=list(df.index)
        subsets = chain.from_iterable(combinations(ids, r) for r in range(10, 11))
        return subsets

    def calc_subset_value(self, df, subset):
        total_val=0
        papers_val=dict()
        for id in subset:
            papers_val[id]=0
            paper_data=df.iloc[id,:]
            papers_contrib=0

            papers_contrib+=paper_data['Cited by']
            papers_val[id]+=papers_contrib
            total_val+=papers_contrib
                # else:
                #     print('co author found')
        value=total_val/num_papers
        # print(value)
        if value>self.q4_quota:
            print('over quota - subset {}'.format(subset))
            for paper_id,paper_val in papers_val.items():
                if value-(paper_val/num_papers)<self.q4_quota:
                    print('paper {} is critical'.format(paper_id))
                    # authors_df.loc[authors_df['Author Id'] == author,'Num critical coalitions']+=1

                    df_for_banzhaf.loc[paper_id,'Num critical coalitions']+=1


    def iterate_subsets(self,df, subsets):
        for subset in subsets:
            self.calc_subset_value(df, subset)

    def calc_authors_index_from_papers(self,df):
        authors = set(''.join(list(df.loc[:, 'Author(s) ID'])).split(';'))
        authors.remove('')
        authors_df = pd.DataFrame(columns=['Author Name', 'Author Id', 'Num papers', 'Num citations', 'Author contribution'])
        index = 0

        for author in authors:
            author_contrib=0
            author_data = df[df['Author(s) ID'].str.contains(author)]
            author_papers = author_data.index.values
            author_citations = author_data.loc[:, 'Cited by'].values

            paper_count = len(author_papers)

            id_location = list(author_data['Author(s) ID'].str.split(';').values)[0].index(author)
            author_name = list(author_data['Authors'].str.split(',').values)[0][id_location].strip()
            for idx, paper_citations in enumerate(author_citations):
                coauthors = author_data['Author(s) ID'].iloc[idx].split(';')
                coauthors.remove('')
                num_coauthors = len(coauthors)

                # if  not author_id in coauthors_set:
                author_contrib += paper_citations / num_coauthors

            record = {'Author Name': author_name, 'Author Id': author, 'Num papers': paper_count,
                      'Num citations': author_citations, 'Author contribution': author_contrib}
            authors_df = authors_df.append(record, ignore_index=True)
        return authors_df

if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    file_path='C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\Shapley_index\\ASLIB_Journal_of_info_manage\\ASLIB_Journal_of_info_manage_2018-2021_scopus.csv'
    bi=Banzhaf_index()
    df=bi.extract_data(file_path)
    num_papers=len(df)
    df_for_banzhaf=bi.remove_low_citation_papers(df)

    df_for_banzhaf['Num critical coalitions']=0
    subsets=bi.get_subsets(df_for_banzhaf)
    bi.iterate_subsets(df_for_banzhaf,subsets)
    print(df_for_banzhaf)
    authors_df=bi.calc_authors_index_from_papers(df_for_banzhaf)
    authors_df=authors_df.sort_values(by="Author contribution",ascending=False)
    print(authors_df)
    authors_df.to_csv('authors_from_papers_subsets_10.csv')
    end_time = datetime.now()
    print(start_time)
    print(end_time)



