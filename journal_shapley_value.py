import pandas as pd
import itertools
from scipy import misc
import math
import numpy as np
from pybliometrics.scopus import AuthorRetrieval




class Journal_shapley:
    def extract_data(self, file):
        df=pd.read_csv(file)
        # df=df.loc[df['Document Type'].isin(['Article','Review'])]
        print(df.head())
        return df

    def remove_low_citation_papers(self, df):
        df1=df[df.loc[:,'Cited by']>13].copy()
        return df1

    def remove_authors_with_low_num_papers(self,df):
        df1=df.copy()
        papers_for_removal=set()
        for idx, paper in df.iterrows():
            authors_ids=paper['Authors IDs'].split(';')
            authors_ids.remove('')
            remove=False
            for author in authors_ids:
                num_papers_by_author=len(df[df['Authors IDs'].str.contains(author)])
                if num_papers_by_author<2:
                    remove=True
                    break
            if remove:
                papers_for_removal.add(idx)

        df1.drop(papers_for_removal, inplace=True)
        df1.reset_index(inplace=True)
        return df1



    def calc_authors_shapley_num_papers(self,df):
        authors=set(''.join(list(df.loc[:,'Authors IDs'])).split(';'))
        authors.remove('')
        authors_df=pd.DataFrame(columns=['Author Name', 'Author Id','Num papers', 'Num citations', 'Num coauthors','Shapley - Num papers','Shapley - Num citations'])
        index=0
        authors_count=len(authors)

        for author in authors:
            papers_and_citations=dict()
            author_data=df[df['Authors IDs'].str.contains(author)]
            author_papers=author_data.index.values
            author_citations=author_data.loc[:,'Cited by'].values

            paper_count=len(author_papers)

            id_location = list(author_data['Authors IDs'].str.split(';').values)[0].index(author)
            author_name = list(author_data['Authors'].str.split(',').values)[0][id_location].strip()
            author_coauthors=pd.DataFrame(author_data.loc[:,'Authors IDs']).copy()
            author_coauthors['num coauthors']=author_coauthors.apply(lambda row: pd.Series(row['Authors IDs'].count(';')-1),axis=1)
            if (index<1000):
                print('author {}, count papers {}, coauthors count {}, citations {}'.format(author,paper_count,author_coauthors['num coauthors'].values, author_citations))
                index+=1
                if (np.sum(author_coauthors['num coauthors'].values)==0):
                    self.calc_auth_shapley_for_single_authored_papers(len(author_papers),authors_count)
                shaply_papers, shapley_citations=self.calc_shapley(authors_count,author_coauthors,citation_data=author_citations)
                record={'Author Name' :author_name, 'Author Id': author,'Num papers':paper_count, 'Num citations':author_citations, 'Num coauthors':author_coauthors['num coauthors'].values,'Shapley - Num papers':shaply_papers,'Shapley - Num citations':shapley_citations}
                authors_df=authors_df.append(record,ignore_index=True)
                # if (np.sum(author_coauthors['num coauthors'].values)==paper_count*2):
                #     self.calc_auth_shapley_all_papers_collaboration_with_single_author(paper_count,authors_count)
        print('num authors {}'.format(len(authors_df)))

        print('num papers {}'.format(len(df)))
        sum_shapley_papers=authors_df['Shapley - Num papers'].sum()
        print('sum shapley num papers {}'.format(sum_shapley_papers))

        return authors_df

    def calc_authors_shapley_num_citations(self,df):
        authors=set(''.join(list(df.loc[:,'Authors IDs'])).split(';'))
        authors.remove('')
        authors_df=pd.DataFrame(columns=['Author Name', 'Author Id','Num papers', 'Num citations', 'Num coauthors','Shapley - Num citations'])
        index=0

        for author in authors:

            author_data=df[df['Authors IDs'].str.contains(author)]
            author_papers=author_data.index.values
            author_citations=author_data.loc[:,'Cited by'].values

            paper_count=len(author_papers)

            id_location = list(author_data['Authors IDs'].str.split(';').values)[0].index(author)
            author_name = list(author_data['Authors'].str.split(',').values)[0][id_location].strip()
            author_coauthors=pd.DataFrame(author_data.loc[:,'Authors IDs']).copy()
            author_coauthors['num coauthors']=author_coauthors.apply(lambda row: pd.Series(row['Authors IDs'].count(';')-1),axis=1)
            if (index<1000):
                print('author {}, count papers {}, coauthors count {}, citations {}'.format(author,paper_count,author_coauthors['num coauthors'].values, author_citations))
                index+=1
                # if (np.sum(author_coauthors['num coauthors'].values)==0):
                #     self.calc_auth_shapley_for_single_authored_papers(len(author_papers),len(authors))
                shaply_papers, shapley_citations=self.calc_shapley(len(authors),author_coauthors,citation_data=author_citations)
                record={'Author Name' :author_name, 'Author Id': author,'Num papers':paper_count, 'Num citations':author_citations, 'Num coauthors':author_coauthors['num coauthors'].values,'Shapley - Num papers':shaply_papers,'Shapley - Num citations':shapley_citations}
                authors_df=authors_df.append(record,ignore_index=True)
                # if (np.sum(author_coauthors['num coauthors'].values)==paper_count*2):
                #     self.calc_auth_shapley_all_papers_collaboration_with_single_author(paper_count,authors_count)
        print('num authors {}'.format(len(authors_df)))
        num_papers=len(df)
        print('num papers {}'.format(num_papers))
        num_citations = df['Cited by'].sum()
        # for paper in papers_set:
        #     num_citations += df[df.index == paper, "Cited by"]
        print('num citations {}'.format(num_citations))
        sum_shapley_citations=authors_df['Shapley - Num citations'].sum()
        print('sum shapley citations {}'.format(sum_shapley_citations))
        return authors_df


    def calc_shapley_sub_group(self, num_journal_authors, sub_group_size, author_coauthors, citation_data=None):
        num_combinations = self.calc_num_combinations(num_journal_authors - 1, sub_group_size)
        num_combinations_without_coauthors=0
        marginal_citation_contrib=0
        for idx,num_coauthors in enumerate(author_coauthors['num coauthors']):
            if (num_coauthors<num_journal_authors):
                num_combinations_without_coauthors_one_paper=self.calc_num_combinations(num_journal_authors-1-num_coauthors,sub_group_size)
                if (len(citation_data)>0):
                    num_citations_for_paper=citation_data[idx]
                    marginal_citation_contrib_one_paper=num_citations_for_paper*num_combinations_without_coauthors_one_paper
            else:
                num_combinations_without_coauthors_one_paper=0
                marginal_citation_contrib_one_paper=0
            num_combinations_without_coauthors+=num_combinations_without_coauthors_one_paper
            marginal_citation_contrib+=marginal_citation_contrib_one_paper
        shapley_sub_group=num_combinations_without_coauthors/num_combinations
        shapley_sub_group_citation=marginal_citation_contrib/num_combinations
        return shapley_sub_group, shapley_sub_group_citation

    def calc_shapley(self, num_journal_authors, author_coauthors, citation_data=None):
        full_marginal_cont = 0
        full_marginal_cont_citation=0
        for sub_group_size in range(num_journal_authors):
            marginal_cont, marginal_cont_citation = self.calc_shapley_sub_group(num_journal_authors, sub_group_size, author_coauthors, citation_data)
            full_marginal_cont += marginal_cont
            if (len(citation_data)>0):
                full_marginal_cont_citation+=marginal_cont_citation
        shapley = full_marginal_cont / num_journal_authors
        shapley_citation=full_marginal_cont_citation/num_journal_authors
        print(shapley)
        print(shapley_citation)
        return shapley, shapley_citation

        # authors_ids=df.loc['Authors IDs'].to_list()
    def calc_auth_shapley_for_single_authored_papers(self, num_papers_by_author,num_journal_authors):
        # comb=self.calc_total_combinations(num_journal_authors)
        full_marginal_cont=0
        for i in range(num_journal_authors):
            num_combinations=self.calc_num_combinations(num_journal_authors - 1, i)
            marginal_cont=num_papers_by_author*num_combinations/num_combinations
            full_marginal_cont+=marginal_cont
        shapley=full_marginal_cont/num_journal_authors
        print('shapley is {}'.format(shapley))

    def calc_auth_shapley_all_papers_collaboration_with_single_author(self, num_papers_by_author, num_journal_authors):
        full_marginal_cont = 0
        num_pivot_author_combination=0
        for i in range(num_journal_authors):
            num_total_combinations = self.calc_num_combinations(num_journal_authors - 1, i)
            if (i>0):
                num_pivot_author_combination=self.calc_num_combinations(num_journal_authors-2,i-1)
            marginal_cont = num_papers_by_author * (num_total_combinations-num_pivot_author_combination) / num_total_combinations
            full_marginal_cont += marginal_cont
        shapley = full_marginal_cont / num_journal_authors
        print('shapley is {}'.format(shapley))

    def count_semi_colon(self,authors_str):
        count=authors_str.count(';')
        return count

    def calc_num_combinations(self,n,comb_size):
        num_comb=math.comb(n, comb_size)
        # print(num_comb)
        return num_comb

    def calc_total_combinations(self, n):
        sum_combinations = 0
        for i in range(n):
            sum_combinations += 1/js.calc_num_combinations(n - 1, i)
            # print(sum_combinations)
        return sum_combinations

    def get_authors_hindex_affiliation(self, df):
        df['h_index']=0
        df['affiliation']=''
        df['affiliation_department']=''
        authors=df['Author Id']
        for author in authors:
            affiliation_dept=''
            affiliation_uni=''
            au = AuthorRetrieval(author)
            hIndex=au.h_index
            if (au!=None and au.affiliation_current!=None):
                affiliation_uni=au.affiliation_current[0].parent_preferred_name
                if (affiliation_uni==None):
                    affiliation_uni=au.affiliation_current[0].preferred_name
                else:
                    affiliation_dept=au.affiliation_current[0].preferred_name
            df.loc[df['Author Id'] == author, 'h_index'] = hIndex
            df.loc[df['Author Id'] == author, 'affiliation'] = affiliation_uni
            df.loc[df['Author Id'] == author, 'affiliation_department'] = affiliation_dept





if __name__ == '__main__':
    # file_path='C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\PUCScopus_2019.csv'
    file_path = 'C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\ASLIB_Journal_of_info_manage\\'
    file_path = file_path + 'power_index\\ban_4_16_005_cites_over_3_q4.csv'

    js=Journal_shapley()
    df=js.extract_data(file_path)
    js.get_authors_hindex_affiliation(df)
    exit(0)

    df_for_shapley_papers=js.remove_authors_with_low_num_papers(df)
    authors_df=js.calc_authors_shapley_num_papers(df_for_shapley_papers)
    authors_df=authors_df.sort_values(by="Shapley - Num papers",ascending=False)

    # js.get_authors_hindex_affiliation(authors_df)
    authors_df.to_csv('C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\PUCScopus_2019_Shapley_num_papers.csv')

    df_for_shapley_citation=js.remove_low_citation_papers(df)
    authors_df=js.calc_authors_shapley_num_citations(df_for_shapley_citation)
    authors_df=authors_df.sort_values(by="Shapley - Num citations",ascending=False)
    # js.get_authors_hindex_affiliation(authors_df)
    authors_df.to_csv('C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\PUCScopus_2019_Shapley_citations.csv')
    # js.calc_total_combinations(21)
