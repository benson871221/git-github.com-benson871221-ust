from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from ES_management.models import Equipment, Site
from Member.models import Member
from Rental.models import Rent_Equipment, Rent_Site
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

#顯示預約審核頁面
@csrf_exempt
def display_order_management(request):
    return render(request, 'ES_order_management.html')

# 場材管理員場地收款後，更新 Rent_Site 訂單狀態為 1
@csrf_exempt
def status_update_site(request): 

    if request.method == "POST":

        data = request.POST
        rent_site_id = data.get('id')
        Rent_Site.objects.filter(id=rent_site_id).update(status=1)
        return HttpResponseRedirect(reverse('Order_management:generate_rental2'))
    #return JsonResponse(data={'msg':'update object success.'})
    return render(request, 'ES_order_management.html')


# 確定租借器材付款(狀態更新為1)
@csrf_exempt
def status_update_equ(request):

    if request.method == "POST":

        data = request.POST
        rent_equ_id = data.get('id')
        Rent_Equipment.objects.filter(id=rent_equ_id).update(status='1')
        return HttpResponseRedirect(reverse('Order_management:generate_rental2'))

    #return JsonResponse(data={'msg':'update object success.'},status=200)
    return render(request, 'ES_order_management.html')

# 確定歸還器材(狀態更新為2)
@csrf_exempt
def status_return_equ(request):

    if request.method == "POST":
        data = request.POST
        rent_equ_id = data.get('id') #訂單id

        # equ_number = Rent_Equipment.objects.get(id=rent_equ_id).number #要加回去的數量
        # equ_id = Rent_Equipment.objects.get(id=rent_equ_id).equipment_id.id #哪個器材
        # old_number = Equipment.objects.get(id=equ_id).number #器材原始數量
        Rent_Equipment.objects.filter(id=rent_equ_id).update(status='2') #狀態修改成2(歸還)
        # Equipment.objects.filter(id=equ_id).update(number=old_number+equ_number) #加上歸還數量
        return HttpResponseRedirect(reverse('Order_management:generate_rental2'))

    #return JsonResponse(data={'msg':'update object success.'},status=200)
    return render(request, 'ES_order_management.html')

#----------------------------------------------

#整合顯示
@csrf_exempt
def generate_rental(request):

    context = {}
    #search_email = "howard11633@gmail.com"
    data = request.POST
    search_email = data.get('email')
    request.session['search_rent_email'] = search_email

    session_email = request.session['search_rent_email']

    if Member.objects.filter(email=search_email).exists():
        if search_email != session_email:
            del request.session['search_rent_email']
            request.session['search_rent_email'] = search_email

        #--------------器材--------------

        result_equ_0 = Rent_Equipment.objects.filter(
            member_id__email = search_email,
        ) & Rent_Equipment.objects.filter( status = 0)

        getdata_value_equ_0 = list(result_equ_0.values_list('id','date','number','equipment_id','status')) 
        return_data_list_equ_0 = []

        result_equ_1 = Rent_Equipment.objects.filter(
            member_id__email = search_email,
        ) & Rent_Equipment.objects.filter( status = 1)

        getdata_value_equ_1 = list(result_equ_1.values_list('id','date','number','equipment_id','status')) 
        return_data_list_equ_1 = []

        member_id = Member.objects.get(email = search_email).id 
        
        return_data_list_site = []
        result_site = Rent_Site.objects.filter(member_id__email = search_email) & Rent_Site.objects.filter(status = 0)#用member的email和狀態為0的訂單做篩選
        
        for i in range(len(result_equ_0)): #去抓每筆訂單的相關資料
            rent_id = getdata_value_equ_0[i][0] #租借ID
            rent_date = getdata_value_equ_0[i][1] #租借日期
            equipment_number = getdata_value_equ_0[i][2] #抓租借數量
            equipment_id = getdata_value_equ_0[i][3] #抓器材ID
            status = getdata_value_equ_0[i][4] #抓器材ID

            equipment_item_data = Equipment.objects.get(id=equipment_id) 
            return_name= equipment_item_data.name #抓器材名字
            return_price=equipment_item_data.price #抓器材價格
            total_price=int(equipment_number)*int(return_price) #租借總金額（數量乘價格）
            equ_school_name = equipment_item_data.department_id.school_id.name #器材所屬的學校名字
            
            #回傳的東東
            return_data = {'id':rent_id,'date':rent_date,'school':equ_school_name,'name':return_name,'number':equipment_number,'price':total_price,'status':status}
            return_data_list_equ_0 += [return_data]
        
        for i in range(len(result_equ_1)): #去抓每筆訂單的相關資料
            rent_id = getdata_value_equ_1[i][0] #租借ID
            rent_date = getdata_value_equ_1[i][1] #租借日期
            equipment_number = getdata_value_equ_1[i][2] #抓租借數量
            equipment_id = getdata_value_equ_1[i][3] #抓器材ID
            status = getdata_value_equ_1[i][4] #抓器材ID

            equipment_item_data = Equipment.objects.get(id=equipment_id) 
            return_name= equipment_item_data.name #抓器材名字
            return_price=equipment_item_data.price #抓器材價格
            total_price=int(equipment_number)*int(return_price) #租借總金額（數量乘價格）
            equ_school_name = equipment_item_data.department_id.school_id.name #器材所屬的學校名字
            
            #回傳的東東
            return_data = {'id':rent_id,'date':rent_date,'school':equ_school_name,'name':return_name,'number':equipment_number,'price':total_price,'status':status}
            return_data_list_equ_1 += [return_data]
            
        #場地
        for i in range(0, len(result_site)): #for迴圈長度為所有結果的長度、用rent_site_count來跳到下一筆租借場地的資料
            rent_id = result_site[i].id
            site_name = result_site[i].duration_id.site_id.name #用Rent_site接到外來鍵來取場地名字
            school_name = result_site[i].duration_id.site_id.department_id.school_id.name #用Rent_site接到外來鍵來取學校名字
            date = result_site[i].date #取日期
            date_start = result_site[i].duration_id.start #到Duration去取開始的時間
            timestamp = result_site[i].timestamp
            rent_site_count = Rent_Site.objects.filter(timestamp = timestamp).count() #用timestamp來抓筆數(EX: 三筆就是租三個小時) 同時也是用來當for迴圈的參數去跳到下一筆的租借資料
            date_end = result_site[i].duration_id.end #開始時間 + 抓到的筆數 = 結束時間
            total_price = Site.objects.get(name = site_name).price #去Site抓一小時的價格 * 這次租借資料的筆數

            return_data2 = {
                'id': rent_id,
                'site_name': site_name,
                'date': date,
                'start': date_start,
                'end': date_end,
                'school_name': school_name,
                'total_price': total_price
            }
            return_data_list_site += [return_data2]

        #檢查有無紀錄
        if not return_data_list_site:
            context['rental_site_set'] = False
        else:
            context['rental_site_set'] = return_data_list_site  

        if not return_data_list_equ_0:
            context['rental_equ_set_0'] = False
        else:
            context['rental_equ_set_0'] = return_data_list_equ_0 

        if not return_data_list_equ_1:
            context['rental_equ_set_1'] = False
        else:
            context['rental_equ_set_1'] = return_data_list_equ_1 

        return render(request, 'ES_order_management.html', context)
    
    else:
        messages.error(request, "查無此人")
        return render(request, 'ES_order_management.html')

    

#整合顯示
@csrf_exempt
def generate_rental2(request):

    context = {}
    search_email = request.session['search_rent_email']
    #--------------器材--------------

    result_equ_0 = Rent_Equipment.objects.filter(
        member_id__email = search_email,
    ) & Rent_Equipment.objects.filter( status = 0)

    getdata_value_equ_0 = list(result_equ_0.values_list('id','date','number','equipment_id','status')) 
    return_data_list_equ_0 = []

    result_equ_1 = Rent_Equipment.objects.filter(
        member_id__email = search_email,
    ) & Rent_Equipment.objects.filter( status = 1)

    getdata_value_equ_1 = list(result_equ_1.values_list('id','date','number','equipment_id','status')) 
    return_data_list_equ_1 = []

    member_id = Member.objects.get(email = search_email).id 
    
    return_data_list_site = []
    result_site = Rent_Site.objects.filter(member_id__email = search_email) & Rent_Site.objects.filter(status = 0)#用member的email和狀態為0的訂單做篩選
    
    for i in range(len(result_equ_0)): #去抓每筆訂單的相關資料
        rent_id = getdata_value_equ_0[i][0] #租借ID
        rent_date = getdata_value_equ_0[i][1] #租借日期
        equipment_number = getdata_value_equ_0[i][2] #抓租借數量
        equipment_id = getdata_value_equ_0[i][3] #抓器材ID
        status = getdata_value_equ_0[i][4] #抓器材ID

        equipment_item_data = Equipment.objects.get(id=equipment_id) 
        return_name= equipment_item_data.name #抓器材名字
        return_price=equipment_item_data.price #抓器材價格
        total_price=int(equipment_number)*int(return_price) #租借總金額（數量乘價格）
        equ_school_name = equipment_item_data.department_id.school_id.name #器材所屬的學校名字
        
        #回傳的東東
        return_data = {'id':rent_id,'date':rent_date,'school':equ_school_name,'name':return_name,'number':equipment_number,'price':total_price,'status':status}
        return_data_list_equ_0 += [return_data]
    
    for i in range(len(result_equ_1)): #去抓每筆訂單的相關資料
        rent_id = getdata_value_equ_1[i][0] #租借ID
        rent_date = getdata_value_equ_1[i][1] #租借日期
        equipment_number = getdata_value_equ_1[i][2] #抓租借數量
        equipment_id = getdata_value_equ_1[i][3] #抓器材ID
        status = getdata_value_equ_1[i][4] #抓器材ID

        equipment_item_data = Equipment.objects.get(id=equipment_id) 
        return_name= equipment_item_data.name #抓器材名字
        return_price=equipment_item_data.price #抓器材價格
        total_price=int(equipment_number)*int(return_price) #租借總金額（數量乘價格）
        equ_school_name = equipment_item_data.department_id.school_id.name #器材所屬的學校名字
        
        #回傳的東東
        return_data = {'id':rent_id,'date':rent_date,'school':equ_school_name,'name':return_name,'number':equipment_number,'price':total_price,'status':status}
        return_data_list_equ_1 += [return_data]
        
    #場地
    for i in range(0, len(result_site)): #for迴圈長度為所有結果的長度、用rent_site_count來跳到下一筆租借場地的資料
        rent_id = result_site[i].id
        site_name = result_site[i].duration_id.site_id.name #用Rent_site接到外來鍵來取場地名字
        school_name = result_site[i].duration_id.site_id.department_id.school_id.name #用Rent_site接到外來鍵來取學校名字
        date = result_site[i].date #取日期
        date_start = result_site[i].duration_id.start #到Duration去取開始的時間
        timestamp = result_site[i].timestamp
        rent_site_count = Rent_Site.objects.filter(timestamp = timestamp).count() #用timestamp來抓筆數(EX: 三筆就是租三個小時) 同時也是用來當for迴圈的參數去跳到下一筆的租借資料
        date_end = result_site[i].duration_id.end #開始時間 + 抓到的筆數 = 結束時間
        total_price = Site.objects.get(name = site_name).price #去Site抓一小時的價格 * 這次租借資料的筆數

        return_data2 = {
            'id': rent_id,
            'site_name': site_name,
            'date': date,
            'start': date_start,
            'end': date_end,
            'school_name': school_name,
            'total_price': total_price
        }
        return_data_list_site += [return_data2]

    context["rental_site_set"] = return_data_list_site
    context["rental_equ_set_0"] = return_data_list_equ_0
    context["rental_equ_set_1"] = return_data_list_equ_1

    return render(request, 'ES_order_management.html', context)