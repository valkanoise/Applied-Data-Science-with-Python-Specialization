import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches


# importamos una función que permite separar un dataset en dos datasets distintos a modo de crear una dataset 
# de entrenamiento y otro de evaluación a partir de un solo dataset.
from sklearn.model_selection import train_test_split

# Importamos el dataset que son una serie de datos tabulados:
fruits = pd.read_table('readonly/fruit_data_with_colors.txt')


# Antes que nada separamos los labels de los atributos de cada fruta
# 1- Definimos una matriz con los atributos de las frutas
X = fruits[['mass', 'width', 'height']]
# 2- Definimos otra matriz con el código de las frutas
y = fruits['fruit_label']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.25)


#%% Function done by FEFe
def plot_fruit_knn(X, y, n_neighbors=5, weights='uniform'):
    X_mat = X[['height', 'width']]
    y_mat = y
    
    # We create the classifier and define K and type of weight:
    clf = KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X_mat, y_mat)
    
    # Create color maps
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF','#AFAFAF'])
    cmap_bold  = ListedColormap(['#FF0000', '#00FF00', '#0000FF','#AFAFAF'])

    mesh_step_size = .01  # step size in the mesh
    plot_symbol_size = 50
    
    x_min, x_max = X_mat['height'].min() - 1, X_mat['height'].max() + 1
    y_min, y_max = X_mat['width'].min() - 1, X_mat['width'].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, mesh_step_size),
                         np.arange(y_min, y_max, mesh_step_size))
    
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
    
    # Plot training points
    plt.scatter(X_mat['height'], X_mat['width'], s=plot_symbol_size, c=y, cmap=cmap_bold, edgecolor = 'black')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    
    patch0 = mpatches.Patch(color='#FF0000', label='apple')
    patch1 = mpatches.Patch(color='#00FF00', label='mandarin')
    patch2 = mpatches.Patch(color='#0000FF', label='orange')
    patch3 = mpatches.Patch(color='#AFAFAF', label='lemon')
    plt.legend(handles=[patch0, patch1, patch2, patch3])
    
    plt.title('K-NN decision boundaries with K= {}'.format(n_neighbors))
    plt.xlabel('height (cm)')
    plt.ylabel('width (cm)')
    
    plt.show()
    
#%% Prueba generando distintos gráficos para cada K= 1,2,3,4,5 y 15(len(y_train))

for i in list(range(1,6))+[y_train.value_counts().iloc[0]]:
    plot_fruit_knn(X_train, y_train, n_neighbors=i, weights='uniform')
    
    
#%% Anothe working function from the web


def plot_fruit_knn2(X, y, n_neighbors, weights):
    
    
    X_mat = X[['height', 'width']].values
    y_mat = y.values
# Create color maps
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF','#AFAFAF'])
    cmap_bold  = ListedColormap(['#FF0000', '#00FF00', '#0000FF','#AFAFAF'])
    clf = KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X_mat, y_mat)
# Plot the decision boundary by assigning a color in the color map
    # to each mesh point.

    mesh_step_size = .01  # step size in the mesh
    plot_symbol_size = 50

    x_min, x_max = X_mat[:, 0].min() - 1, X_mat[:, 0].max() + 1
    y_min, y_max = X_mat[:, 1].min() - 1, X_mat[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, mesh_step_size),
                         np.arange(y_min, y_max, mesh_step_size))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
# Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
# Plot training points
    plt.scatter(X_mat[:, 0], X_mat[:, 1], s=plot_symbol_size, c=y, cmap=cmap_bold, edgecolor = 'black')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    patch0 = mpatches.Patch(color='#FF0000', label='apple')
    patch1 = mpatches.Patch(color='#00FF00', label='mandarin')
    patch2 = mpatches.Patch(color='#0000FF', label='orange')
    patch3 = mpatches.Patch(color='#AFAFAF', label='lemon')
    plt.legend(handles=[patch0, patch1, patch2, patch3])
    
    plt.xlabel('height (cm)')
    plt.ylabel('width (cm)')
    #plt.title("4-Class classification (k = %i, weights = '%s')" % (n_neighbors, weights))    
    plt.show()


#%%

plot_fruit_knn2(X_train, y_train, n_neighbors=5, weights='uniform')
