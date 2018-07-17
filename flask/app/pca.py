import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
import json
import csv

def get_2d_ingredients():
    '''
    Get Principal Components from ingredients csv
    https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60

    :var keys in the format { ingredient(string):index(number) }
        for faster lookup times
    :var keysArr an array of keys in the correct order
    :var currentIndex the current index
    :var matrix the matrix of recipes (rows) and ingredients (columns)
    :return: finalDfArr the matrix of x and y values for each ingredient
    '''
    keys = {}
    keysArr = []
    matrix = []

    with open(os.path.join(os.getcwd(), 'app/4week_recipes.json')) as jsonFile:
        data = json.load(jsonFile)

    # only use the first 1000 recipes for now
    data = data[:1000]

    # -------------------------------------------------
    # create an array of ingredients (the keys)
    # clean and trim the ingredient string before adding it
    for recipe in data:
        for ingredient in recipe['ingredients']:
            clean = clean_ingredient(ingredient)
            if (clean not in keys):
                keysArr.append(clean)
                keys[clean] = len(keysArr) - 1
    # -------------------------------------------------


    # -------------------------------------------------
    # Create a row in the matrix for each recipe
    # if the ingredient exists in the recipe,
    # make it a 1. If not, it will be 0
    for recipe in data:
        matrixArr = [0] * len(keysArr)
        for ingredient in recipe['ingredients']:
            matrixArr[keys[clean_ingredient(ingredient)]] = 1
        matrix.append(matrixArr)
    # -------------------------------------------------


    # -------------------------------------------------
    # Create a dataframe and find the co-occurrence matrix
    # of the ingredients by multiplying by the transpose
    df = pd.DataFrame(matrix)
    cooccurrence = df.T.dot(df)
    cooccurrence = cooccurrence.loc[:, cooccurrence.columns.values].values
    # -------------------------------------------------


    # -------------------------------------------------
    # run PCA on the co-occurrence matrix to get the
    # x and y values
    new_matrix = StandardScaler().fit_transform(cooccurrence)
    pca = PCA(n_components = 2)
    keys_dataframe = pd.DataFrame(keysArr)
    principalComponents = pca.fit_transform(new_matrix)
    principalDf = pd.DataFrame(data = principalComponents
                               , columns = ['x', 'y'])
    finalDf = pd.concat([principalDf['x'],principalDf['y'], keys_dataframe[0]], axis = 1)
    finalDfArr = finalDf.loc[:,['x', 'y', 0]].values.tolist()
    # -------------------------------------------------

    # write the data to a csv file for now
    with open('app/results.csv', 'w') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=',')
        csvWriter.writerows(finalDfArr)
    return finalDfArr



def clean_ingredient(ingredient):
    '''
    Remove non-ascii characters and whitespace

    :param ingredient: the ingredient
    :return: ingredient cleaned up
    '''
    return ingredient.encode('ascii', errors='ignore').strip()







