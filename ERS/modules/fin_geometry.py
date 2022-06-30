from convertion import convert
from cmath import pi

#distionary elements is this order { Fin_Name:	[H=0, t=1, lambda_2=2, OL=3, FinType=4]}
Fin_parameter={ 'Hongsheng_wavy_9.5' : [9.5 ,0.15 ,2.25 ,0 ,'wavy']
                ,'Hongsheng_offset_3' : [3 ,0.2 ,2 ,5 ,'offset']
                ,'Hongsheng_offset_6.5' : [6.5 ,0.2	,2 ,5 ,'offset']
                ,'Hongsheng_offset_3.8' : [3.8 ,0.3	,2 ,5 ,'offset']
            }

#                   (D_out,D_fin,s_v,s_h,th_tube,th_fin,p_fin,Fintype)
Tube_fin_parameter={"Tube_fin25":[25,50,56,48.5,2,0.4,3.175,"Circular"]}


'''def geometry_name(L_core, T_core, n_coldrows, Fin_name,side):
    # Function for calculating geometry parameters of fin by name of fin alone from the library 
    H=Fin_parameter[Fin_name][0]*convert('mm','m')
    t=Fin_parameter[Fin_name][1]*convert('mm','m')
    lambda_=Fin_parameter[Fin_name][2]*convert('mm','m')
    OL=Fin_parameter[Fin_name][3]*convert('mm','m')
    type=Fin_parameter[Fin_name][4]
    
    if side=="cold":                        # for coldside
        th_Lbar = 11.5*convert('mm','m')
        W_core = L_core - 2 * th_Lbar
        if type=="wavy":  # for coldwavyfin
            L_core = T_core*1.083
        else:             # for coldoffsetfin
            L_core = T_core
    elif side=="hot":                        # for Hotside
        th_Wbar = 6*convert('mm','m')
        W_core = T_core - 2 * th_Wbar
        n_coldrows-=1
        if type=="wavy":    # for hotwavyfin
            L_core*=1.083
    else :
        print("ERROR")
    
    W = lambda_ - t
    Hi = H - t 
    Dh = (2*W*Hi)/(W+Hi)  
    Af = (W*Hi)/lambda_  
    At = (2*(W+Hi))/lambda_  
    Ap = (2*W)/lambda_  
    As = (2*Hi)/lambda_  
    FA = At*L_core*W_core*n_coldrows  
    Beta = FA/(H*W_core*L_core*n_coldrows)  
    Alpha = (Af*W_core*n_coldrows)/(H*W_core*n_coldrows)  
    A_face = (H*W_core*n_coldrows)
    return (W_core,L_core,W,Hi,n_coldrows,Dh,Af,At,Ap,As,FA,Beta,Alpha,A_face,H,lambda_,t,OL)'''

def geometry_value(L_core, T_core,H, lambda_, t, n_coldrows, side, type):
    # Function for calculating geometry parameters of fins by the values provided for the fins, does not refer to library of fins 
    # Assumption Units of parameters are coverted to m from mm in the main function
    if side=="cold":                        # for coldside
        th_Lbar = 11.5*convert('mm','m')
        W_core = L_core - 2 * th_Lbar
        if type=="wavy":  # for coldwavyfin
            L_core = T_core*1.083
        else:             # for coldoffsetfin
            L_core = T_core
    elif side=="hot":                        # for Hotside
        th_Wbar = 6*convert('mm','m')
        W_core = T_core - 2 * th_Wbar
        n_coldrows-=1
        if type=="wavy":    # for hotwavyfin
            L_core*=1.083
    else :
        print("ERROR")
    
    W = lambda_ - t
    Hi = H - t 
    Dh = (2*W*Hi)/(W+Hi)  
    Af = (W*Hi)/lambda_  
    At = (2*(W+Hi))/lambda_  
    Ap = (2*W)/lambda_  
    As = (2*Hi)/lambda_  
    FA = At*L_core*W_core*n_coldrows  
    Beta = FA/(H*W_core*L_core*n_coldrows)  
    Alpha = (Af*W_core*n_coldrows)/(H*W_core*n_coldrows)  
    A_face = (H*W_core*n_coldrows)
    return (W_core,L_core,W,Hi,n_coldrows,Dh,Af,At,Ap,As,FA,Beta,Alpha,A_face)
        
def corewidth (H_cs, n_cs,H_hs, n_hs): #: W_core)   
    th_middleplate = 0.5*convert('mm','m') # #[mm]*convert(mm,m) 
    th_cover = 3*convert('mm','m') # #[mm]*convert(mm,m) 
    W_core = (H_cs*n_cs)+(H_hs*n_hs)+(th_middleplate*(n_cs+n_hs+1))+(th_cover*4) 
    return W_core

def geometry(L_core, T_core, H, lambda_, t, n_coldrows,OL, Fin_name, side, type):
    # Function for calculating geometry parameters of fins by either values or name provided for the fins
    # Units of parameters are coverted to m in the function  
    if(Fin_name==None and H==None ):
        print("ERROR")
        exit()
    elif(Fin_name!=None and H!=None):
        print("ERROR : Both are given")
        exit()
    elif(Fin_name!=None):
            H=Fin_parameter[Fin_name][0]*convert('mm','m')
            t=Fin_parameter[Fin_name][1]*convert('mm','m')
            lambda_=Fin_parameter[Fin_name][2]*convert('mm','m')
            OL=Fin_parameter[Fin_name][3]*convert('mm','m')
            type=Fin_parameter[Fin_name][4]

    if side=="cold":                        # for coldside
        th_bar = 11.5*convert('mm','m') 
        W_core = L_core - 2 * th_bar 
        if type=="wavy":  # for coldwavyfin
            L_core = T_core*1.083
        else:             # for coldoffsetfin
            L_core = T_core
    elif side=="hot":                        # for Hotside
        th_bar = 6*convert('mm','m')
        W_core = T_core - 2 * th_bar
        n_coldrows-=1
        if type=="wavy":    # for hotwavyfin
            L_core*=1.083
    else :
        print("ERROR")
    
    W = lambda_ - t
    Hi = H - t 
    Dh = (2*W*Hi)/(W+Hi)  
    Af = (W*Hi)/lambda_  
    At = (2*(W+Hi))/lambda_  
    Ap = (2*W)/lambda_  
    As = (2*Hi)/lambda_  
    FA = At*L_core*W_core*n_coldrows  
    Beta = FA/(H*W_core*L_core*n_coldrows)  
    Alpha = (Af*W_core*n_coldrows)/(H*W_core*n_coldrows)  
    A_face = (H*W_core*n_coldrows)
    A_per_layer = W_core* L_core
    A_total = A_per_layer* n_coldrows
    Unit_weight = (( H-2* t)* t+( lambda_+ t)* t)*2700/ lambda_
    fin_weight = Unit_weight* A_total

    n_seal = n_coldrows*2
    B_seal = th_bar
    T_seal = T_core
    Unit_weight_seal = B_seal* H*2700
    seal_weight = Unit_weight_seal * T_seal* n_seal

    Total_fin_weight= fin_weight + seal_weight

    return (W_core,L_core,W,Hi,n_coldrows,Dh,Af,At,Ap,As,FA,Beta,Alpha,A_face,H,lambda_,t,OL,Total_fin_weight)

def geometry_TubeFin(D_out,D_fin,s_v,s_h,th_tube,th_fin,p_fin,Fintype,N_t_row,N_t_col,N_pass_hs,L_core ):

    W_core=s_v * N_t_row  #//Height of heat exchanger face 
    T_core =s_h * N_t_col  #//Length of heat exchanger in air flow direction 
    
    #//Tube geometry calculations     
    D_in=D_out-2*th_tube  #//Inner diameter of Tube  
    N_circuits = (N_t_row*N_t_col)/N_pass_hs #//Number of Circuits  
    L_tube=N_pass_hs*L_core  #//Total tube length  
    A_s_h = pi*D_in*L_tube*N_circuits  #//Inner Surface Area of Tube  
    A_flowarea_h = pi*0.25*pow(D_in,2)*N_circuits  #//Inner Surface Area of Tube 

    #//Fin Geometry   
    N_fin=L_core/p_fin   #//Number of fins  
    A_s_fin = N_t_row* N_t_col*(L_core/p_fin)*(pi*(pow(D_fin,2)-pow(D_out,2))/2+D_fin*th_fin) #//Total fin area   
    A_s_unfin =pi*N_t_row*N_t_col*L_tube*D_out*(p_fin-th_fin)/p_fin  #//Total Un-finned area 
    A_s_c = A_s_fin + A_s_unfin  #//Total air-side surface area  
    A_flowarea_c = (N_t_row*L_core/p_fin)*(s_v*p_fin-(D_fin-D_out)*th_fin-p_fin*D_out)   
    A_face_c = L_core*W_core 

    return (W_core,T_core,D_in,N_circuits,L_tube,A_s_h,A_flowarea_h,N_fin,A_s_fin,A_s_unfin,A_s_c,A_flowarea_c,A_face_c)

def Platebar_Weight(weight_hs,weight_cs,H_cs,n_cs,H_hs,n_hs,L_core,T_core):
    n_total = n_cs + n_hs +1
    A_per_Sep =L_core* T_core
    A_total_sep = A_per_Sep* n_total
    t_sep = 0.6 *10**(-3)
    Unit_weight_sep = t_sep* 2700
    Tot_weight_sep = Unit_weight_sep * A_total_sep
        
    t_cover = 3*10**(-3)
    A_total_cover = A_per_Sep*2
    Unit_weight_cover = t_cover * 2700
    Tot_weight_cover = Unit_weight_cover * A_total_cover

    weight_core=(weight_hs+weight_cs+Tot_weight_sep+Tot_weight_cover)*1.2

    return weight_core


        