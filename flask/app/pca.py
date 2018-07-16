import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

'''
Get Principal Components from ingredients csv
https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60

The csv contains ingredients related to each other by the number of times
they have appeared in the same recipe

This function uses PCA to reduce the n-d matrix of ingredients
to a 2-d matrix of x and y values which can be graphed or separated
into clusters

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
    return finalDf.loc[:,['x', 'y', 'Ingredient']].values.tolist()


