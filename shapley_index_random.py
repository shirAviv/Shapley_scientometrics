import pandas as pd
import itertools
from scipy import misc
import math
import numpy as np
from pybliometrics.scopus import AuthorRetrieval
from itertools import chain,combinations
from datetime import date,datetime,timedelta
import random



class Shapley_index:
    q4_quota=0.4
    q2_quota=2.2
    eps=0.005
    delta=0.005
    all_permutations=dict()
    duplicate_permutations_counter=0

    def init_permutations(self):
        self.duplicate_permutations_counter = 0
        for idx in range(0,50):
            self.all_permutations[idx]=list()

    def extract_data(self, file, year=None):
        df=pd.read_csv(file)
        df=df.loc[df['Document Type'].isin(['Article','Review'])]
        if year:
            df=df.loc[df['Year']==year]
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


    def gen_permutation(self,authors_df,current_author, size=0):
        permutation=list()
        authors = list(authors_df.loc[:, 'Author Id'])
        if size>1:
            exists=True
            while exists:
                permutation=list(random.sample(authors,size-1))
                while current_author in permutation:
                    permutation = list(random.sample(authors, size-1))
                permutation.append(current_author)
                exists=self.does_permutation_exist(permutation)
            return permutation
        else:
            exists=True
            while exists:
                size=random.randint(10,30)
                permutation = list(random.sample(authors, size - 1))
                while current_author in permutation:
                    permutation = list(random.sample(authors, size-1))
                permutation.append(current_author)
                exists=self.does_permutation_exist(permutation)
            return permutation
        for author in authors:
            if author!=current_author:
                val=random.getrandbits(1)
                if val:
                    permutation.add(author)
            else:
                permutation.add(author)
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



    def check_critical(self,permutation, authors_df, current_author):
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



    def confidence_shapley_single_author(self,df_authors, current_author):
        print(datetime.now())
        x=0
        k=0
        min_num_samples=math.log(2/self.delta,math.e)/(2*math.pow(self.eps,2))
        print('min num samples {}'.format(min_num_samples))
        while k<min_num_samples:
            permutation=self.gen_permutation(df_authors,current_author, size=0)
            # permutation=self.gen_permutation(df_authors,current_author, size=0)

            # if len(permutation)<10:
            #     print('permutation size {}'.format(len(permutation)))
            k+=1
            is_critical=self.check_critical(permutation,df_authors,current_author)
            if is_critical:
                x+=1
        shapley=x/k
        confidence_interval_min=shapley-self.eps
        confidence_interval_max = shapley + self.eps
        print(datetime.now())
        return shapley,confidence_interval_min,confidence_interval_max


    def confidence_shapley(self,df_authors):
        authors = set(df_authors.loc[:, 'Author Id'])
        for author in authors:
            self.init_permutations()
            shapley,confidence_interval_min,confidence_interval_max=self.confidence_shapley_single_author(df_authors,author)
            authors_df.loc[authors_df['Author Id'] == author, 'shapley'] = shapley
            print('for author {} shapley is {} and interval is [{},{}]'.format(author,shapley,confidence_interval_min,confidence_interval_max))
            print('num dups created {}'.format(self.duplicate_permutations_counter))


    # def get_subsets(self,df):
    #     authors_ids=list(df['Author Id'])
    #     subsets = chain.from_iterable(combinations(authors_ids, r) for r in range(6, 7))
    #     return subsets

    # def calc_subset_value(self, authors_df, subset):
    #     total_val=0
    #     authors_val=dict()
    #     for author_id in subset:
    #         authors_val[author_id]=0
    #         author_data=authors_df[authors_df['Author Id'] == author_id]
    #         if author_data['Num papers'].values[0]>1:
    #             print('more than 1 paper')
    #         authors_contrib=0
    #         for idx,paper_citations in enumerate(author_data['Num citations']):
    #             # count_coauthors_in_current_subset=0
    #             coauthors_set = set()
    #             coauthors = author_data['Coauthors'].iloc[0][idx].split(';')
    #             coauthors.remove('')
    #             coauthors.remove(author_id)
    #             coauthors_set.update(set(coauthors))
    #             num_coauthors = len(coauthors_set)
    #             count_coauthors_in_current_subset=len(coauthors_set.intersection(subset))
    #
    #             # if  not author_id in coauthors_set:
    #             authors_contrib+=paper_citations[0]/(count_coauthors_in_current_subset+1)
    #             authors_val[author_id]+=authors_contrib
    #             total_val+=authors_contrib
    #             # else:
    #             #     print('co author found')
    #     value=total_val/num_papers
    #     # print(value)
    #     if value>self.q4_quota:
    #         # print('over quota - subset {}'.format(subset))
    #         for author,author_val in authors_val.items():
    #             if value-(author_val/num_papers)<self.q4_quota:
    #                 print('author {} is critical'.format(author))
    #                 authors_df.loc[authors_df['Author Id'] == author,'Num critical permutations']+=1

    # def iterate_subsets(self,authors_df, subsets):
    #     counter=0
    #     for subset in subsets:
    #         self.calc_subset_value(authors_df, subset)
    #         counter+=1
    #     print("count subsets is {}".format(counter))

if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    file_path='C:\\Users\\Shir\\OneDrive - Bar Ilan University\\research\\Journals_data\\IS\\ASLIB_Journal_of_info_manage\\ASLIB_Journal_of_info_manage_2018-2021_scopus.csv'
    si=Shapley_index()
    df=si.extract_data(file_path, year=2021)
    num_papers=len(df)
    print('num papers is {}'.format(num_papers))
    # df_for_banzhaf=bi.remove_low_citation_papers(df)
    df_for_banzhaf=df
    authors_df=si.get_authors_df(df_for_banzhaf)
    authors_df['Num critical permutations']=0
    authors_df['shapley'] = 0

    si.confidence_shapley(authors_df)
    authors_df = authors_df.sort_values(by="Num critical permutations", ascending=False)
    print(authors_df)
    # authors_df.to_csv('shap_subsets_10_2.csv')
    authors_df.to_csv('shap_relative_10_30_005_cites_over_3_q4.csv')
    end_time = datetime.now()
    print(start_time)
    print(end_time)

    exit(0)

    # subsets=si.get_subsets(authors_df)
    # si.iterate_subsets(authors_df,subsets)
    # authors_df = authors_df.sort_values(by="Num critical permutations", ascending=False)
    # print(authors_df)
    # authors_df.to_csv('authors_power_index_subsets_6.csv')

    # print(authors_df)
    # authors_df=authors_df.sort_values(by="Num citations",ascending=False)
    # end_time = datetime.now()
    # print(start_time)
    # print(end_time)



