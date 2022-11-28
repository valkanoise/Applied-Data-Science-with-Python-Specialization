import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, RadioButtons

# Command to have interactive graphs in Jupyter notebook
#%matplotlib notebook



### 0- Lets generate some data

n = 100

# generate 4 random variables from the random, gamma, exponential, and uniform distributions
d1 = np.random.normal(0, 1, n)
d2 = np.random.gamma(2, 2, n)
d3 = np.random.exponential(2, n)
d4 = np.random.uniform(size=n)


# Generate a list with all the distributions
dists = [d1,d2,d3,d4]
nombres = ['Normal', 'Gamma', 'Exponential', 'Uniform']


### 1- Creates the Figure and its 4 subplots/axes

fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
# Sets the spacing between subplots
plt.subplots_adjust(bottom=0.25, right=0.9, top=0.85, wspace=0.4, hspace=0.4)
# Adds common names to the x and y axis of the whole figure
fig.text(0.5, 0.17, 'Frequency', ha='center')
fig.text(0.05, 0.5, 'Values', va='center', rotation='vertical')


### 2- Lets create a function that will update the plots

def update(frame):
    # check if animation is at the last frame, and if so, stop the animation a
    if frame == n: 
        myanimation.event_source.stop()
    
       
    # For every distribution/pot/axes   
    for ax,dist,nombre in zip(fig.get_axes(),dists, nombres):
        
        # Defines the number of bines to be graphed
        bines=20
        
        # Clear axes of every subplot
        ax.cla()
        
        ### 
        # In order to avoid resizing of the axes during the animation we can fix x and y axis
        # 1st calculate the bins and its frequencies for each distribution to later set x and y limits
        frequency, bins = np.histogram(dist, bins=bines)   
        
        # 2nd use bins and frequency to set x and y limits
        ax.set_xlim(bins.min(),bins.max())
        ax.set_ylim(0, max(frequency)+1)
        ###
        
        # Plots each distribution according to the number of frame
        ax.hist(dist[:frame], bins=bines, color='r', alpha=0.5, edgecolor='yellow')
        # Sets the title of each subplot/axes
        ax.set_title(f'{nombre} distribution', loc='center', size=9)
        
        # Defines the same number of 5 xticks for every axes according to the values given by the bins
        ax.set_xticks(np.linspace(round(bins.min()), round(bins.max()), 5))        
    
        # Adds to the Figure a title
        fig.suptitle(f'Frame number={frame}', fontsize=15)
    
### 3- Lets create the animation
myanimation = animation.FuncAnimation(fig, update, frames=None, interval=10)

#%% Save the animation as video
f = r"c://Users/FEFe/Desktop/animation1.mov" 
writervideo = animation.FFMpegWriter(fps=30) 
myanimation.save(f, writer=writervideo)