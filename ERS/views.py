from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from CoolerProps.settings import EMAIL_HOST_USER
from django.shortcuts import render
from ERS.demo1 import *
from ERS.ERS_Trial1 import *
import math, random
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
import csv,json

a_user=None
user=None

def home(request):
    return render(request,"login.html")

def logout_out(request):
    print("logged out..")
    logout(request)
    return redirect("/")

def login_in(request):
    if request.method=="POST":
        username=request.POST['username']
        psw=request.POST['psw']

        user=authenticate(username=username,password=psw)
        print(user)
        if user is not None:
            check=Registration_Approval.objects.filter(UserID = username,Aprove=0)
            if len(check)!=0:
                login(request,user)
                return redirect(Main_home)
            else:
                return render(request,"login.html",{'error':"Wait for Admin approval."})
        else:
            return render(request,"login.html",{'error':"Incorrect userId or password"})

        '''user=users.objects.filter(userID=username,password=psw)
        print(len(user))
        if len(user)!=0:
            check=Registration_Approval.objects.filter(UserID = username,Aprove=0)
            if len(check)!=0:
                return Main_home(request)
            else:
                return render(request,"login.html",{'error':"Wait for Admin approval."})
        else:
            return render(request,"login.html",{'error':"Incorrect userId or password"})'''
    else:
        return redirect("/")

def Main_home(request):
    return render(request,"Home.html")

def register(request):
    if request.method == 'POST':
        username = request.POST['userid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        #phone = request.POST['phone']
        #dob = request.POST['dob']
        psw1 = request.POST['psw1']
        psw2 = request.POST['psw2']

        '''user1=users.objects.filter(userID=username)
        user2=users.objects.filter(Email=email)
        print(user1.count())
        print(user2.count())'''
        if User.objects.filter(username=username).exists():
            return render(request,"register.html",{"error":"Username is already taken","fname":fname,"lname":lname,"email":email,"userid":username})
        elif User.objects.filter(email=email).exists():
            return render(request,"register.html",{"error":"Mail-id is already taken","fname":fname,"lname":lname,"email":email,"userid":username})
        elif psw1!=psw2:
            return render(request,"register.html",{"error":"Password mismatch","fname":fname,"lname":lname,"email":email,"userid":username})
        else:
            print("Account registered successfully..")
            #request.session['username']=username
            user= User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=psw1)
            user.save()
            print("DONE")
            Reg_App=Registration_Approval(UserID=username,Email=email,Aprove=1)
            Reg_App.save()
            ######################### mail system ####################################
            '''sub='welcome to SNS'
            message= f"Your registration is successful.."
            email_from= settings.EMAIL_HOST_USER
            to= [email]
            send_mail( sub,message,email_from,to)'''
            return redirect("/",{"error":"Wait for admin approval.."})
    else:
        return render(request,"register.html")

def forgot_password(request):
    if request.method=="POST":
        sub="Reset OTP."
        message=f'Your OTP to reset password is 123456.'
        to=["pavan0312c@gmail.com"]
        email_from=settings.EMAIL_HOST_USER
        print(email_from)
        send_mail(sub,message,email_from,to)
        return render(request,"login.html")
    else:
        return render(request,"forgot_password.html")

def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_otp(request):
    email=request.GET.get("T_amb")
    print(email)
    o=generateOTP()
    htmlgen = '<p>Your OTP is <strong>o</strong></p>'
    print(o)
    #send_mail('OTP request',o,'<your gmail id>',[email], fail_silently=False, html_message=htmlgen)
    return HttpResponse(o)

def sampleotp(request):
    return render(request,"smapleotp.html")

def password_trial(request):
    return render(request,"password_trial.html")

def demo1(request):
    if request.method=="POST":
        T_amb=request.POST['T_amb']
        RH_amb=request.POST['RH_amb']
        Altitude=request.POST['Altitude']
        FTPQ=request.POST['HCA']
        print(FTPQ)
        HCA=HCA_details.objects.filter(name=FTPQ)
        print(HCA)
        for i in HCA:
            data=i
        print(data.FAD)
        print(data.T_H_In)
        print(data.P_input)
        print(data.Q_input)
        (Q,Weight)=demo123(T_amb,RH_amb,Altitude,data)
        return render(request,"demo1.html",{'T_amb':T_amb,"RH_amb":RH_amb,"Altitude":Altitude,"HCA":FTPQ,"Q":Q,"Weight":Weight})
    else:
        return render(request,"demo1.html",{"Q":Q,"Weight":Weight})
        

    
def reset_password(request):
    un = request.GET["username"]
    try:
        #user = get_object_or_404(User,username=un)
        user = "Pavan"
        otp = random.randint(1000,9999)
        msz="hi...."
        #msz = "Dear {} \n{} is your One Time Password (OTP) \nDo not share it with others \nThanks&Regards \nMyWebsite".format(user.username, otp)
        try:
            #email = EmailMessage("Account Verification",msz,to=[user.email])
            #email.send()
            print("Email Sent...")
            #return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
            return JsonResponse({"status":"sent","email":"abc@gmail.com","rotp":otp})
        except:
            print("Email Sent1...")
            return JsonResponse({"status":"error","email":user.email})
    except:
        print("Email Sent2...")
        return JsonResponse({"status":"failed"})

def admin_main(request):
    Reg_app=Registration_Approval.objects.filter(Aprove=1)
    Ret_app=Reset_password_Approval.objects.filter(Aprove=1)
    user_d=User.objects.all()
    HCA_d=HCA_details.objects.all()
    CD26_a_d=CD26_airend_data.objects.all()
    CD26_a_d_r=CD26_airend_data_rated.objects.all()
    #return render(request,"admin_main.html",{'Reg_app':Reg_app,'Ret_app':Ret_app})
    return render(request,"Admin_All.html",{'Reg_app':Reg_app,'Ret_app':Ret_app,'user_d':user_d,'HCA_d':HCA_d,'CD26_a_d':CD26_a_d,'CD26_a_d_r':CD26_a_d_r})

def Register_request(request):
    if request.POST['approve']=="Approve":
        userid=request.POST['userid']
        print(userid)
        X=Registration_Approval.objects.filter(UserID = userid).update(Aprove=0)
        print("Approved")
    elif request.POST['approve']=="Reject":
        X=Registration_Approval.objects.filter(UserID = userid).update(Aprove=-1)
        print("Rejected")
    Reg_app=Registration_Approval.objects.filter(Aprove=1)
    Ret_app=Reset_password_Approval.objects.filter(Aprove=1)
    return render(request,"admin_main.html",{'Reg_app':Reg_app,'Ret_app':Ret_app})


def Reset_pwd_request(request):
    if request.POST['approve']=="Approve":
        userid=request.POST['userid']
        print(userid)
        X=Reset_password_Approval.objects.filter(UserID = userid).update(Aprove=0)
        Y=Reset_password_Approval.objects.filter(UserID = userid)
        for i in Y:
            psw=i.Password
        Z=User.objects.filter(userID = userid).update(password=psw)                ####testing pending
        print("Approved")
    elif request.POST['approve']=="Reject":
        X=Reset_password_Approval.objects.filter(UserID = userid).update(Aprove=-1)
        print("Rejected")
    Reg_app=Registration_Approval.objects.filter(Aprove=1)
    Ret_app=Reset_password_Approval.objects.filter(Aprove=1)
    return render(request,"admin_main.html",{'Reg_app':Reg_app,'Ret_app':Ret_app})


def upload_data(request):
    path="C:\\Users\\pxc2007.ext\\Desktop\\CD26 Airend Data Rated pressure.CSV"
    list=[]
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(row)
    for i in range(len(list)):
        add= CD26_airend_data_rated(Model_id=list[i][0],rated_P=float(list[i][1]))
        ''',p_S1=float(list[i][2]),p_S2=float(list[i][3]),FAD=float(list[i][4]),
            Q_sh=float(list[i][5]),Pr_ratio_stg1=float(list[i][6]),Pr_ratio_stg2=float(list[i][7]),n_stg1=float(list[i][8]),n_stg2=float(list[i][9]))'''
        add.save()
        print(i)
    list=Reset_password_Approval.objects.filter(Aprove=1)
    for i in list:
        print(i.UserID)   
        print(i.Email )
        print(i.Aprove)
    return render(request,"admin_main.html",{'data':list})

def calculate(request):
    if(request.method=="POST"):
        T_amb=request.POST['T_amb']
        RH_amb=request.POST['RH_amb']
        Altitude=request.POST['Altitude']
        model_id=request.POST['Model_id']
        P=request.POST['P']
        Pr_type=request.POST['Pressure']
        TW_in=request.POST['T_in']
        TW_out=request.POST['T_out']
        CTD_ac=request.POST['CTD_ac']
        CTD_ic=request.POST['CTD_ic']
        input_=[T_amb,RH_amb,Altitude,model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic]
        RP=CD26_airend_data_rated.objects.filter(Model_id=model_id)
        for i in RP:
            data=i
        Rated_P=data.rated_P
        MD=CD26_airend_data.objects.filter(Model_id=model_id,P=Rated_P)
        for i in MD:
            data=i
        M_data=data
        print("-------------------------------",M_data.P)
        (WF,ReH,DT)=ERS_TRIAL(float(T_amb),float(RH_amb),float(Altitude),model_id,float(P),Pr_type,float(TW_in),float(TW_out),float(CTD_ac),float(CTD_ic),M_data)
        print(T_amb,RH_amb,Altitude,model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic)
        
        list=CD26_airend_data_rated.objects.all()
        return render(request,"Home.html",{"model_id":list,"WF":WF,"ReH":ReH,"DT":DT})
    else:
        WF,ReH,DT=10,15,20
        list=CD26_airend_data_rated.objects.all()
        return render(request,"Home.html",{"model_id":list,"WF":WF,"ReH":ReH,"DT":DT})

def send_data(request):
    if request.method=="POST":
        TYPE=request.POST['TYPE']
        T_amb=request.POST['T_amb']
        RH_amb=request.POST['RH_amb']
        Altitude=request.POST['Altitude']
        model_id=request.POST['Model_id']
        P=request.POST['P']
        Pr_type=request.POST['Pr_type']
        TW_in=request.POST['T_in']
        TW_out=request.POST['T_out']
        CTD_ac=request.POST['CTD_ac']
        CTD_ic=request.POST['CTD_ic']
        input_=[T_amb,RH_amb,Altitude,model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic]
        if Pr_type=="Rated_Pressure":
            RP=CD26_airend_data_rated.objects.filter(Model_id=model_id)
            for i in RP:
                data=i
            Rated_P=data.rated_P
            MD=CD26_airend_data.objects.filter(Model_id=model_id,P=Rated_P)
            for i in MD:
                data=i
            M_data=data
        else:
            M_data=CD26_airend_data.objects.filter(Model_id=model_id)
        (WF,ReH,DT)=ERS_TRIAL(float(T_amb),float(RH_amb),float(Altitude),model_id,float(P),Pr_type,float(TW_in),float(TW_out),float(CTD_ac),float(CTD_ic),M_data)
        print(TYPE,T_amb,RH_amb,Altitude,model_id,P,Pr_type,TW_in,TW_out,CTD_ac,CTD_ic)
        print(model_id,"-------------------------------------------------------------------")
        return HttpResponse(json.dumps({ "WF":WF, "ReH":ReH, "DT":DT}),content_type ="application/json")

def home_parallel(request):
    list=CD26_airend_data_rated.objects.all()
    data={}
    data1={}
    for i in list:
        data[i.Model_id]=i.Max
        data1[i.Model_id]=i.T_W_out
    #print(data)
    max_v=json.dumps(data)
    max_T=json.dumps(data1)
    return render(request,"Home_parallel.html",{"model_id":list,"max_v":max_v,"max_T":max_T})


def home_series(request):
    list=CD26_airend_data_rated.objects.all()
    data={}
    data1={}
    for i in list:
        data[i.Model_id]=i.Max
        data1[i.Model_id]=i.T_W_out
    #print(data)
    max_v=json.dumps(data)
    max_T=json.dumps(data1)
    return render(request,"Home_series.html",{"model_id":list,"max_v":max_v,"max_T":max_T})

def HTP(request):
    list=CD26_airend_data_rated.objects.all()
    data={}
    data1={}
    for i in list:
        data[i.Model_id]=i.Max
        data1[i.Model_id]=i.T_W_out
    #print(data)
    max_v=json.dumps(data)
    max_T=json.dumps(data1)
    return render(request,"HPT.html",{"model_id":list,"max_v":max_v,"max_T":max_T})

def reset_password(request):
    if request.method=="POST":
        username=request.POST['userid']
        email=request.POST['email']
        user=users.objects.filter(userID=username,Email=email)
        print(len(user))
        if len(user)==0:
            return render(request,"reset_password.html",{"error":"User not exist..","uid":username,"eid":email})
        psw1=request.POST['psw1']
        psw2=request.POST['psw2']
        if psw1==psw2:
            ReP_App=Reset_password_Approval(UserID=username,Email=email,Password=psw1,Aprove=1)
            ReP_App.save()
            return render(request,"Login.html",{"error":"Wait for admin approval.."})
        else:
            return render(request,"reset_password.html",{"error":"Password not matching..","uid":username,"eid":email})
    else:
        return render(request,"reset_password.html")

def admin_login(request):
    if request.method=="POST":
        username=request.POST['username']
        psw=request.POST['psw']
        a_user=authenticate(username=username,password=psw)
        print(a_user)
        if a_user is not None:
            if  a_user.is_authenticated:
                print("Authenticated")
            check=User.objects.filter(username=username,is_superuser = True)
            print(len(check))
            for i in check:
                print(i)
            if len(check)!=0:
                login(request,a_user)
                return redirect(admin_main)
            else:
                return render(request,"Admin_login.html",{'error':"You don't have access to admin"})
        else:
            return render(request,"Admin_login.html",{'error':"Incorrect adminId or password"})
    else:
        return render(request,"Admin_login.html")

