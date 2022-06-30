from scipy import interpolate

def P_Interpolation(M_data,P_input):
    Model_id=[]
    P=[]
    p_S1 =[]
    p_S2=[]
    FAD = []
    Q_sh = []
    Pr_ratio_stg1 = []
    Pr_ratio_stg2 = []
    n_stg1 = []
    n_stg2 = []

    for i in M_data:
        Model_id.append(i.Model_id)
        P.append(i.P)
        p_S1.append(i.p_S1)
        p_S2.append(i.p_S2)
        FAD.append(i.FAD)
        Q_sh.append(i.Q_sh)
        Pr_ratio_stg1.append(i.Pr_ratio_stg1)
        Pr_ratio_stg2.append(i.Pr_ratio_stg2)
        n_stg1.append(i.n_stg1)
        n_stg2.append(i.n_stg2)

    P = tuple(P)
    p_S1 = tuple(p_S1)
    p_S2 = tuple(p_S2)
    FAD = tuple(FAD)
    Q_sh = tuple(Q_sh)
    Pr_ratio_stg1 = tuple(Pr_ratio_stg1)
    Pr_ratio_stg2 = tuple(Pr_ratio_stg2)
    n_stg1 = tuple(n_stg1)
    n_stg2 = tuple(n_stg2)

    _p_S1 = interpolate.splrep(P,p_S1)
    _p_S2= interpolate.splrep(P,p_S2)
    _FAD = interpolate.splrep(P,FAD)
    _Q_sh = interpolate.splrep(P,Q_sh)
    _Pr_ratio_stg1 = interpolate.splrep(P,Pr_ratio_stg1)
    _Pr_ratio_stg2 = interpolate.splrep(P,Pr_ratio_stg2)
    _n_stg1 = interpolate.splrep(P,n_stg1)
    _n_stg2 = interpolate.splrep(P,n_stg2)

    I_p_S1 = round(float(interpolate.splev(P_input,_p_S1)),3)
    I_p_S2= round(float(interpolate.splev(P_input,_p_S2)),3)
    I_FAD = round(float(interpolate.splev(P_input,_FAD)),0)
    I_Q_sh = round(float(interpolate.splev(P_input,_Q_sh)),1)
    I_Pr_ratio_stg1 = round(float(interpolate.splev(P_input,_Pr_ratio_stg1)),3)
    I_Pr_ratio_stg2 = round(float(interpolate.splev(P_input,_Pr_ratio_stg2)),3)
    I_n_stg1 = round(float(interpolate.splev(P_input,_n_stg1)),3)
    I_n_stg2 = round(float(interpolate.splev(P_input,_n_stg2)),3)

    return(I_p_S1,I_p_S2,I_FAD,I_Q_sh,I_Pr_ratio_stg1,I_Pr_ratio_stg2,I_n_stg1,I_n_stg2)


