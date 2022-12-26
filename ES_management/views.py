from django.shortcuts import render, redirect
from .models import Site, Department, Duration, Equipment
from Rental.models import Rent_Equipment
from .forms import AddSiteModelForm, UpdateSiteForm, AddEquModelForm, UpdateEquForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import datetime

#場材管理員首頁
@csrf_exempt
def home_page(request):
    return render(request, 'home-se.html')

#回首頁
@csrf_exempt
def back_to_home_page(request):
    return redirect('/es_management/home_page/')

#場地管理
@csrf_exempt
def site_management(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        context = {}
        #根據 email 查詢負責管理的場地
        se_manager_email = request.session.get("email")
    
        result = Site.objects.filter(
            department_id__email = se_manager_email #在 Site Table 抓該 Email 管理的場地 id 
        ).order_by('usage')
    
        return_data = result.values('id','name', 'usage', 'price', 'rule', 'image', 'address', 'location') #取要回傳回去的值

        #檢查
        if len(list(return_data)) == 0:
            context['site_set'] = False
        else:
            context['site_set'] = list(return_data)

        return render(request, 'site_management.html',context)

#新增場地
@csrf_exempt
def add_site(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        form = AddSiteModelForm()
        se_manager_email = request.session.get("email")

        form.initial['department_id'] = Department.objects.get(email=se_manager_email).id
        form = AddSiteModelForm(initial={'department_id': form.initial['department_id']}) #設初值
        
        if request.method == "POST":
            form = AddSiteModelForm(request.POST, request.FILES)
            rule = request.POST['rule']
            price = request.POST['price']
            address = request.POST['address']
            name = request.POST['name']
            department_id = Department.objects.get(email=se_manager_email).id
            if form.is_valid():  
                if(Site.objects.filter(name = name, department_id = department_id).exists()): 
                    messages.error(request,"重複場地名稱，請重新輸入")
                    return HttpResponseRedirect(request.path_info)
                elif(address!=("桃園市中壢區中大路300號")and address!=("新竹市東區光復路二段101號") and address!=("新竹市東區大學路1001號")and address!=("臺北市文山區指南路二段64號")):  
                    messages.error(request,"場地地址需要輸入學校地址")    
                    return HttpResponseRedirect(request.path_info)   
                elif(len(rule)<20):   
                    messages.error(request,"場地租借規則需要至少20字!")    
                    return HttpResponseRedirect(request.path_info)  
                elif(name==None):
                     return site_management(request)
                else:                   
                    name = form.cleaned_data['name']
                    form.save()
                    ##
                    start = int(request.POST["start"])
                    end = int(request.POST["end"])

                    for i in range(1,8):

                        date = datetime.date.today()+ datetime.timedelta(days=i)
                        for i in range(start,end):  #(8,11)
                            start_time = i
                            end_time = i+1
                            print(date,start_time,end_time)
                            Duration.objects.create(
                                date=date,
                                start=start_time,
                                end=end_time,
                                rent_status=0,
                                site_id=Site.objects.get(name = name, department_id = Department.objects.get(email=se_manager_email).id
                            )
                        )

                        return site_management(request)
            else:              
                messages.error(request,"新增錯誤")
                return HttpResponseRedirect(request.path_info)
        
        return render(request, 'add_site.html', {'form': form})




#顯示修改場地頁面
@csrf_exempt
def display_edit_site(request):
    if request.method == "POST":
        form = UpdateSiteForm()
        site_id = request.POST.get('id')
        request.session['site_id'] = site_id
    return render(request, 'edit_site.html', {'form': form})


#修改場地
@csrf_exempt
def edit_site(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        context = {}
        form = UpdateSiteForm()

        if request.method == "POST":
            form = UpdateSiteForm(request.POST ,request.FILES)
            rule = request.POST['rule']
            address = request.POST['address']
            
            print(form)
            if form.is_valid():
                if(address!=("桃園市中壢區中大路300號")and address!=("新竹市東區光復路二段101號") and address!=("新竹市東區大學路1001號")and address!=("臺北市文山區指南路二段64號")):  
                    messages.error(request,"場地地址需要輸入學校地址")    
                    return HttpResponseRedirect(request.path_info)    
                elif(len(rule)<20):   
                    messages.error(request,"場地租借規則需要至少20字!")    
                    return HttpResponseRedirect(request.path_info)  
                elif('site_id' not in request.session):
                    return site_management(request) 
                else:
                    id = request.session['site_id']
                    keyitem = Site.objects.get(id=id) 
                    form = UpdateSiteForm(request.POST, request.FILES,instance=keyitem)

                    form.instance.department_id = Site.objects.get(id=id).department_id
                    form.save() 
                    del request.session['site_id']
                    return site_management(request)
            else:
                messages.error(request, "修改失敗")
                return HttpResponseRedirect(request.path_info)

        context['form']=form
        return render(request, 'edit_site.html', context)

#刪除場地 
@csrf_exempt
def delete_site(request):

    if request.method == "POST":
        site_id = request.POST.get('id')
        data = Site.objects.get(id=site_id) 

        if Duration.objects.filter(site_id=site_id,rent_status=1):
            messages.error(request, "該場地正被租借中，不可被刪除")
            return site_management(request)
        else:
            data.delete()   
            return site_management(request)



#器材管理
@csrf_exempt
def equipment_management(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        context = {}
        #根據 email 查詢負責管理的器材
        se_manager_email = request.session.get("email")

        result = Equipment.objects.filter(
            department_id__email = se_manager_email  #在 Equipment Table 抓該 Email 管理的器材 id 
        )

        return_data = result.values('id','name','price','number','image', 'usage', 'rule') #取要回傳回去的值

        #檢查
        if len(list(return_data)) == 0:
            context['equ_set'] = False
        else:
            context['equ_set'] = list(return_data)

        return render(request, 'equipment_management.html',context)

#新增器材
@csrf_exempt
def add_equipment(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        form = AddEquModelForm()
        se_manager_email = request.session.get("email")

        form.initial['department_id'] = Department.objects.get(email=se_manager_email).id
        form = AddEquModelForm(initial={'department_id': form.initial['department_id']})
        # context = {}
        if request.method == "POST":
            form = AddEquModelForm(request.POST, request.FILES)
            rule = request.POST['rule']
            name = request.POST['name']
            department_id = Department.objects.get(email=se_manager_email).id
            if form.is_valid():  
                if(Equipment.objects.filter(name = name, department_id = department_id).exists()): 
                    messages.error(request,"重複器材名稱，請重新輸入")
                    return HttpResponseRedirect(request.path_info)           
                elif(len(rule)<20):   
                    messages.error(request,"場地租借規則需要至少20字!")    
                    return HttpResponseRedirect(request.path_info)   
                else:         
                #messages.success(request,"新增成功")
                    form.save()
                    return equipment_management(request)
            else:  
                form = AddEquModelForm()              
                messages.success(request,"新增錯誤")
        
        return render(request, 'add_equipment.html', {'form': form})

#顯示修改器材頁面
@csrf_exempt
def display_edit_equipment(request):
    if request.method == "POST":
        form = UpdateEquForm()
        equipment_id = request.POST.get('id')
        request.session['equipment_id'] = equipment_id
    return render(request, 'edit_equipment.html', {'form': form})

#修改器材
@csrf_exempt
def edit_equipment(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        content={}
        form = UpdateEquForm()

        if request.method == "POST":
            form = UpdateEquForm(request.POST, request.FILES)
            rule = request.POST['rule']
            if form.is_valid():    
                if(len(rule)<20):   
                    messages.error(request,"場地租借規則需要至少20字!")    
                    return HttpResponseRedirect(request.path_info)   
                elif('equipment_id' not in request.session):
                    return equipment_management(request)
                else:
                    equipment_id = request.session['equipment_id']
                    keyitem = Equipment.objects.get(id=equipment_id) 
                    form = UpdateEquForm(request.POST, request.FILES,instance=keyitem)
                    form.instance.department_id = Equipment.objects.get(id=equipment_id).department_id 
                    form.save()
                    del request.session['equipment_id']
                return equipment_management(request)

            else:
                messages.error(request, "修改失敗")
                return HttpResponseRedirect(request.path_info)
        content['form'] = form 
        return render(request, 'edit_equipment.html',content)


#刪除器材
@csrf_exempt
def delete_equipment(request):

    if request.method == "POST":

        id = request.POST.get('id')
        data = Equipment.objects.get(id=id)
        data_id = Equipment.objects.get(id=id).id

        if Rent_Equipment.objects.filter(equipment_id=data_id) & Rent_Equipment.objects.filter( status = 1):
            messages.error(request, "該器材正被租借中，不可被刪除")
            return equipment_management(request)
        else:
            data.delete()       
            return equipment_management(request)
