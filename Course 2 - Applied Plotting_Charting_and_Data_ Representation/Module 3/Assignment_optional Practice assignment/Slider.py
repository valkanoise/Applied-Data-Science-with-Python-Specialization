import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, RadioButtons

# Command to have interactive graphs in Jupyter notebook
%matplotlib notebook



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



#### Widget section ####

### 1- Generate the 4 plots, one for each distribution

fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
# Sets the spacing between subplots
plt.subplots_adjust(bottom=0.25, right=0.9, top=0.85, wspace=0.4, hspace=0.4)


# Defines the number of bines to be graphed
bines_init=10

for ax,dist,nombre in zip(fig.get_axes(),dists, nombres):
        # Clear axes of every subplot
        #ax.cla()

        ### 
        # In order to avoid resizing of the axes during the animation we can fix x and y axis
        # 1st calculate the bins and its frequencies for each distribution to later set x and y limits
        frequency, bins = np.histogram(dist, bins=bines_init)   

        # 2nd use bins and frequency to set x and y limits
        ax.set_xlim(bins.min(),bins.max())
        ax.set_ylim(0, max(frequency))
        ###

        # Plots each distribution according to the number of frame
        ax.hist(dist, bins=bines_init, color='r', alpha=0.5)
        # Sets the title of each subplot/axes
        ax.set_title(f'{nombre} distribution', loc='center', size=9)

        # Defines the same number of 5 xticks for every axes according to the values given by the bins
        ax.set_xticks(np.linspace(round(bins.min()), round(bins.max()), 5))

# Adds to the Figure a title
fig.suptitle(f'Different types of distributions', fontsize=15)
# Adds common names to the x and y axis of the whole figure
fig.text(0.5, 0.17, 'Frequency', ha='center')
fig.text(0.05, 0.5, 'Values', va='center', rotation='vertical')
    


### 2- Add sliding bar in the bottom

# Generate two new axes and define their positions
axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

# Generate the slider in the previously generated axes
# We also define the values from 1-50 with "valstep" argument
sfreq = Slider(axfreq, 'Bins', valmin=1, valmax=50, valinit=bines_init, valstep=[x for x in range(1,51)])



### 3- Generate the function that will update the figure upon changes in the slider
def update(val):
    freq = sfreq.val
    for ax,dist in zip(fig.get_axes()[0:4], dists):
        ax.cla()
        ax.hist(dist, bins=freq, color='r', alpha=0.5)
        
# When the slider values are changed the update function is called      
sfreq.on_changed(update)


### 4- Create a button that resets everything to the original bin=10

# Creates an axes and put a class button there
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

# Function that defines what happens when you click the button 
def reset(event):
    sfreq.reset()
button.on_clicked(reset)