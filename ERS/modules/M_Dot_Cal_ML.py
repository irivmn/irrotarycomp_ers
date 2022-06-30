from CoolProp.HumidAirProp import HAPropsSI
from compressed_air_Prop import *
from CoolingAirProps import *

def M_DOT_H(T_,P_,omega_,Q,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a,P_w_amb):
    # Finds Q for given M_Dot_H & T_H_out
    m_dot_w[100] = 0 #[kg/s]
    m_dot_dry_air = m_dot_a[100] / (1+omega_[100])
    m_dot_wv = m_dot_a[100] - m_dot_dry_air
    (m_dot_a[125], m_dot_w[125], omega_[125],T_sat[125])=condensate (m_dot_dry_air, m_dot_a[100], m_dot_w[100], omega_[100], P_[125], T_[125],125,P_w_amb,P_[100])  # Inline IC IN Properties 
    (h_a[125],h_w[125],Rho_a[125],C_p_a[125],Mu_a[125],k_a[125],Pr_a[125])=compressedairprop (T_[125], omega_[125], P_[125])   # Inline IC IN Properties 
    (m_dot_a[150],m_dot_w[150],omega_[150],T_sat[150])=condensate (m_dot_dry_air, m_dot_a[125], m_dot_w[125], omega_[125], P_[150], T_[150],150,P_w_amb,P_[100])  # Inline IC Out Properties  
    (h_a[150],h_w[150],Rho_a[150],C_p_a[150],Mu_a[150],k_a[150],Pr_a[150])=compressedairprop (T_[150], omega_[150], P_[150])   # Inline IC Out Properties 
    (Rho_a[137],C_p_a[137],Mu_a[137],k_a[137],Pr_a[137])=avgprop (Rho_a[125], C_p_a[125], Mu_a[125],k_a[125],Pr_a[125],Rho_a[150], C_p_a[150], Mu_a[150],k_a[150],Pr_a[150], 137)   # Inline IC AVG Props 
    Q_dot = ((m_dot_a[125] * h_a[125]) - (m_dot_a[150] * h_a[150])) + ((m_dot_w[150] * h_w[150]) - (m_dot_w[125] * h_w[125]))  #//Inline IC Total Heat Load 
    return (T_,P_,omega_,Q_dot,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a)
    
def M_DOT_H_None(T_,P_,omega_,Q,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a,P_w_amb):
    # M_dot_H iteration program for matching given Q
    C_p_a[137]=HAPropsSI('Cha','T',T_[150],'P',P_[150],'W',omega_[100])     # assumed avg as 150
    m_dot_max = (Q / C_p_a[137] * (T_[125] - T_[150]))*2                    # max value of m_dot_H considering ratio of Latent and sensible as 2
    m_dot_min=0
    m_dot_a[100] = (m_dot_min+m_dot_max)/2
    Q_dot=0
    while m_dot_min<m_dot_max and abs(Q-Q_dot)>1:
        # iterates m_dot_h via binary search to convolute to the Given Q with in error of 1
        (T_,P_,omega_,Q_dot,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a)=M_DOT_H(T_,P_,omega_,Q,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a,P_w_amb)
        if abs(Q-Q_dot)>1:
            if Q>Q_dot:
                m_dot_min=m_dot_a[100]
                m_dot_a[100] = (m_dot_min+m_dot_max)/2
            else:
                m_dot_max=m_dot_a[100]
                m_dot_a[100] = (m_dot_min+m_dot_max)/2
    return (T_,P_,omega_,Q_dot,m_dot_a,m_dot_w,T_sat,Rho_a,h_a,h_w,C_p_a,Mu_a,k_a,Pr_a)

def M_DOT_C(T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a):
    # Computes avg props used to compute Q based on m_dot_c with or without T_C_out
    (h_a[500],Rho_a[500],C_p_a[500],Mu_a[500],k_a[500],Pr_a[500])=coolingairprop(T_[500], omega_[500], P_[500],500)
    (h_a[525],Rho_a[525],C_p_a[525],Mu_a[525],k_a[525],Pr_a[525])= coolingairprop(T_[525], omega_[500], P_[500],525)
    (Rho_a[512],C_p_a[512],Mu_a[512],k_a[512],Pr_a[512]) = avgprop (Rho_a[500],C_p_a[500],Mu_a[500],k_a[500],Pr_a[500],Rho_a[525],C_p_a[525],Mu_a[525],k_a[525],Pr_a[525],512)
    Q_dot=m_dot_a[500]*(T_[525]-T_[500])*C_p_a[512]
    return (T_,P_,omega_,m_dot_a,Rho_a,h_a,C_p_a,Mu_a,k_a,Pr_a,Q_dot)



