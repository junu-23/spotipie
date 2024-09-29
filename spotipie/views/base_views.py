import os
import requests
from django.shortcuts import redirect, HttpResponse, render
from env.env import CLIENT_ID, CLIENT_SECRET
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

def index(request):
    return render(request, 'spotipie/music_list.html')

def favicon_view(request):
    return HttpResponse(status=204)  # 빈 응답을 반환
def callback(request):
    code = request.GET.get('code')
    # 스포티파이가 제공하는 인증 코드
    if code:
        response = requests.post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            # 스포티파이 인증 서버에서 리디렉션 uri를 통해 받은 인증 코드
            'redirect_uri': 'http://localhost:8000/spotipie/callback/',
            # Spotify Developer 대시보드에 등록된 리디렉션 URI
            # 인증 결과 처리하는 전용 엔드포인트 => 로그인 성공시 여기로 인증 결과 돌려보내 줌(인증코드 포함)
            # 엔드포인트 : 웹 api에서 특정 리소스나 기능에 접근하기 위한 url 경로
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
            # 하드코딩 X => 보안문제!
        })
        response_data = response.json()
        # 응답을 JSON 형식으로 변환한다.
        access_token = response_data.get('access_token')
        if access_token:
            request.session['access_token'] = access_token
            # 엑세스 토큰을 Django 세션에 저장한다.
            # 엑세스 토근은 api 요청에 필요한 인증 정보 포함함.
            # HttpResponse: 엑세스 토큰 포함한 응답을 클라이언트에게 반환
            return redirect('spotipie:index')
        return HttpResponse('No access token received')
    return HttpResponse('No code received')
# access 토근 받기, callback 처리
#역할: Spotify의 OAuth 인증 프로세스에서 인증 코드를 액세스 토큰으로 교환합니다
# 함수는 Spotify의 OAuth 인증 프로세스에서 중요한 역할을 하며, 사용자 인증 후 Spotify API와의 상호작용을 설정하는 데 사용됨.
# 이 함수의 주요 기능은 인증 코드를 받아 액세스 토큰으로 교환하고 이를 세션에 저장하여 API 요청에 사용할 수 있게 하는 것.

