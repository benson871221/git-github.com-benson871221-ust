from django.shortcuts import render
from Member.models import Member
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# 系統管理員查詢會員資料
@csrf_exempt
def search_member(request):

    context = {}

    filter_obj = list(Member.objects.all().values('id','name','email','identity','sex','birthday','tel'))
    context["member_set"] = filter_obj
    #return JsonResponse(filter_obj, safe=False)
    return render(request, 'member_manage.html',context)

#以 email 查詢單筆會員資料
@csrf_exempt
def email_search_member(request):
    context = {}
    data = request.POST
    search_email = data.get('email')

    if Member.objects.filter(email=search_email).exists():
       return_data =  list(Member.objects.filter(email=search_email).values('id','name','email','identity','sex','birthday','tel'))
    else:
       messages.error(request, "查無此人")
       return render(request, 'member_manage.html')

    context["one_member_set"] = return_data
    return render(request, 'member_manage.html',context)

# 刪除會員
@csrf_exempt
def delete_member(request):
    if request.method == "POST":
        member_id = request.POST.get('member_id')
        data = Member.objects.get(id=member_id)
        data.delete()
        return HttpResponseRedirect(reverse('member_management:search_member'))

    return render(request, 'member_manage.html')

#新增會員資料
