# PyGameOfLive
 Game of Live on Python 3.10

 ## Required Libraries
pygame==2.5.0

numba==0.57.1

numpy==1.24.4

 ## Start settings
The \_\_name__ == "\_\_main__" block contains all the basic parameters for setting up the game.

"window_size" is a tuple containing the length and width of the window in pixels.

"pixel_size" is the size of one cell in pixels.

"fps" - number of frames per second (enter -1 for maximum frames)

"random_fill" - responsible for random filling of cells. If this parameter is turned off, the cells will completely fill the sufficient volume.

"barrier_percent" - the percentage of the map inaccessible for the first appearance of cells
## Additional settings

You can also optionally specify some settings when creating the "automaton" object. Layout to create them V/B/S

__V__ - vision. How cells will see. 

V = "8" means that cells will see all their 8 neighbor cells. 

V = "4d" means that the cell will see diagonally. 

V = "4c" means that the cell will see the crosshairs from its neighbors.

B - birth. In this parameter, you must specify a list with the values ​​of "live neighbors" at which a new cell may appear

S - survival. In this parameter, you must specify a list with the values ​​of "living neighbors" at which the cell will continue to live