import pandas as pd

filepath_dict = {'yelp':   '~/data/yelp_labelled.txt',
                 'amazon': '~/data/amazon_cells_labelled.txt',
                 'imdb':   '~/data/imdb_labelled.txt'}

df_list = []
for source, filepath in filepath_dict.items():
    df = pd.read_csv(filepath, names=['sentence', 'label'], sep='\t')
    df['source'] = source  # Add another column filled with the source name
    df_list.append(df)

df = pd.concat(df_list)
print(df.iloc[0])
