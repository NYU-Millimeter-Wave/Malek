from __future__ import division

import Tkinter as tk
import numpy as np
import turtle

#wn= turtle.Screen()
#lam= turtle.Turtle()
app = tk.Tk()
cv = turtle.ScrolledCanvas(app)
cv.pack()
screen=turtle.TurtleScreen(cv)
screen.screensize(1500,1500)
lam= turtle.RawTurtle(screen)

tabdist = [-184, 2, 0, -6, -6, -6, -11, -204, -2, -487, 2, 0, -6, 4, -11, -409, 11, 29]
tabangle = [-1, 13, 18, 9, 8, 8, 3, 5, 16, 0, -13, -18, -8, -7, -6, -1, 0, 0]

#tabdist = [10,10,10,10,10,10,10,10]
#tabangle = [0,0,0,30,-30,0,0,0]


#dessin(tabdist,tabangle)

def dessin(tabdist,tabangle):
        ltab=len(tabdist)
        for i in range (0,ltab):
		#if tabdist[i] >=0:
                lam.forward(tabdist[i])
		#else: 
			#tempp=-1*tabdist[i]
			#lam.backward(tempp)
                if tabangle[i] >=0:
                	temp =-(180-tabangle[i])
           		lam.right(temp)
		else:	
			tempp = (180-tabangle[i])
                        lam.right(tempp)
        #turtle.getscreen()._root.mainloop()
	turtle.mainloop()
#tabdist=[32,78,125,94,17,25,0,34]
#tabangle=[41,25,90,-13,65,-8,-42,18]
dessin(tabdist,tabangle)
