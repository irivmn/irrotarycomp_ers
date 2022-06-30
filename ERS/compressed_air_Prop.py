from CoolProp.HumidAirProp import HAPropsSI
from CoolProp.CoolProp import PropsSI


def condensate(m_dot_dry_air, m_dot_pa, m_dot_pw, omega_p, P_c, T_c, cond,P_w_amb,P_100): #: m_dot_ca, m_dot_cw, omega_c,T_c_sat):
    T_c_sat= HAPropsSI('D','P_w',P_w_amb*(P_c/P_100),'P',P_c,'R',1)                        
    if T_c < T_c_sat :
        omega_c = HAPropsSI('W','T',T_c,'P',P_c,'R',1.00); #humrat(AirH2O,T=T_c,R=1.00,P=P_c)   
        m_dot_cw = (m_dot_dry_air * (omega_p - omega_c)) + m_dot_pw   
        m_dot_ca = m_dot_pa - (m_dot_dry_air * (omega_p - omega_c))  
    else:  
        if (cond!=205 and cond!=215 and cond!=225) : 
            omega_c = omega_p 
            #print("omega_125 : ",omega)   
            m_dot_ca = m_dot_pa  
            #print(m_dot_a[cond])  
            m_dot_cw = 0  + m_dot_pw 
            #print(m_dot_w[cond])
        else:
            if T_c == T_c_sat :   
                omega_c = omega_p    
                m_dot_ca = m_dot_pa    
                m_dot_cw = 0  + m_dot_pw   
            else  :  
                omega_pw = omega_p + (m_dot_pw / m_dot_dry_air)                                                          #"Omega_w ' wet ' assumes all water carryover is vaporized"    
                T_c_sat = HAPropsSI('D','P_w',P_w_amb*(P_c/P_100),'P',P_c,'R',1);#print("T_c_sat_w : ",T_sat[cond])
                if T_c < T_c_sat :    
                    omega_c = HAPropsSI('W','T',T_c,'P',P_c,'R',1.00);                                               #humrat(AirH2O,T=T_c,R=1.00,P=P_c)     
                    m_dot_cw = ((m_dot_dry_air * omega_p) + m_dot_pw)  - (m_dot_dry_air * omega_c)              #"Conservation of mass"      
                    m_dot_ca = (m_dot_pa + m_dot_pw) - m_dot_cw    
                else :    
                    omega_c = omega_pw     
                    m_dot_ca = (m_dot_pa + m_dot_pw)     
                    m_dot_cw= 0 #[kg/s]
    '''print("m_dot_a_dict : ",m_dot_a)
    print("m_dot_w_dict : ",m_dot_w)
    print("omega_dict : ",omega_)
    print("T_sat_dict",T_sat)'''
    return (m_dot_ca, m_dot_cw, omega_c,T_c_sat)

def compressedairprop (T, omega, P) : #: h_a,h_w,Rho_a,C_p_a,Mu_a,k_a,Pr_a) 
    h_a = HAPropsSI('H','T',T,'P',P,'W',omega) #enthalpy(AirH2O,T=T,w=omega,P=P)   
    h_w = PropsSI('H','T',T,'P',P,'IF97::Water'); #print(h_125) #enthalpy(Water,T=T,P=P)                      
    Rho_a = 1/HAPropsSI('Vha','T',T,'P',P,'W',omega)  #density(AirH2O,T=T,w=omega,P=P)             
    C_p_a = HAPropsSI('Cha','T',T,'P',P,'W',omega); #print(C_p_a)  #cp(AirH2O,T=T,w=omega,P=P)                 
    Mu_a = HAPropsSI('mu','T',T,'P',P,'W',omega); #print(Mu_a)   #viscosity(AirH2O,T=T,w=omega,P=P)            
    k_a = HAPropsSI('K','T',T,'P',P,'W',omega)    #conductivity(AirH2O,T=T,w=omega,P=P)          
    Pr_a = (Mu_a*C_p_a)/k_a; #print(Pr_a)   #prandtl(AirH2O,T=T,w=omega,P=P)   
    return (h_a,h_w,Rho_a,C_p_a,Mu_a,k_a,Pr_a)
