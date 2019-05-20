# -------------------------------------------------------------- #
# -------------------------------------------------------------- #
# ----------- Declaring optimization function for limb darkening correction ------- #
# -------------------------------------------------------------- #
# -------------------------------------------------------------- #

import numpy as np
def Correction(theta):
    
    import numpy as np
    c0, c1, c2, c3 = theta
    global Mu_Brightest, Map_Brightest, Mu, Flat_Mask, Cylindrical_to_Spherical_Conversion_list
    correction = np.array(c0 - c1*(1 - Mu_Brightest) - c2*(1 - Mu_Brightest**2) - c3*(1 - Mu_Brightest**3))
    
    Model = Map_Brightest * correction
    Light_Curve_Images = np.zeros((5,360,720))
    for i in range(5):
        
        Light_Curve_Images[i] = model * Flat_Mask[i]/(c0 - c1*(1 - Mu[i]) - c2*(1 - Mu[i]**2) - c3*(1 - Mu[i]**3))
        Light_Curve_Images[i] *= Cylindrical_to_Spherical_Conversion_list[i]
    
    Light_Curve_Average = np.sum(Light_Curve_Images)/np.count_nonzero(Light_Curve_Images)
    Map_Averages = np.sum(Map_Master)/np.count_nonzero(Map_Master)
    Covariance = np.sum((Light_Curve_Images - Light_Curve_Average) * (Map_Master - Map_Averages))
    return Covariance