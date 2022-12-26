from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import MemberModelForm, LoginModelForm
from .models import Member
from Member_management.models import Department
from django.contrib import messages
from django.http import HttpResponseRedirect

#註冊
@csrf_exempt
def register(request):
    form = MemberModelForm()
    context = {}
    if request.method == "POST":
        form = MemberModelForm(request.POST, request.FILES)
        if form.is_valid():
            #確認密碼
            password = form.cleaned_data['password']
            check_password = request.POST['check_password']
            #確認email沒有重複
            email = form.cleaned_data['email']
            #確認電話號碼格式正確
            cellphone = form.cleaned_data['tel']
            
            if(password != check_password):
                messages.error(request, "密碼與確認密碼不一置，請重新輸入")
                return HttpResponseRedirect(request.path_info)
            elif(Member.objects.filter(email=email).exists()):
                messages.error(request, "此帳號已存在，請輸入其他Email進行註冊")
                return HttpResponseRedirect(request.path_info)
            elif(len(password)<8):
                messages.error(request, "密碼長度需要大於8")
                return HttpResponseRedirect(request.path_info)
            elif(len(cellphone) != 10):
                messages.error(request, "輸入手機號碼長度錯誤! (格式: 09開頭+8位數字)")
                return HttpResponseRedirect(request.path_info)
            elif(cellphone[0:2] != '09'):
                messages.error(request, "輸入手機號碼格式錯誤! (格式: 09開頭+8位數字)")
                return HttpResponseRedirect(request.path_info)          
            else:
                heck_cellphone = ['0','1','2','3','4','5','6','7','8','9']
                for char in cellphone:
                    if(char not in heck_cellphone):
                        messages.error(request, "輸入手機號碼格式錯誤! (格式: 09開頭+8位數字)")
                        return HttpResponseRedirect(request.path_info)
    
                form.save()
                context['successful_submit']=True
    context['form']=form

    return render(request, 'register.html', context)

#登入
@csrf_exempt
def login(request):
    form = LoginModelForm()
    context = {}
    if request.method == "POST":
        form = LoginModelForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #email與password是否存在Member table中
            if Member.objects.filter(email=email, password=password).exists():

                #GET Member的name和identity
                member_data = Member.objects.filter(email=email, password=password).values("id","name","identity")
                
                id = member_data[0]["id"]
                name = member_data[0]["name"]
                identity = member_data[0]["identity"]
                
                #存入session
                request.session['id'] = id
                request.session['email'] = email
                request.session['name'] = name
                request.session['identity'] = identity
                
                #一般使用者登入跳轉到home_member.html
                if identity == 1:
                    return redirect('/rental/home_page/')
                elif identity == 2:
                    if Department.objects.filter(email=email).exists():
                        return redirect('/es_management/home_page/')
                    else:
                        messages.error(request, "此場材管理員帳號未被登記，請聯繫系統管理員!")
                        return HttpResponseRedirect(request.path_info)
                elif identity == 3:
                    return redirect('/member_management/search_member/')
                #缺場材管理URL
                else:
                    messages.error(request, "此會員身分錯誤，請聯繫系統管理員")
                    return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, "email或密碼輸入錯誤")
                return HttpResponseRedirect(request.path_info)
    
    context['form']=form
    return render(request, 'login.html', context)            


#修改會員資料
@csrf_exempt
def edit_member_profile(request):
    if 'email' not in request.session:
        return redirect('/member/login/')
    else:
        
        if request.method == "POST":
            old_password = request.POST['old_password']
            member_id = request.session.get('id')
            
            if Member.objects.filter(id=member_id, password=old_password).exists():
                cellphone = request.POST['cellphone']
                new_password = request.POST['new_password']
                if(len(cellphone) != 0):
                    if(len(cellphone) != 10):
                        messages.error(request, "輸入手機號碼長度錯誤! (格式: 09開頭+8位數字)")
                        return HttpResponseRedirect(request.path_info)
                    elif(cellphone[0:2] != '09'):
                        messages.error(request, "輸入手機號碼格式錯誤! (格式: 09開頭+8位數字)")
                        return HttpResponseRedirect(request.path_info)
                    else:
                        heck_cellphone = ['0','1','2','3','4','5','6','7','8','9']
                        for char in cellphone:
                            if(char not in heck_cellphone):
                                messages.error(request, "輸入手機號碼格式錯誤! (格式: 09開頭+8位數字)")
                                return HttpResponseRedirect(request.path_info)
                        
                        #修改會員手機電話
                        Member.objects.filter(id=member_id).update(tel=cellphone)
                        messages.success(request, "手機號碼修改成功!")
                        return HttpResponseRedirect(request.path_info)
                elif(len(new_password) != 0):
                    if(len(new_password) < 8):
                        messages.error(request, "輸入新密碼長度錯誤! (格式: 密碼長度8位數(含)以上)")
                        return HttpResponseRedirect(request.path_info)
                    else:
                        #修改會員密碼
                        Member.objects.filter(id=member_id).update(password=new_password)
                        messages.success(request, "新密碼修改成功!")
                        return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, "請輸入手機號碼或新密碼進行修改!")
                    return HttpResponseRedirect(request.path_info)

                #new_password = request.POST['new_password']
            else:
                messages.error(request, "輸入舊密碼錯誤!!")
                return HttpResponseRedirect(request.path_info)
        
        context={}
        identity = request.session.get("identity")
        if(identity == 1):
            context["base_html"] = 'base_member.html'
            context["active_number"] = 'active4'

        elif(identity == 2):
            context["base_html"] = 'base_site_equipment_management.html'
        else:
            context["base_html"] = 'base_member_management.html'  

        return render(request, 'edit_member_profile.html', context)   

#登出
@csrf_exempt
def logout(request):
    if request.method == "POST":
        request.session.clear()
        return redirect('/member/login/')
    