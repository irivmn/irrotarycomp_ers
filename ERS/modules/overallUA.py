from cmath import tanh

def overallucoeff (alpha_cs, t_cs,H_cs, As_cs,At_cs,alpha_hs,t_hs,H_hs,As_hs,At_hs,FA_cs,FA_hs): #: UA_hs,UA_cs,UA)   
    k_cs = 192 #[W/m C]  
    m_cs = pow(((2*alpha_cs)/(k_cs*t_cs)),(1/2))
    eta_f_cs = (tanh(m_cs*H_cs*0.5)/(m_cs*H_cs*0.5)).real                 
    eta_O_cs = 1- ((1-eta_f_cs)*(As_cs/At_cs))   
    k_hs = 192 #[W/m C]   
    m_hs = pow(((2*alpha_hs)/(k_hs*t_hs)),(1/2)) 
    eta_f_hs = (tanh(m_hs*H_hs*0.5)/(m_hs*H_hs*0.5)).real                 
    eta_O_hs = 1- ((1-eta_f_hs)*(As_hs/At_hs))  
    #//Overall Heat Transfer Calcualtion   
    alpha_0_cs = 1/((1/(alpha_cs*eta_O_cs))+(FA_cs/(FA_hs*alpha_hs*eta_O_hs)))  
    alpha_0_hs = 1/((1/(alpha_hs*eta_O_hs))+(FA_hs/(FA_cs*alpha_cs*eta_O_cs)))    
    UA_hs = alpha_0_hs*FA_hs  
    UA_cs = alpha_0_cs*FA_cs
    UA = max(UA_hs,UA_cs)
    return (UA_hs,UA_cs,UA)