import requests
import json
# json 모듈을 임포트
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
import urllib.parse

def play_track(request, track_id):
    # 특정 트랙의 상세 정보를 표시
    access_token = request.session.get('access_token')

    if not access_token:
        return HttpResponse('Access token not found')

    # Spotify에서 트랙 정보를 가져온다.
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers)
    track = response.json()

    return render(request, 'spotipie/play_track.html', {
        'track_id': track_id,
        'track': track,
        'access_token': access_token
    })

def my_library(request):
    # my_library.html 템플릿을 렌더링
    access_token = request.session.get('access_token')
    # 엑세스 코드 전달해 줘야만 '내 라이브러리' 에서 곡 재생 가능함
    return render(request, 'spotipie/my_library.html', {'access_token': access_token})


def delete_track(request, track_uri):
    if request.method == 'DELETE':
        decoded_uri = urllib.parse.unquote(track_uri)
        # track_uri를 디코딩함
        print(decoded_uri)  # 디버그용 로그
        # 여기서 decoded_uri를 사용해 삭제 로직을 처리
        return JsonResponse({'message': '곡이 삭제되었습니다!'}, status=200)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)