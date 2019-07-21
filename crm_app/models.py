from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.sessions.models import Session
 

# Create your models here.


class User_Details(models.Model):
    username = models.CharField(max_length = 20)
    designation = models.CharField(max_length = 40)


    def __str__(self):
        return self.username


class Reporter_Data(models.Model):
    report_from = models.ForeignKey(User_Details,on_delete=models.CASCADE)
    report_to = models.ForeignKey(User_Details,related_name='report_list',on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}\n".format(self.report_from, self.report_to)
        # return "$'reportedFrom':'{0}','reportedTo':'{1}'$".format(self.report_from,self.report_to)

class Lead_List(models.Model):
    name = models.CharField(max_length = 30)
    phone_number = models.CharField(max_length = 10,unique=True)
    email = models.EmailField()
    address = models.CharField(max_length = 300)
    nxt_flw_dt = models.DateTimeField(blank=True)
    dob = models.DateField(blank=True,default=None)
    user_fllwng = models.ForeignKey(User_Details,on_delete=models.CASCADE,related_name='lead_list_data')
    status = models.CharField(max_length = 10)
    created_dt = models.DateTimeField(auto_now=True)
    campaign = models.CharField(max_length=30,default='online website')
    enquired_for = models.CharField(max_length = 200,default='Internship')
    degree = models.CharField(max_length = 100,default='B.E')
    yop = models.DateTimeField(blank=True)
    marks = models.CharField(max_length=10,default='0')
    brnch_loc = models.CharField(max_length=20,default='')
    tchngly_lk_fr = models.CharField(max_length=300,default='')


    def __str__(self):
        return self.name
        # return "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(self.name,self.phone_number,
        # self.email,self.address,self.nxt_flw_dt,self.dob,self.user_fllwng,
        # self.status,self.created_dt,self.campaign,self.enquired_for,self.degree,
        # self.yop,self.marks,self.brnch_loc,self.tchngly_lk_fr)

class Followed_History(models.Model):
    date = models.DateField(blank=False)
    lead_id = models.ForeignKey(Lead_List,on_delete=models.CASCADE,related_name='lead_history')
    status = models.CharField(max_length=10)
    reason = models.CharField(max_length=100)
    user = models.ForeignKey(User_Details,on_delete=models.CASCADE,related_name='user_follwup_list')

    def __str__(self):
        return "{} {} {} {} {}\n".format(self.date,self.lead_id,self.status,self.reason,self.user)



class Courses(models.Model):
    course_name = models.CharField(max_length=40)
    taxable_fees = models.CharField(max_length=10,blank=False)
    non_txbl_fees = models.CharField(max_length=10,blank=False)

    def __str__(self):
        return self.course_name





class Invoice_List(models.Model):
    lead = models.ForeignKey(Lead_List,on_delete=models.CASCADE,related_name='lead_invoice_list')
    total_amt = models.CharField(max_length=10,blank=False)
    invc_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User_Details,on_delete=models.CASCADE,related_name='user_invoice_list')
    invc_id = models.CharField(max_length = 20,unique=True)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,related_name='course_inc')

    def __str__(self):
        return "{} {} {} {} {} n".format(self.lead,self.total_amt,self.invc_date,self.user,self.invc_id)
        #ET_INV_BLR_0000010



class Installments(models.Model):
    pay_date=models.DateField()
    pay_amount = models.CharField(max_length=15,blank=False)
    inv_id = models.ForeignKey(Invoice_List,on_delete=models.CASCADE,related_name='instlmnts_lst')
    paid = models.BooleanField(default=False)
    def __str__(self):
        return self.pay_date



class Roles(models.Model):
    role = models.CharField(max_length=40,unique=True)

    def __str__(self):
        return self.role
     
# class Lead_Follow_Table(models.Model):
#     lead_id = models.ForeignKey(Lead_List,on_delete=models.CASCADE,related_name='lead_asign_flow')
#     user_id = models.ForeignKey(User_Details,on_delete=models.CASCADE,related_name='user_lead_assign_flow')

#     def __str__(self):
#         return "{} {}\n".format(self.lead_id,self.user_id)


class Branch(models.Model):
    brnch_name = models.CharField(max_length = 30)

    def  __str__(self):
        return self.brnch_name
        

# class Bills(models.Model):
#     invoice_id = models.ForeignKey(Invoice_List,on_delete=models.CASCADE,related_name='invc_bills')
#     amount = models.CharField(max_length = 50,blank = True)
#     paid_date = models.DateTimeField(auto_now=True)
#     user = models.ForeignKey(User_Details,on_delete=models.CASCADE,related_name='user_billed')
#     bill_id = models.CharField(max_length=100,default='')
#     payment_type = models.CharField(max_length = 40,default='CASH')
#     dated = models.DateField(auto_now=True)
#     drawn_on = models.DateField(auto_now=True)

#     def __str__(self):
#         return self.amount

class Bill(models.Model):
    invoice_id = models.ForeignKey(Invoice_List,on_delete=models.CASCADE,related_name='invc_bills')
    amount = models.CharField(max_length = 50,blank = True)
    paid_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User_Details,on_delete=models.CASCADE,related_name='user_billed')
    bill_id = models.CharField(max_length=100,default='')
    payment_type = models.CharField(max_length = 40,blank=False)
    dated = models.DateField(blank = True)
    drawn_on = models.DateField(blank = True)
    

    def __str__(self):
        return self.amount






