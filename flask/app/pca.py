import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

'''
Get Principal Components from ingredients csv
https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
'''
def get_2d_ingredients():
    recipes_csv = pd.read_csv(os.path.join(os.getcwd(), 'app/recipes.csv'))
    x = recipes_csv.drop('Ingredient', axis=1)
    x = x.loc[:, x.columns.values].values
    x = StandardScaler().fit_transform(x)
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents
                               , columns = ['x', 'y'])
    finalDf = pd.concat([principalDf, recipes_csv[['Ingredient']]], axis = 1)
    print finalDf
    return []


