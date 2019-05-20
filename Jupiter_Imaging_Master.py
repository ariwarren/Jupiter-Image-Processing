import inspect
file = inspect.getfile(inspect.currentframe())

import numpy as np
import scipy.optimize as op

execfile('Load_Data.py')

c0_init, c1_init, c2_init, c3_init = 0.31071799, -2.43823808,  2.44058044, -0.9041359

# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# -------------- Run Optimization.py script to ----------------- #
# -------------- declare 'Correction' function ----------------- #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #

execfile('Optimization.py')

# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# ------- Assign initial guesses to function arguments --------- #
# ------------  and execute function recursively --------------- #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #

Covariance = lambda *args: -Correction(*args)
result = op.minimize(Covariance, [c0_init, c1_init, c2_init, c3_init], options = {'maxiter' : 100000}, args=(), method='COBYLA')
print(result)

# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# ---- Assign result of optimization function to placeholder --- #
# ------- variables and use these to construct a model --------- #
# ----------- using the brightest points from images ----------- #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #

c0, c1, c2, c3 = result["x"][0], result["x"][1], result["x"][2], result["x"][3]

Final_Model = (c0 - c1*(1 - Mu_Brightest) - c2*(1 - Mu_Brightest**2) - c3*(1 - Mu_Brightest**3)) * Map_Brightest
Correction_Master = (c0 - c1*(1 - Mu) - c2*(1 - Mu**2) - c3*(1 - Mu**3))

# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# ----------- Declaring light curve and "rolling" -------------- # 
# ------------------ cutout across final map ------------------- #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #

Light_Curve = np.zeros((720))

Mu_Rolled = np.zeros((720,360,720))
Mu_Flat_Rolled = np.zeros((720,360,720))
for k in range(720):
    
    Mu_Flat_Rolled[k] = np.roll(Mu_Flat_Centered, k, axis=1)
    Mu_Rolled[k] = np.roll(Mu_Centered, k, axis=1)

# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# ---------- Calculating effective brightness of light --------- #
# ------------ curve at each coordinate of longitutde ---------- #
# -------------- by dividing by correction factor -------------- # 
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #


Light_Curve = np.sum(np.sum(Final_Model * Mu_Flat_Rolled/(c0 - c1*(1 - Mu_Rolled) - c2*(1 - Mu_Rolled**2) - c3*(1 - Mu_Rolled**3)), axis=2), axis=1)

# -------------------------------------------------------------- #
# ----- Constructing images at each point from final model ----- #
# -------------------------------------------------------------- #

Constructed_Images = Final_Model * Mu_Flat_Rolled/(c0 - c1*(1 - Mu_Rolled) - c2*(1 - Mu_Rolled**2) - c3*(1 - Mu_Rolled**3))

# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# ---------- Summing up map points and normalizing ------------- #
# --------------- with respect to light curve ------------------ #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #

Map_Totals = np.sum(np.sum(Map_Master_Spherical, axis=2), axis=1)
Map_Totals *= (np.sum(Light_Curve)/720.)/(np.sum(Map_Totals)/5.)

# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# --------- Constructing graph of image brightnesses ----------- #
# --------- plotted on top of light curve brightness ----------- #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #

import matplotlib.pyplot as plt
plt.ion()
plt.figure()
plt.title(file)
plt.xlabel(result["x"])
plt.plot(Light_Curve)
Light_Curve_Points = [Light_Curve[centers_list]]
plt.scatter(Centers_List, Light_Curve_Points)
plt.scatter(Centers_List, Map_Totals)

# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# ------------ Constructing image of final model --------------- #
# ------- in colors representing infrared temperature ---------- #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #

import matplotlib.pyplot as plt
plt.ion()
levels = []
for i in range(200):
    levels.append(-0.03 + 0.002*i)

x = list(range(720))
y = list(range(360))

levels = []
for i in range(200):
    levels.append(-0.03 + 0.0010*i)
    
plt.figure()
plt.title(file)
cp = plt.contourf(x, y, Final_Model, cmap='hot', levels=levels)
plt.colorbar(cp)