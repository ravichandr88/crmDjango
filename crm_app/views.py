from django.shortcuts import render,HttpResponse,redirect
from .forms import SignUpForm,LoginForm
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User_Details,Reporter_Data,Roles,Courses,Invoice_List,Lead_List,Bill,Installments
import numpy as np
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.forms.models import model_to_dict
import datetime
# Create your views here.



def signupview(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            userData =  User_Details(username=user.username,designation=form.cleaned_data.get('designation'))
            userData.save()
            user.save()
            data = {'username':user.username,'email':user.email}
            return JsonResponse(data)
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})



def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return HttpResponse("Successfully logged in")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form' : form})




@csrf_exempt
@api_view(['GET', 'POST', ])
def reportersList(request):
    if request.method == 'GET':
        users = User_Details.objects.values_list('username','id')
        users=list(users)
        # j = 0
        # for i in users:
        #     usr = User_Details.objects.get(id=i[1])
        #     rprtList = usr.report_list.all()
        #     rprtList = list(rprtList)
        #     users[j] =  i +(rprtList,)
        #     j += 1
        w = 0
        for j in users:
            usr = User_Details.objects.get(id=j[1])
            f=[]
            rpl = list(Reporter_Data.objects.values_list('report_from','report_to'))
            for m in rpl:
                if usr.id == m[1]:
                    f.append(User_Details.objects.get(id=m[0]).username)
            users[w] = j + (f,)
            w += 1
            
        
        data = dict({'users':users})
        return Response(data=data)
    
    else:
        return HttpResponse("sdsdsads")


# def json_body_decoder(my_func):
#     def inner_func(request, *args, **kwargs):
#         body = request.body.decode("utf-8")
#         request.POST = json.loads(body)
#         return my_func(request, *args, **kwargs)
#     return inner_func

 

@csrf_exempt
@api_view(['GET', 'POST', ])
def reportLoad(request):
    if request.method == 'GET':
        return render(request,'sample.html',{})
    elif(request.method =='POST'):
        # lis =  request.POST
        # data = list(json.loads(request.POST.get('data', '')))
        # data = json.loads(request.data)
        # return JsonResponse({'result':data},safe=False)
        df = list(request.data)
        for i in range(df.__len__()):     
            usrnm = df[i][0]
            usrrepo = df[i][2]
            usr = User_Details.objects.get(username = usrnm)
            for q in usrrepo:
                rep = User_Details.objects.get(username = q)
                dummy = Reporter_Data.objects.filter(report_from=rep,report_to=usr).count()
                if(dummy == 0):
                    srepo = Reporter_Data(report_from=rep,report_to=usr)
                    srepo.save()
        return Response({'received data': usrnm})
    else:
        return HttpResponse("no call")




@csrf_exempt
@api_view(['POST'])
def delete_user(request):
    data = request.data
    session = Session.objects.get(session_key=data.get('user_session_Id'))
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    if userC.is_superuser:
        usrd = User_Details.objects.get(id=data.get('id'))
        useri = User.objects.get(username = usrd.username)
        usrd.delete()
        useri.delete()
        return Response(data={
            'code':'200',
            'body':'user deleted'
        })
    else:
        return Response(data={
            'code':'400',
            'message':'Sorry, Not a super user'
        })



@csrf_exempt
@api_view(['POST'])
def report_to_usr(request):
    data = request.data
    session = Session.objects.get(session_key=data.get('user_session_Id'))
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    if userC.is_superuser:
        # Reporter_Data()
        rp_ter = int(data.get('rp_ter'))
        rp_to = int(data.get('rp_to'))
        usr = User_Details(id=rp_to)
        rp_lst = usr.report_list.all()
        if rp_ter in rp_lst:
            return Response(data={
                'code':'200',
                'message':'already a reporter'
            })
        else:
            rp_ter = User_Details.objects.get(id=rp_ter)
            rp_to = User_Details.objects.get(id=rp_to)
            if Reporter_Data.objects.filter(report_from=rp_ter.id).count() > 0:
                rp_lst = Reporter_Data.objects.filter(report_from=rp_ter.id)
                for l in rp_lst:
                    l.delete()
            rp = Reporter_Data(report_from=rp_ter,report_to=rp_to)
            rp.save()
            return Response(data={
            'code':'200',
            'body':'Successfully added as a reporter'
            })
    else:
         return Response(data={
            'code':'400',
            'message':'Sorry, Not a super user'
        })


@csrf_exempt
@api_view(['POST'])
def roles(request):
    if request.method == 'POST':
        data = request.data
        session = Session.objects.get(session_key=data.get('user_session_Id'))
        uid = session.get_decoded().get('_auth_user_id')
        userC = User.objects.get(pk=uid)
        message=''                              # error message
        body = ''
        role = data.get('role')
        if userC.is_superuser:
            if data.get('job') == 'create':     # Creating the role
                r = Roles(role = role)
                r.save()
                body='successfully created'

            elif data.get('job') == 'update':   # Updating the role
                r = Roles.objects.filter(role=role).count()     #check if the role is present in the db
                if(r == 0):
                    message = 'Role not found'
                else:
                    r = Roles.objects.get(role=role)
                    r.role = data.get('up_role')
                    r.save()
                    body = 'successfully updated'
                    
            elif data.get('job') == 'delete':   #delete the role
                r = Roles.objects.get(role=role)    #check if the role is present in the db
                r.delete()
                body='Successsfully deleted'
            else:                               # list all roles
                r = Roles.objects.all()
                l = []
                for i in r:
                    l.append(model_to_dict(i))
                body = l
            if(message == ''):
                return Response(data={
                    'code':'200',
                    'body':body,
                    'job':data.get('job')
                })
            else:
                return Response(data={
                    'code' : '400',
                    'message': message
                })
        else:
            return Response(data={
                'code':'400',
                'message' : 'Not a  Super User'
            })

# {
#     'user_session_Id':'',
#     'job':'what to do',
#     'crt_updt_data':{
#         'course_name':'',
#         'taxable_fees':",
#         'non_txbl_fees':''
#     },
#   'id':'',
#     'delete_data':'course-name',
# }


@csrf_exempt
@api_view(['POST'])
def courses(request):
    if request.method == 'POST':
        data = request.data
        session = Session.objects.get(session_key=data.get('user_session_Id'))
        uid = session.get_decoded().get('_auth_user_id')
        userC = User.objects.get(pk=uid)
        job = data.get('job')
        if userC.is_superuser:                  # check whether the user is super user or not
            if job == 'create':                 #create data
                dtls = data.get('crt_updt_data')
                course = Courses(
                    course_name = dtls.get('course_name'),
                    taxable_fees = dtls.get('taxable_fees'),
                    non_txbl_fees = dtls.get('non_txbl_fees')
                    )
                course.save()
                return Response(data={
                    'code':'200',
                    'body':'Created successfully'
                })
            elif job == 'update':               #update data
                course = Courses.objects.get(id = data.get('id'))
                dtls = data.get('crt_updt_data')
                if dtls.get('course_name') != '':
                    course.course_name = dtls.get('course_name')
                if dtls.get('taxable_fees') != '':
                    course.taxable_fees = dtls.get('taxable_fees')
                if dtls.get('non_txbl_fees') != '':
                    course.non_txbl_fees = dtls.get('non_txbl_fees')
                course.save()
                return Response(data={
                    'code':'200',
                    'body':'updated successfully'
                })
            elif job == 'delete':               #delete data
                cousre = Courses.objects.get(id = data.get('delete_data'))
                cousre.delete()
                return Response(data={
                    'code':'200',
                    'body':'Successfully deleted'
                })
                             # job == '':  only super user can perfrom these actions
                
                             # read the data
        courses = Courses.objects.all()
        crs_lst = []
        for i in courses:
            crs_lst.append(model_to_dict(i))
        
        return Response(data={
            'code':'200',
            'body':crs_lst
            }) 
        

    else:
        return Response(data={
            'code':'405',
            'messsage':'Only POST is accepted'
        })




 
    # inv.invc_date = ''
    # inv.total_amt = ''
    # invc_id = ''
    # lead = 'ET_INV_BLR_000001'
    # inv.course = ''
    
    # {
    #     'lead':'', # lead id
    #     'invc_date' : '',
    #     'total_amt':'',
    #     'course' : ''  # course id
    # }



@csrf_exempt
@api_view(['POST'])
def invoice(request):
    data = request.data
    session = Session.objects.get(session_key=data.get('user_session_Id'))
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    userD = User_Details.objects.get(username=userC.username)
    for i in data:
        if data.get(i) is '':
            return Response(data = {
                'code':'400',
                'message':'Required all feilds'
            })
    if data.get('job') == 'create':
        inv = Invoice_List()
        inv.lead = Lead_List.objects.get(phone_number=data.get('phone_number'))
        inv.user = userD
        inv_id = str((int(Invoice_List.objects.latest('id').id) + 1))
        inv_id = '0'*(6 - len(inv_id)) + str(inv_id)
        inv_id = 'ET_' + data.get('location') +'_' + inv_id
        inv.invc_id = inv_id
        cur = Courses.objects.get(id = int(data.get('course')))
        inv.course = cur
        inv.total_amt = cur.taxable_fees
        inv.save()
        kijl= ''
        for instls in data.get('instalments'):
            # inst = Installments(
            # pay_date=instls.get('date'),
            # inv_id = inv,
            # pay_amount = instls.get('amount')
            # )
            inst = Installments()
            inst.inv_id = inv
            inst.pay_amount = instls.get('amount')
            inst.pay_date = instls.get('date')
            inst.save()
            kijl = 'khgkjhg'
        inv.save()
        return Response(data={
            'code':'200',
            'body':'Sucesfuly created'
        })
    else:
        ld = Lead_List.objects.get(id = data.get('id'))
        invs = ld.lead_invoice_list.all()
        inv_lst = []
        inv = {}
        for i in invs:
            inv['date'] = i.invc_date
            inv['ttl_amt'] = i.ttl_amt
            inv['course'] = i.course
            inv_lst.append(inv)
        return Response(data={
            'code':'200',
            'body':inv_lst
        })



@csrf_exempt
@api_view(['POST'])
def branches(request):
    if request.method == 'POST':
        data = request.data
        session = Session.objects.get(session_key=data.get('user_session_Id'))
        uid = session.get_decoded().get('_auth_user_id')
        userC = User.objects.get(pk=uid)
        message=''                              # error message
        body = ''
        branch = data.get('branch')
        if userC.is_superuser:
            if data.get('job') == 'create':     # Creating the role
                r = Branch(brnch_name=branch)
                r.save()
                body='successfully created'

            elif data.get('job') == 'update':   # Updating the role
                r = Branch.objects.filter(brnch_name=branch).count()     #check if the role is present in the db
                if(r == 0):
                    message = 'Role not found'
                else:
                    r = Branch.objects.get(brnch_name=branch)
                    r.role = data.get('up_role')
                    r.save()
                    body = 'successfully updated'
                    
            elif data.get('job') == 'delete':   #delete the role
                r = Branch.objects.get(brnch_name=branch)    #check if the role is present in the db
                r.delete()
                body='Successsfully deleted'
            else:                               # list all roles
                r = Branch.objects.all()
                l = []
                for i in r:
                    l.append(model_to_dict(i))
                body = l
            if(message == ''):
                return Response(data={
                    'code':'200',
                    'body':body,
                    'job':data.get('job')
                })
            else:
                return Response(data={
                    'code' : '400',
                    'message': message
                })
        else:
            return Response(data={
                'code':'400',
                'message' : 'Not a  Super User'
            })


@csrf_exempt
@api_view(['POST'])
def bills(request):
    data = request.data
    session = Session.objects.get(session_key=data.get('user_session_Id'))
    uid = session.get_decoded().get('_auth_user_id')
    userC = User.objects.get(pk=uid)
    userD = User_Details.objects.get(username = userC.username)
    inv_id = Invoice_List.objects.get(invc_id = data.get('invoice_id'))
    if int(data.get('amount')) < 1 or (int(inv_id.total_amt) - int(data.get('amount'))) < 0:
        return Response(data={
            'code':'400',
            'message':'bill amount is not valid'
        })
    else:
        #check whether there are any recipts in the DB
        if Bill.objects.all().count() == 0:
            bll_id = str((0 + 1))
            bll_id = '0'*(6 - len(bll_id)) + str(bll_id)
        else:
            bll_id = str((int(Bill.objects.latest('id').id) + 1))
            bll_id = '0'*(6 - len(bll_id)) + str(bll_id)
            bll_id = 'RCT_' + data.get('location') + '_' + bll_id
            if data.get('payment_type') == 'cheque' and (data.get('dated') is '' or data.get('drawn_on') is ''):
                return Response(data={
                    'code':'400',
                    'message':'Require date feilds for cheque payment type'
                })
            else:
                data['dated'] = None
                data['drawn_on'] = None
        bill = Bill(invoice_id = inv_id,
            amount = data.get('amount'),
            user = userD,
            bill_id =  bll_id,
            payment_type = data.get('payment_type'),
            dated = data.get('dated'),
            drawn_on = data.get('drawn_on')
        )
        bill.save()
        return Response(data={
            'code': '200',
            'message':'successfully created the reciept',
            'bill_id':bll_id
        })


@csrf_exempt
@api_view(['POST'])
def inv_view(request):
    data = request.data
    if data.get('user_session_Id') != '':
        inv = Invoice_List.objects.get(invc_id = data.get('invc_id'))
        inv_usr = inv.lead
        billls = inv.invc_bills.all()
        bll_lst = []
        for i in billls:
            bll_lst.append({
                'bill_id': i.bill_id,
                'paid':i.amount,
                'date':i.paid_date
            })

        resp ={
            'address':inv_usr.address,
            'dob':inv_usr.dob,
            'invoice_id':inv.invc_id,
            'bills':bll_lst
        }
        return Response(data={
            'body':resp,
            'code':'200'
        })
    else:
        return Response(data={
            'code':'200',
            'message':'please login'
        })


@csrf_exempt
@api_view(['POST'])
def bill_view(request):
    data = request.data
    if data.get('user_session_Id') != '':
        bill = Bill.objects.get(bill_id = data.get('bill_id'))
        invoice = Invoice_List.objects.get(id = bill.invoice_id.id)
        lead = Lead_List.objects.get(id = invoice.lead.id)
        course = Courses.objects.get(id = invoice.course.id)
        ttl_paid_bills = invoice.invc_bills.all()
        ttl_amt = 0
        for i in ttl_paid_bills:
            ttl_amt = ttl_amt + int(i.amount)
        bln_amt = int(course.taxable_fees) -  ttl_amt 
        #due date variable
        dt_lst = invoice.instlmnts_lst.all()
        # due_dte = dt_lst[0]
        due_dte = 0



        for hj in dt_lst:
            if hj.paid is False:
                due_dte = hj.pay_date
                break



        dtls = {
            'std_nm':lead.name,
            'course':course.course_name,
            'total_fees':course.taxable_fees,
            'pay_type':bill.payment_type,
            'dated' : bill.dated,
            'drawn_on':bill.drawn_on,
            'amt_rcvd':bill.amount,
            'blnc_amt' : bln_amt,
            'due_date':due_dte,
            'bill_date':bill.paid_date,
        }
        return Response(data={
            'code':'200',
            'body':dtls
        })
    else:
        return Response(data={
            'code':'400',
            'message':'Please login'
        })







        
            















