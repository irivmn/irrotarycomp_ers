def ambientpressure(Altitude) : #(Altitude : P_amb):   #" *** Pressure at altitude calculations *** "  
    g_o = 9.80665 #[m/s^2] #"Universal constants"  
    M = 28.9644 #[kg/kmol] #"Universal constants"  
    R = 8314.32 #[N-m/kmol-K] #"Universal constants"  
    #"Atmospheric layer constants for less than 11,000 meters. Reference: https://en.wikipedia.org/wiki/Barometric_formula"  
    P_b = 101325 #[Pa]  #"Static pressure"  
    T_b = 288.15 #[K]  #"Standard temperature"  
    h_b = 0 #[m]  #"Height at bottom of layer b (e.g.: h_1 = 11,000 m)"  
    L_b = -0.0065 #[K/m]  #"Standard temperature lapse rate in ISA"  
    H = Altitude  
    P_amb = (P_b * pow((T_b / (T_b + L_b * (H - h_b))),((g_o * M)/(R*L_b))))
    return P_amb 