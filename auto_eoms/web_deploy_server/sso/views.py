import requests
from urllib import parse
import re

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.


base_url = r'http://sso.sunnyoptical.cn'
home_url = 'http://10.1.1.79:9999'


def to_landing_page(request):

    ticket = request.GET.get('ticket')
    session_info = request.session.get('is_login')

    url_path = request.path
    if not session_info and not ticket:
        url = base_url + '/login?service=' + encoded_url(url_path)
        return redirect(url)
    if ticket:
        url = base_url + '/serviceValidate'
        params = {'ticket': ticket, 'service': home_url + url_path}

        r = requests.get(url, params)

        if not session_info:
            uid = get_uid(r.text)
            request.session['uid'] = uid
            request.session['is_login'] = True
            request.session.set_expiry(7 * 24 * 60 * 60)

            if not uid:
                return redirect(url)

        if url_path == '/get_uid':
            return JsonResponse({'uid': request.session.get("uid")})
        return render(request, 'index.html')

    if session_info:
        if url_path == '/get_uid':
            return JsonResponse({'uid': request.session.get("uid")})
        return render(request, 'index.html')


def encoded_url(url_route):
    """url编码"""
    url = home_url + url_route
    return parse.quote(url, encoding='utf-8')


def get_uid(xml_text):
    """获得UID"""
    uid_info = re.compile(r'<cas:uid>\d+').findall(xml_text)
    if len(uid_info) >= 1:
        return get_digit(uid_info[0])
    return


def get_digit(string):
    return re.findall(r"\d+", string)[0]


def logout(request):
    request.session.flush()
    logout_url = 'http://sso.sunnyoptical.cn/logout?service=' + home_url
    return redirect(logout_url)
