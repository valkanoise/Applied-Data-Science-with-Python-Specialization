import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Agrego comando para tener gráficos interactivos en Spyder
# Tener en cuenta que se abre una nueva ventana donde se aprecia el gráfico
# %matplotlib

#Generamos 100 datos al azar con una distribución normal

n = 100
x1 = np.random.normal(-2.5, 1, 10000)
x2 = np.random.gamma(2, 1.5, 10000)
x3 = np.random.exponential(2, 10000)+7
x4 = np.random.uniform(14,20, 10000)

dists = [x1,x2,x3,x4]

def update(frame):
    # check if animation is at the last frame, and if so, stop the animation a
    if frame == n: 
        myanimation.event_source.stop()
    
    bins = 10
    for ax,dist in zip(fig.get_axes(),dists):
        ax.cla()
        ax.hist(dist[:frame], bins=bins)
    
fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2, sharex=True, sharey=True)
myanimation = animation.FuncAnimation(fig, update, frames=None, interval=100)