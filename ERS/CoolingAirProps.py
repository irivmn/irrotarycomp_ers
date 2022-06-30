from CoolProp.HumidAirProp import HAPropsSI

def coolingairprop (T, omega, P,n) : #h_ca,v_ca,Rho_ca,C_p_ca,Mu_ca,k_ca,Pr_ca)   
    h_a= HAPropsSI('H','T',T,'P',P,'W',omega)    #enthalpy(AirH2O,T=T,w=omega,P=P)  
    v_a= HAPropsSI('Vha','T',T,'P',P,'W',omega)     #volume(AirH2O,T=T,w=omega,P=P)  
    Rho_a= 1/HAPropsSI('Vha','T',T,'P',P,'W',omega) #density(AirH2O,T=T,w=omega,P=P)            
    C_p_a= HAPropsSI('Cha','T',T,'P',P,'W',omega)   #cp(AirH2O,T=T,w=omega,P=P)                 
    Mu_a= HAPropsSI('M','T',T,'P',P,'W',omega)   #viscosity(AirH2O,T=T,w=omega,P=P)  
    k_a= HAPropsSI('K','T',T,'P',P,'W',omega)    #conductivity(AirH2O,T=T,w=omega,P=P)   
    Pr_a = (Mu_a*C_p_a)/k_a         #prandtl(AirH2O,T=T,w=omega,P=P) 

    return (h_a,Rho_a,C_p_a,Mu_a,k_a,Pr_a)

def avgprop (Rho_IN, C_p_IN, Mu_IN,k_IN,Pr_IN,Rho_OUT, C_p_OUT, Mu_OUT,k_OUT,Pr_OUT,avg ) : # Rho_avg,C_p_avg,Mu_avg,k_avg,Pr_avg)    
    Rho_avg  =  (Rho_IN+Rho_OUT)/2  
    C_p_avg =  (C_p_IN+C_p_OUT)/2  
    Mu_avg  =  (Mu_IN+Mu_OUT)/2   
    k_avg  =  (k_IN+k_OUT)/2   
    Pr_avg  =  (Pr_IN+Pr_OUT)/2 
    return (Rho_avg,C_p_avg,Mu_avg,k_avg,Pr_avg)