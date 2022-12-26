from django.shortcuts import render, redirect
from Rental.models import Duration, Rent_Site, Rent_Equipment, Equipment
from Member.models import Member
from django.db.models import IntegerField, ExpressionWrapper, F, Q, Sum
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime


#首頁
@csrf_exempt
def home_page(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        return render(request, "home-nu.html")

#回搜尋場地
@csrf_exempt
def back_to_search_site(request):
    if request.method == "POST":
        return redirect('/rental/search_site/')

#回搜尋器材
@csrf_exempt
def back_to_search_equipment(request):
    if request.method == "POST":
        return redirect('/rental/search_equipment/')

#搜尋場地
@csrf_exempt
def search_site(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        if 'rent_site_turn_page' in request.session:
            del request.session['rent_site_turn_page']
        
        context = {}

        if request.method == "POST":
            school = request.POST['school']
            usage = request.POST['usage']
            date = request.POST['date']
            start = int(request.POST['start'])
            end = int(request.POST['end'])

            end_first = start+1
            start_last =end-1

            result = Duration.objects.filter(
            site_id__department_id__school_id = school,
                    site_id__usage = usage,
                    date = date,
                    rent_status = 0,
                    start__gte = start,
                    start__lte = start_last,
                    end__gte = end_first,
                    end__lte = end
                )

            context["condition_query_set"] = result
            return render(request, "search_site.html", context)

        return render(request, "search_site.html")
 
#顯示欲預約場地
@csrf_exempt
def display_reserve_site(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        context={}
        if request.method == "POST":
            id = request.POST['reserve_site_duration_id']
            result = Duration.objects.filter(id = id)
            context["reserve_site_duration"] = result
            
            #呼叫完reserve_site後
            if 'rent_site_turn_page' in request.session:
                turn_page = request.session.get('rent_site_turn_page')
                if( turn_page == 1):
                    context["successful_submit"] = True
            
            return render(request, "rent_site.html", context)


#確定預約場地
@csrf_exempt
def reserve_site(request):

    if request.method == "POST":

        #檢查是否場地已被預約
        id = request.POST['reserve_site_duration_id']
        result = Duration.objects.filter(id = id).values('rent_status')
        rent_status = result[0]['rent_status']

        if rent_status == 1:
            messages.error(request, "你慢了一步! 該場地已被其他使用者預約!")
            request.session['rent_site_turn_page'] = 0
            return display_reserve_site(request)
        else:
            request.session['rent_site_turn_page'] = 1
            #確定預約場地
            date = datetime.date.today()  # Returns YYYY-MM-DD
            status = 0 #未付款狀態
            timestamp = datetime.datetime.now() # Returns YYYY-MM-DD HH:MM
            member_id = request.session.get('id')
            
            Rent_Site.objects.create(  #Rent_site資料庫新增一筆資料
                date=date,
                status=status,
                timestamp=timestamp,
                member_id=Member.objects.get(id = member_id),
                duration_id=Duration.objects.get(id = id),
            )
            
            #duration table 改租借狀態
            Duration.objects.filter(id=id).update(rent_status=1)

            messages.success(request, "預約場地成功! 請盡速至繳費地點繳費，否則將取消場地預約")
            return display_reserve_site(request)


#搜尋器材
@csrf_exempt
def search_equipment(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        #補session

        context = {}

        if request.method == "POST":
            if 'search_equipment_date' in request.session:
                del request.session['search_equipment_date']
            if 'search_equipment_number' in request.session:
                del request.session['search_equipment_number']
            if 'rent_equipment_turn_page' in request.session:
                del request.session['rent_equipment_turn_page']
            
            school = request.POST['school']
            usage = request.POST['usage']
            date = request.POST['date']
            
            #date存入session用於display_reserve_equipment, reserve_equipment
            request.session['search_equipment_date'] = date
            
            #依學校、用途、日期搜尋可預約器材
            result = Rent_Equipment.objects.select_related('Equipment').values(
                'equipment_id__id',
                'equipment_id__name',
                'equipment_id__usage',
                'equipment_id__price',
                'equipment_id__rule',
                'equipment_id__image',
                'equipment_id__department_id__address'
                ).filter(
                    Q(date=date,status=0)|Q(date=date,status=1),
                    equipment_id__usage = usage,
                    equipment_id__department_id__school_id = school,
                ).annotate(
                    equ_remaining_number = ExpressionWrapper( F('equipment_id__number') - Sum('number', output_field=IntegerField()), output_field=IntegerField())
                ).filter(
                    ~Q(equ_remaining_number=0)
                )

            #當天有使用者租借的所有器材id
            list=[]
            for equipment_id in result:
                list.append(equipment_id['equipment_id__id'])
            
            #當天沒有任何使用者租借的所有器材id
            not_rented_equipment = Equipment.objects.filter(
                    usage = usage,
                    department_id__school_id = school,
                ).exclude(id__in=list)

            context["condition_query_set"] = result
            context["not_rented_equipment"] = not_rented_equipment
            return render(request, "search_equipment.html", context)

        return render(request, "search_equipment.html")

 
#顯示欲預約器材
@csrf_exempt
def display_reserve_equipment(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        context={}
        if request.method == "POST":
            id = request.POST['reserve_equipment_id']
            result = Equipment.objects.filter(id = id)
            number = request.POST.get('number', False)
            
            #呼叫完reserve_equipment後
            if 'rent_equipment_turn_page' in request.session:
                turn_page = request.session.get('rent_equipment_turn_page')
                if( turn_page == 1):
                    context["successful_submit"] = True
                    number=request.session.get('search_equipment_number')
            else:
                #數量存入session用於reserve_equipment
                request.session['search_equipment_number'] = number
            
            #計算租借器材價錢
            total_price = int(number) * int(result[0].price)


            context["reserve_equipment"] = result
            context["total_price"] = total_price
            context["search_equipment_date"] = request.session.get('search_equipment_date')
            
            
            return render(request, "rent_equipment.html", context)
        
        return render(request, "rent_equipment.html")

#確定預約器材
@csrf_exempt
def reserve_equipment(request):

    if request.method == "POST":

        equipment_id = request.POST['reserve_equipment_id']
        date = request.session.get('search_equipment_date')
        #檢查是否器材已被預約
        #查詢當日該器材剩餘數量
        current_equ_remaining_number = Rent_Equipment.objects.values('date').filter(
            ~Q(status=2),
            date=date,
            equipment_id = equipment_id
        ).annotate(
            equ_remaining_number = Sum('number', output_field=IntegerField())
        )

        #當天有使用者租借的所有器材id
        #檢查當日該器材沒有被任何人租借
        if not current_equ_remaining_number:
            current_equ_remaining_number=0
        else:
            current_equ_remaining_number=int(current_equ_remaining_number[0]['equ_remaining_number'])
        
        #查詢該器材數量上限
        equ_limit_number = Equipment.objects.values('number').filter(id=equipment_id)


        if current_equ_remaining_number >= int(equ_limit_number[0]['number']):
            messages.error(request, "你慢了一步! 該器材已無剩下數量可被預約!")
            request.session['rent_equipment_turn_page'] = 0
            return display_reserve_equipment(request)
        else:
            request.session['rent_equipment_turn_page'] = 1

            #確定預約器材
            number = request.session.get('search_equipment_number') #預約數量
            status = 0 #未付款狀態
            timestamp = datetime.datetime.now() # Returns YYYY-MM-DD HH:MM
            member_id = request.session.get('id')
            
            Rent_Equipment.objects.create(  #Rent_site資料庫新增一筆資料
                date=date,
                number=number,
                status=status,
                timestamp=timestamp,
                member_id=Member.objects.get(id = member_id),
                equipment_id=Equipment.objects.get(id = equipment_id),
            )

            messages.success(request, "預約器材成功! 請盡速至繳費地點繳費，否則將取消器材預約")
            return display_reserve_equipment(request)


#目前租借紀錄
@csrf_exempt
def current_rental_record(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        member_id = request.session.get('id')
        #當天日期與後7天
        date = datetime.date.today()  # Returns YYYY-MM-DD
        date_7daysAfter = datetime.date.today() + datetime.timedelta(days=7)
        
        member_rent_site = Rent_Site.objects.filter(
                    member_id = member_id,
                    date__range=[date, date_7daysAfter]
                ).order_by('date')

        member_rent_equipment = Rent_Equipment.objects.filter(
                    member_id = member_id,
                    date__range=[date, date_7daysAfter]
                ).order_by('date')
        
        context={}
        
        #檢查使用者有無場地/器材預約紀錄
        if not member_rent_site:
            context['member_rent_site'] = False
        else:
            context['member_rent_site'] = member_rent_site
        
        if not member_rent_equipment:
            context['member_rent_equipment'] = False
        else:
            context['member_rent_equipment'] = member_rent_equipment


        return render(request, "current_rental_record.html", context)

#刪除場地預約
@csrf_exempt
def delete_reserve_site(request):
    
    if request.method == "POST":
        
        rent_site_id = request.POST.get('reserve_site_id', False)
        #避免重整頁面發生Bug
        if(rent_site_id == False):
            return current_rental_record(request)
        
        #rent_site的duration_id
        rent_site_duration_id = Rent_Site.objects.values('duration_id').filter(id = rent_site_id)
        #duration修改status=0
        Duration.objects.filter(id = rent_site_duration_id[0]['duration_id']).update(rent_status = 0)
        #rent_site刪整筆預約場地紀錄
        rent_site_record = Rent_Site.objects.filter(id = rent_site_id)
        rent_site_record.delete()

        return current_rental_record(request)

#刪除器材預約
@csrf_exempt
def delete_reserve_equipment(request):
    
    if request.method == "POST":
        
        rent_equipment_id = request.POST.get('reserve_equipment_id', False)
        #避免重整頁面發生Bug
        if(rent_equipment_id == False):
            return current_rental_record(request)
        
        #rent_equipment刪整筆預約場地紀錄
        rent_equipment_record = Rent_Equipment.objects.filter(id = rent_equipment_id)
        rent_equipment_record.delete()
        
    return current_rental_record(request)

#歷史租借紀錄
@csrf_exempt
def historical_rental_record(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        member_id = request.session.get('id')
        #當天日期與前31天
        date = datetime.date.today() - datetime.timedelta(days=1) # Returns YYYY-MM-DD
        date_31daysBefore = datetime.date.today() - datetime.timedelta(days=31)
        
        member_rent_site = Rent_Site.objects.filter(
                    member_id = member_id,
                    status = 1,
                    date__range=[date_31daysBefore, date]
                ).order_by('date')

        member_rent_equipment = Rent_Equipment.objects.filter(
                    member_id = member_id,
                    status = 2,
                    date__range=[date_31daysBefore, date]
                ).order_by('date')
        
        context={}
        
        #檢查使用者有無場地/器材預約紀錄
        if not member_rent_site:
            context['member_rent_site'] = False
        else:
            context['member_rent_site'] = member_rent_site
        
        if not member_rent_equipment:
            context['member_rent_equipment'] = False
        else:
            context['member_rent_equipment'] = member_rent_equipment

        return render(request, "historical_rental_record.html", context)

