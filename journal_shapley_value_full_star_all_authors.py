import pandas as pd
import os
import itertools
from scipy import misc
import math
import numpy as np
# from pybliometrics.scopus import AuthorRetrieval
import random
from datetime import date,datetime,timedelta
from fractional_and_full_value import Fractional_And_Full_value
from journals import Journals



class Journal_shapley_value_full_star:
    eps = 0.05
    delta = 0.05
    all_permutations = dict()
    duplicate_permutations_counter = 0
    all_coalitions = dict()
    duplicate_coalitions_counter = 0
    num_pcs=15

    def init_permutations(self):
        self.duplicate_permutations_counter = 0
        for idx in range(0, 500):
            self.all_permutations[idx] = list()
        self.duplicate_coalitions_counter = 0
        for idx in range(0, 100):
            self.all_coalitions[idx] = set()

    def extract_data(self, file):
        df=pd.read_csv(file)
        df=df.loc[df['Document Type'].isin(['Article','Review'])]
        df['Cited by']=df['Cited by'].fillna(0)
        print(df.head())
        return df

    '''
    def remove_low_citation_papers(self, df):
        df1=df[df.loc[:,'Cited by']>10].copy()
        return df1
    '''
    def get_authors_df(self,df):
        authors = set(''.join(list(df.loc[:, 'Author(s) ID'])).split(';'))
        authors.remove('')
        authors_df = pd.DataFrame(columns=['Author Name', 'Author Id', 'papers','Num papers', 'Num citations', 'Coauthors'])
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
            record = {'Author Name': author_name, 'Author Id': author, 'papers': author_papers,'Num papers':paper_count,
                      'Num citations': author_citations, 'Coauthors': author_coauthors['Author(s) ID'].values}
            authors_df = authors_df.append(record, ignore_index=True)
        return authors_df

    def gen_permutation(self,authors_df, size=0):
        permutation = list(authors_df.loc[:, 'Author Id'])
        exists = True
        while exists:
            random.shuffle(permutation)
            # for author in authors:
            #     val=random.getrandbits(1)
            #     if val:
            #         permutation.append(author)
            exists = self.does_permutation_exist(permutation)
        return permutation

    def does_permutation_exist(self,permutation):
        permutation_size=len(permutation)
        permutations_of_size=self.all_permutations[permutation_size]
        if permutation in permutations_of_size:
            self.duplicate_permutations_counter+=1
            # print('permutation already exists')
            return True
        else:
            self.all_permutations[permutation_size].append(permutation)
            return False


    '''
    def confidence_shapley(self,df_authors, column_name, permutation_size=0):
        authors = set(df_authors.loc[:, 'Author Id'])
        for author in authors:
            self.init_permutations()
            shapley,confidence_interval_min,confidence_interval_max=self.confidence_shapley_single_author(df_authors,author, permutation_size)
            authors_df.loc[authors_df['Author Id'] == author, column_name] = shapley
            print('for author {} shapley is {} and interval is [{},{}]'.format(author,shapley,confidence_interval_min,confidence_interval_max))
            print('num dups created {}'.format(self.duplicate_permutations_counter))
    '''

    def value_single_permutation_frac(self,permutation, authors_df, current_author):
        total_val = 0
        # authors_val = dict()
        for author_id in permutation:
            # authors_val[author_id] = 0
            author_data = authors_df[authors_df['Author Id'] == author_id]
            # if author_data['Num papers'].values[0] > 1:
            #     print('more than 1 paper')
            authors_contrib = 0
            for idx, paper_citations in enumerate(author_data['Num citations'].values[0]):
                # count_coauthors_in_current_subset=0
                coauthors_set = set()
                coauthors = author_data['Coauthors'].iloc[0][idx].split(';')
                coauthors.remove('')
                coauthors.remove(author_id)
                coauthors_set.update(set(coauthors))
                num_coauthors = len(coauthors_set)
                count_coauthors_in_current_subset = len(coauthors_set.intersection(permutation))

                # if  not author_id in coauthors_set:
                authors_contrib += paper_citations / (count_coauthors_in_current_subset + 1)

                # authors_contrib += paper_citations / (num_coauthors + 1)
            if current_author==author_id:
                current_author_contrib=authors_contrib
                # authors_val[author_id] += authors_contrib
            total_val += authors_contrib
                # else:
                #     print('co author found')
        value = total_val / num_papers
        if value>self.q4_quota:
            # print('over quota - subset {}'.format(permutation))
            # for author,author_val in authors_val.items():
            if value-(current_author_contrib/num_papers)<self.q4_quota:
                # print('author {} is critical'.format(current_author))
                authors_df.loc[authors_df['Author Id'] == current_author,'Num critical permutations']+=1
                return True
        return False


    def value_single_permutation_full(self,permutation, authors_df, column_name):
        # num_combinations = self.calc_num_combinations(len(authors_df) - 1, len(permutation)-1)
        value_coalition_without_current_author=0
        total_val = 0
        papers=set()
        for author_id in permutation:

            author_data = authors_df[authors_df['Author Id'] == author_id]
            authors_contrib = 0
            # sum up citations for current author, only for papers not counted yet
            for idx, paper_id in enumerate(author_data['papers'].values[0]):
                if not paper_id in papers:
                    authors_contrib += author_data['Num citations'].values[0][idx]
                    papers.add(paper_id)

            total_val += authors_contrib

            value_coalition_with_current_author = total_val / len(papers)
            author_marginal_contribution = (value_coalition_with_current_author - value_coalition_without_current_author)
            authors_df.loc[authors_df['Author Id'] == author_id, column_name] += author_marginal_contribution
            value_coalition_without_current_author=value_coalition_with_current_author


    def confidence_shapley(self,df_authors, column_name):
        self.init_permutations()

        x=0
        k=0

        min_num_samples=(2*math.pow(citation_to_papers_ratio,2)*math.log(2/self.delta,math.e))/(math.pow(self.eps,2))
        min_num_samples=min_num_samples/self.num_pcs
        # min_num_samples=10000
        print('min num samples {}'.format(min_num_samples))
        val = 0

        while k<min_num_samples:
            permutation=self.gen_permutation(df_authors)
            # permutation=self.gen_permutation(df_authors,current_author, size=0)

            # if len(permutation)<10:
            #     print('permutation size {}'.format(len(permutation)))
            self.value_single_permutation_full(permutation,df_authors, column_name=column_name)
            if k%5000==0:
                print('num samples is {}'.format(k))
            k+=1
        authors_df[column_name]=authors_df[column_name]/min_num_samples
        return

'''
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

    def add_fractional_contrib_to_df(self,df_complete,df_fractional):
        df_complete['Fractional']=0
        for idx, author_data in df_fractional.iterrows():
            author = author_data.loc['Author Id']
            frac = author_data['Fractional']
            df_complete.loc[df_complete['Author Id']==author,'Fractional']=frac

    def add_fractional_normalized_contrib_to_df(self,df_complete,df_fractional):
        df_complete['Fractional Normalized']=0
        for idx, author_data in df_fractional.iterrows():
            author = author_data.loc['Author Id']
            frac = author_data['Fractional']
            df_complete.loc[df_complete['Author Id']==author,'Fractional Normalized']=frac

'''

if __name__ == '__main__':
    journals=Journals()
    name=journals.dirsIS[6]
    file_name=journals.file_path+name+'\\'+name+'.csv'
    print(file_name)
    js=Journal_shapley_value_full_star()
    df=js.extract_data(file_name)
    authors_df = js.get_authors_df(df)
    ffv = Fractional_And_Full_value()
    ffv.get_authors_fractional_values(authors_df)
    ffv.get_authors_full_values(authors_df)

    authors_df['citation_to_papers_ratio']=authors_df['Full']/authors_df['Num papers']
    print(authors_df.sort_values(by='citation_to_papers_ratio').tail(10))
    # citation_to_papers_ratio = authors_df['citation_to_papers_ratio'].max()
    citation_to_papers_ratio=55
    print('num authors {}'.format(len(authors_df)))
    print(citation_to_papers_ratio)
    # for perm_size in [5,10,50,100,200,400]:
    #     column_name='shapley_'+str(perm_size)
    #     authors_df[column_name] = 0
    column_name='Shapley_star'
    authors_df[column_name]=0
    print(datetime.now())
    js.confidence_shapley(authors_df, column_name=column_name)
    authors_df = authors_df.sort_values(by=column_name, ascending=False)
    print(authors_df)
    print(authors_df[column_name].sum())
    # authors_df.to_csv('shap_subsets_10_2.csv')
    authors_df.to_csv(file_path+name+'\\_'+os.environ['COMPUTERNAME']+'_shap_full_star_all_authors.csv')
    print(datetime.now())


    exit(0)

    # df_for_shapley_papers=js.remove_authors_with_low_num_papers(df)

    # authors_df=js.calc_authors_shapley_num_citations(df)
    # authors_df=authors_df.sort_values(by="Shapley - Num citations",ascending=False)
    # js.get_authors_hindex_affiliation(authors_df)
    # authors_df.to_csv('C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\PUCScopus_2019_Shapley_full_star_citations.csv')
    # js.calc_total_combinations(21)
