from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import uuid

from .forms import *
from .models import *
from .models import Stock_Companies
from datetime import datetime

########################  Backend File Imports  ###########################

from .utils.Market_Summary import Today_Market
from .utils.Historic_Data import DataReader
from .utils.Candel_Chart import Candlestic
from .utils.Stock_Predictions import Prediction
from plotly.offline import plot
import pandas as pd
import numpy as np
from django.db.models import Q

##########################################################################

# Registration View
def register_user(request):    

    if request.method == 'POST':

        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, 'Username is already taken')
                return redirect('register')

            if not username:
                messages.add_message(request, messages.ERROR, 'Username is required!')
                return redirect('register')

            if not email:
                messages.add_message(request, messages.ERROR, 'Email is required!')
                return redirect('register')
            
            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, 'Email already exists, user another one.')
                return redirect('register')

            if len(password1) < 8:
                messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                return redirect('register')
        
            if password1 != password2:
                messages.add_message(request, messages.ERROR, 'Password does not match')
                return redirect('register')
            
            user_obj = User.objects.create_user(username=username, email=email, password=password1)
            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()

            verification_email(email, auth_token, username)
            messages.success(request, 'Verification Email Sent! Check your Mail.')
            return redirect('register')

        except:
            return render('error')

    return render(request, 'register.html')


# Login View
def login_signup(request):

    if request.user.is_authenticated:
        return redirect('market_summary')
    
    else:   
        try:  
            if request.method == 'POST':

                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
 
                profile_obj = Profile.objects.filter(user = user).first()

                if user is not None:
                    if profile_obj.is_verified:
                        Profile.objects.update(reset_password=False)
                        auth_login(request,user)
                        return redirect('market_summary')
                    else:
                        messages.error(request, 'You are not Verified! Please check Email.')
                else:
                    messages.error(request, 'Invalid Username or Password!')
        except:
            messages.error(request, 'An Error Occured!')
            return redirect('login_signup')

    return render(request, 'login_signup.html')               

# Edit User
def profile_update(request):
    
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':

                email1 = request.POST.get('email')
                username1 = request.POST.get('username')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')

                if len(password1) < 8:
                    messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                    return redirect('profile')

                if password1 != password2:
                    messages.add_message(request, messages.ERROR, 'Password does not match')
                    return redirect('profile')

                if User.objects.filter(email=email1).first():
                    user = User.objects.get(email=email1)
                    user.username = username1
                    user.email = email1
                    user.set_password(password1)
                    user.save()
                    auth_login(request, user)
                    messages.success(request, 'Successfully changed User Details')
                    return redirect('profile')

                else:
                    messages.error(request, "No User Found!")
                    return redirect('profile')

        except:
            messages.error(request, 'An Error Occured during process!')
            return redirect('profile')  

    else:
        return redirect('login_signup')


############################## Email Verification Views ###############################

# Verification for Email
def verification_email(email,token, username):
    subject = 'Your account needs to be verified'
    message = f'Hi {username}! , Please use this link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)


# Verify Email Token
def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your Account has been Verified!')
            return redirect('login_signup')
        else:
            return redirect('error')
    except Exception as e:
        print(e)


########################### Forgot Password Views #################################

# Password Update
def update_password(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).first():

            if Profile.objects.filter(is_verified=True):

                data = User.objects.get(email = email)
                auth_token = str(uuid.uuid4())
                
                Profile.objects.update(auth_token = auth_token)
            
                request.session['email'] = email
                username = data.username

                messages.success(request, 'We have sent you an Email with the Link!')

                password_verify(email, auth_token, username)
                return redirect('update')
            
            else:
                messages.error(request, 'User is not verified yet!')
                return redirect('forgot_password')
        
        else:
            messages.error(request, "Invalid Email! Please enter a Valid Email Address")
            return redirect('forgot_password')
        
    return render(request, 'error.html')

# Password Token Email
def password_verify(email,token, username):
    subject = 'Request for Password Change!'
    message = f'Hi {username}! , Please use this link to reset your password: http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail(subject, message, email_from, recipent_list)

# Verify Password 
def change_password(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.reset_password = True
            profile_obj.save()
            messages.success(request, 'Email Verified! Now you can change your Password.')
            return redirect('update')
        else:
            return redirect('error')
    except Exception as e:
        print(e)

    return redirect('error')

# Update Password
def update(request):
    email = request.session['email']

    if request.method == 'POST':
        try:
            if Profile.objects.filter(reset_password=True):

                password = request.POST.get('password')
                password1 = request.POST.get('password1')
                
                if len(password) < 8:
                    messages.add_message(request, messages.ERROR, 'Password should be atleast 8 characters, should be alpha numeric')
                    return redirect('update')

                if password != password1:
                    messages.add_message(request, messages.ERROR, 'Password does not match')
                    return redirect('update')

                user = User.objects.filter(email=email).first()
                user.set_password(password1)
                user.save()

                messages.success(request, 'Password Changed Successfully!')
                return redirect(login_signup)
            
            else:
                messages.error(request, 'Email not verified yet!')
        except:
                messages.error(request, 'Update Error')
                return redirect('error')
        
    return render(request, 'update.html')

###################### Main Views ##########################

# Index View
def index(request):
    if request.user.is_authenticated:  
        return render(request, 'index.html')
    else:
        return render(request, 'login_signup.html')

# Register Page
def register(request): 
    return render(request, 'register.html')

# Register Page
def login(request): 
    return render(request, 'login_signup.html')

# Aboutus View
def aboutus(request):
  if request.user.is_authenticated:    
        return render(request, 'aboutus.html')
  else:
        return redirect('login_signup')

def profile(request):
  if request.user.is_authenticated:    
        return render(request, 'profile.html')
  else:
        return redirect('login_signup')

#Error Page
def error_page(request):
    return render(request, 'error.html')

# Forgot Password View
def forgot_password(request):
        return render(request, 'forgot_password.html')

# Logout View
def logoutUser(request):
    logout(request)
    return redirect('login_signup')

#########################################################################################

# View for Today's Market 
def market_summary(request):
    if request.user.is_authenticated:
        try:
            print(1)
            global M_data
            obj = Today_Market()
            M_data=obj.Scrap_Table
            fig, config = obj.Table_Dsg(M_data)
            table_dsg = plot(fig, config=config, output_type='div')
            return render(request, 'market_summary.html' , context={'table_dsg': table_dsg}) 

        except:
            messages.error(request, 'Please check your connection and try again...')
            return redirect('error')
    else:
        return redirect('login_signup')

# View for Market Charts
def market_charts(request):
    if request.user.is_authenticated:
        try:
            obj = Today_Market()
            fig, config = obj.Market_Dsg(M_data)
            market_dsg = plot(fig, config=config, output_type='div')
            return render(request, 'market_charts.html' , context={'market_dsg': market_dsg})

        except:
            messages.error(request, 'Please Download Market Summary Data first!')
            return redirect('error')
    else:
        return redirect('login_signup')

# View for Bullet Charts
def bullet_charts(request):
    if request.user.is_authenticated:
        try:
            obj = Today_Market()
            fig, config = obj.Bullet_Dsg(M_data)
            bullet_dsg = plot(fig, config=config, output_type='div')
            return render(request, 'bullet_charts.html' , context={'bullet_dsg': bullet_dsg}) 

        except:
            messages.error(request, 'Please Download Market Summary Data first!')
            return redirect('error')
    else:
        return redirect('login_signup')

# View for Pie Charts
def pie_charts(request):
    if request.user.is_authenticated:
        try:
            obj = Today_Market()
            fig, config = obj.Pie_Dsg(M_data)
            pie_dsg = plot(fig, config=config, output_type='div')
            return render(request, 'pie_charts.html' , context={'pie_dsg': pie_dsg}) 

        except:
            messages.error(request, 'Please Download Market Summary Data first!')
            return redirect('error')
    else:
        return redirect('login_signup')

# Top 10 Companies View
def top_comp(request):
    if request.user.is_authenticated:
        try:
            obj = Today_Market()
            fig, config = obj.Tt_Com_Dsg(M_data)
            tt_com_dsg = plot(fig, config=config, output_type='div')
            return render(request, 'top_comp.html' , context={'tt_com_dsg': tt_com_dsg}) 
        
        except:
            messages.error(request, 'Please Download Market Summary First!')
            return redirect('error')
    else:
        return redirect('login_signup')

# View for Stock Name 
def stock_name(request):

    companies=pd.read_json("https://dps.psx.com.pk/symbols")

    
    companies.drop(['isETF','isDebt', 'isGEM'], axis=1, inplace=True)
    regex = '(?:.*MTH.*|.*DEFAULTER SEGMENT.*|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))'
    
    companies.drop(companies[companies.name.str.contains(regex).fillna(False)].T, axis=0, inplace=True)
    companies['name'].replace('', np.nan, inplace=True)
    companies['sectorName'].replace('', np.nan, inplace=True)
    
    companies.dropna(subset = ['name','sectorName'], inplace = True)
    
    companies.sectorName = companies.sectorName.str.replace("/", "")
 
    df_records = companies.to_dict('records')
    model_instances = [
        Stock_Companies
        (
            symbol=record['symbol'],
            name=record['name'],
            sectorName=record['sectorName'],
        ) for record in df_records]
        
    Stock_Companies.objects.bulk_create(model_instances)
    return render(request, 'historic_fm.html')

# View for Stock Searching
def stock_search(request):
    
    if request.method == "POST":
        searched = request.POST['searched']
 
        companies = Stock_Companies.objects.filter( Q(symbol__icontains=searched) | Q(name__icontains=searched) | Q(sectorName__icontains=searched))
        
        return render(request, 'stock_search.html', {'searched':searched,'companies':companies})
        
    else:
        return render(request, 'stock_search.html', {})

# View for Historic Form
def historic_fm(request):
    if request.user.is_authenticated:
        try:
            companies = Stock_Companies.objects.values_list('symbol', flat=True)
            comp = []
            for i in companies:
                if i not in comp:
                    comp.append(i)
            return render(request, 'historic_fm.html', {'comp': comp})
        
        except:
            messages.error(request, 'Please check your connection and try again...')
            return redirect('error')
    else:
        return redirect('login_signup')

# View for Historic Data
def historic_data(request):
    if request.method == "POST":

        try:
            stockcompanies = request.POST["stockcompanies"]
            startdate = request.POST["startdate"]
            startdate = datetime.strptime(startdate, '%Y-%m-%d')
            enddate = request.POST["enddate"]
            enddate = datetime.strptime(enddate, '%Y-%m-%d')
            data_reader = DataReader()
            global H_data
            H_data = data_reader.stocks(stockcompanies, start = startdate, end=enddate)
            data=H_data
            data["Date"] = pd.DatetimeIndex(data["Date"]).strftime("%Y-%m-%d")
            
            fig, config = data_reader.Table_Dsg(data)

            h_table_dsg = plot(fig, config=config, output_type='div')
            
            return render(request, "historic_data.html",{'h_table_dsg': h_table_dsg })
            
        except:
            messages.error(request, 'Please Download Historic data first!')
            return redirect('historic_fm')

    else:
        return render(request, 'historic_fm.html', {})

# Candle Chart View
def candelistic(request):
    if request.user.is_authenticated:
        try:
            data=H_data  
            obj = Candlestic(data) 
            fig, config = obj.can_gph
            can_dsg = plot(fig, config=config, output_type='div')
            return render(request, 'candelistic.html', {'can_dsg':can_dsg})
        except:
            messages.error(request, 'Please Download Historic data first!')
            return redirect('historic_fm')
    else:
        return redirect('login_signup')

# Predictions View
def prediction(request):
    if request.user.is_authenticated:
        try:
            data = H_data
            if len(data) > 50:
                data = data.drop('Volume', axis=1)
                global P_data 
                obj= Prediction(data)
                P_data=obj.pre_data

                fig, config=obj.Pred_Dsg(P_data)
                pre_dsg = plot(fig, config=config, output_type='div')
                return render(request, 'predictions.html', {'pre_dsg':pre_dsg})
            else:
                messages.error(request, 'Data is not enough to make Predictions. Please download again!')
                return redirect('historic_fm')
        except:
            messages.error(request, 'Please Download Historic data first!')
            return redirect('historic_fm')    
    else:
        return redirect('login_signup')

# Data Download View
def data_download(request):
    # Creating Response with csv content
    response = HttpResponse(content_type="text/csv")
 
    if request.POST.get("mrsum_btn"):
        # Renaming the result column header
        M_data.columns = ["SCRIP", "LDCP", "OPEN", "HIGH","LOW", "CURRENT", "CHANGE", "VOLUME"]
 
        # Disposing 
        response["Content-Disposition"] = "attachment; filename=Market_Summary.csv"
        M_data.to_csv(path_or_buf=response)
    elif request.POST.get("his_btn"):
        # Renaming the result column header
        H_data.columns = ["Date", "Open", "High", "Low","Close","Volume"]
 
        # Disposing 
        response["Content-Disposition"] = "attachment; filename=Historic_Data.csv"
        H_data.to_csv(path_or_buf=response)
    elif request.POST.get("pre_btn"):
        # Renaming the result column header
        P_data.columns = ["Date", "Open", "High", "Low","Close"]
 
        # Disposing 
        response["Content-Disposition"] = "attachment; filename=Prediction_Data.csv"
        P_data.to_csv(path_or_buf=response)
 
    return response