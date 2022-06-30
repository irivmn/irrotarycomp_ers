convert_value={'mm_m':pow(10,-3)
            ,'L/min_m^3/s':1/60000
            ,'m^3/hr_m^3/s':1/3600
            ,'W/C_kW/C':pow(10,-3)
            ,'m^3/s_L/hr':3600000
            ,'micron_m':pow(10,(-6))
            ,'Pa_bar':pow(10,(-5))
            ,'W_KW':pow(10,-3)
            }

def convert(a,b):
    if a+"_"+b in convert_value:
        return convert_value[a+'_'+b]
    elif b+"_"+a in convert_value:
        return 1/convert_value[b+'_'+a]
    else:
        return 0


