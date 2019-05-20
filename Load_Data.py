# -------------------------------------------------------------- #    
# --------------------- Loading raw data ----------------------- #
# -------------------------------------------------------------- #    


Map_Master = np.array([np.reshape(np.loadtxt('Cylindrical_Map1.dat'), (360,720)), np.reshape(np.loadtxt('Cylindrical_Map2.dat'),(360,720)), np.reshape(np.loadtxt('Cylindrical_Map3.dat'),(360,720)), np.reshape(np.loadtxt('Cylindrical_Map4.dat'),(360,720)), np.reshape(np.loadtxt('Cylindrical_Map5.dat'),(360,720))])
Mu = np.array([np.reshape(np.loadtxt('Cylindrical_Mu1.dat'),(360,720)), np.reshape(np.loadtxt('Cylindrical_Mu2.dat'),(360,720)), np.reshape(np.loadtxt('Cylindrical_Mu3.dat'),(360,720)), np.reshape(np.loadtxt('Cylindrical_Mu4.dat'),(360,720)), np.reshape(np.loadtxt('Cylindrical_Mu5.dat'),(360,720))])

# -------------------------------------------------------------- #    
# ------- Declaring index matrix and assigning values  --------- #
# -------------------------------------------------------------- #    

Index_Master = np.zeros((720,360,720,2))

for i in range(360):
    Index_Master[:,i,:,0] = i
for j in range(720):
    Index_Master[:,:,j,1] = j
    
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    
# ----------- Trimming values above and below 75 N ------------- #
# ------------------ and 75 S, respectively  ------------------- #
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    

for i in range(0,30):
    Map_Master[:,i] = 0
for i in range(330,360):
    Map_Master[:,i] = 0

# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    
# ------ Declaring array consisting of 720 360x720 arrays ------ #    
# ----- each sucessively filled with values 0 through 719 ------ #    
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    

K_Matrix = np.zeros((720,360,720))

for k in range(720):
   K_Matrix[k,:] = k
    
# -------------------------------------------------------------- #        
# -------------------------------------------------------------- #    
# --------- Trimming telescope artifacts from images ----------- #
# ------------ by removing points below threshold -------------- #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #    

for index, value in np.ndenumerate(Map_Master):
    
    if value < 0.01:
        
        Map_Master[index] = 0.

# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    
# --------- Declaring array to convert from cylindrical -------- #
# ---------- to spherical weighting with the formula: ---------- #
# ----- Spherical_weighting = sin((phi))^2 * |cos((theta))| ---- #    
# --- where phi is the polar angle and theta is the azimuthal -- #    
# ------- angle from the center of an image (in radians) ------- #    
# --------  declared for all possible coordinate values--------- #    
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    

Cylindrical_to_Spherical_Conversion = np.array(map(lambda (i,j,k): np.sin((i/float(360)*np.pi))**2 * np.abs(np.cos(np.pi/(360)*(j - k))), zip(index_master[:,:,:,0],index_master[:,:,:,1],k_matrix)))

# -------------------------------------------------------------- #    
# ---------- Normalizing conversion over all points ------------ #    
# -------------------------------------------------------------- #    

Cylindrical_to_Spherical_Conversion /= np.sum(Cylindrical_to_Spherical_Conversion)/np.count_nonzero(Cylindrical_to_Spherical_Conversion)

# -------------------------------------------------------------- #    
# ------------ Declaring list of values of central ------------- # 
# ------------ azimuthal coordinate for each image ------------- #   
# -------------------------------------------------------------- #    

Centers_List = [np.argmax(mu[0])%720, np.argmax(mu[1])%720, np.argmax(mu[2])%720, np.argmax(mu[3])%720, np.argmax(mu[4])%720]

# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #
# ***README*** 
# ----- Creating list of correct conversions for each image ---- #    
# --------- from array of all possible conversions by ---------- #    
# --------------- assigning index of image's center ------------ #    
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    

Cylindrical_to_Spherical_Conversion_list = [Cylindrical_to_Spherical_Conversion[centers_list[0]], Cylindrical_to_Spherical_Conversion[centers_list[1]], Cylindrical_to_Spherical_Conversion[centers_list[2]], Cylindrical_to_Spherical_Conversion[centers_list[3]], Cylindrical_to_Spherical_Conversion[centers_list[4]]]

# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    
# ----------- Declaring spherical map and filling -------------- #    
# ------------------ with corrected values --------------------- #    
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    

Map_Master_Spherical = np.zeros((5,360,720))

for i in range(5):
    Map_Master_Spherical[i] = Map_Master[i] * Cylindrical_to_Spherical_Conversion[int(Centers_List[i])]

# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #
# ------------ Creating image of a mu map centered  ------------ #    
# ---------------- about 0 azimuthal coordinate ---------------- #    
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    

Mu_Centered = np.roll(Mu[3], -int(Centers_List[3]), axis=1)
 
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    
# ------------------- Creating image of mu --------------------- #    
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    

Mu_Flat = np.zeros((5,360,720))

for index, value in np.ndenumerate(Map_Master):
    
    if value != 0.:
        
        Mu_Flat[index] = 1.
        
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    
# ---------- Creating a flat mu array centered about ----------- #    
# ------------------- the 0 azimuthal point -------------------- #    
# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    

Mu_Flat_Centered = Mu_Flat[3]
Mu_Flat_Centered = np.roll(Mu_Flat_Centered, -int(Centers_List[3]), axis=1)
 

# -------------------------------------------------------------- #    
# -------------------------------------------------------------- #    
# --------------- Creating arrays and assigning ---------------- #
# ------------ the brightest map and corresponding ------------- #
# ---------------------mu points to them ----------------------- #    
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #    

Mu_Brightest = np.zeros((360,720))
Brightest_Indices = np.zeros((360,720))
Map_Brightest = np.zeros((360,720))
Map_Brightest = np.max(Map_Master, axis=0)

for index, value in np.ndenumerate(Brightest_Indices):
    
    Mu_Brightest[index] = mu[int(Brightest_Indices[index]), int(index[0]), int(index[1])]