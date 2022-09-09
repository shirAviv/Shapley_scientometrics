import os
import tqdm
import pandas as pd

path=r'C:\Users\Shir\OneDrive - Bar Ilan University\research\Journals_data\IS\Informing Science'


class MergeData:
    def merge(self):
        df = pd.read_csv(path+r'/shapley_all_authors_base.csv')
        df[column_name]=0
        list_of_files = list(os.listdir(path))
        for file in os.listdir(path=path):
            if not file.endswith('_shap_full_star_all_authors.csv'):
                continue
            obj_path = os.path.join(path, file)
            df_shap = pd.read_csv(obj_path)
            for idx, author_data in df.iterrows():
                author_id=author_data['Author Id']
                shap_value=df_shap.loc[df_shap['Author Id']==author_id, column_name]
                df.loc[df['Author Id'] == author_id, column_name] += shap_value
        print(df)



if __name__ == '__main__':
    column_name='Shapley_star'
    merge=MergeData()
    merge.merge()
