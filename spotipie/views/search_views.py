import requests
from django.shortcuts import HttpResponse, render


def search_tracks(query, access_token):
    # 트랙을 검색하는 기능 / api와 상호작용
    # query는 검색할 트랙 제목이나 아티스트 이름과 같은 문자열을 뜻함
    # access_token : spotify에 요청할 때 필요한 인증 토큰
    url = "https://api.spotify.com/v1/search"
    # spotify의 검색 api 엔드포인트 url
    # /v1/search 스포티파이의 검색 경로
    headers = {
        "Authorization": f"Bearer {access_token}"
        # api 호출 시 필요로 하는 http 헤더를 설정
    }
    params = {
        # 쿼리 파라미터
        "q": query,
        "type": "track",
        "limit": 10
    }
    response = requests.get(url, headers=headers, params=params)
    #  클라이언트와 서버가 데이터를 주고받을 때 중요한 정보를 전달
    # request 모듈 -> http 요청을 쉽게 처리할 수 있는 라이브러리
    # get()함수 -> get요청을 보낼 때 사용한다.
    search_results = response.json()
    #  스포티파이 api로부터 반환된 json 응답을 담고 있는 딕셔너리 -> 검색 결과 관련 다양한 데이터 들어있다
    tracks = search_results.get('tracks', {}).get('items', [])
    # tracks vs items -> 노트북 사진 참고

    # 아티스트 정보 추가
    for track in tracks:
        artist_id = track['artists'][0]['id']
        # 첫 번째 트랙의 아티스트 id(정보) 가져온다
        artist_info = get_artist_info(artist_id, access_token)
        track['artist_image'] = artist_info.get('images', [{}])[0].get('url', '')
        # tracks 리스트는 search_results 안에 존재. track에 추가된 아티스트 이미지는 search_results에 추가됨
        # tracks 내부의 track에 아티스트 이미지 추가

    return search_results

def search(request):
    # 사용자 인터페이와 관련된 로직 처리
    query = request.GET.get('query', '').strip()
    # request.GET은 get요청으로 전달된 파라미터를 가져옴
    # 여기서는 쿼리 파라미터에서 "query" 값 가져옴. 없으면 공백
    access_token = request.session.get('access_token')
    #  request.session은 장고에서 제공하는 세션을 관리하는 속성이다.
    #  세션 존재하지 않을 시 기본적으로 none반환

    if not access_token:
        return HttpResponse('Access token not found')

    if query:
        search_results = search_tracks(query, access_token)
        # query 값이 존재한다면 search_tracks 함수를 호출해서 spotify api에서 트랙을 검색
        # get요청,결과 반환
        # search_results: 이 변수는 Spotify API에서 반환된 JSON 응답을 담고 있는 딕셔너리입니다.
        tracks = search_results.get('tracks', {}).get('items', [])
        # search_results 에서 tracks와 items 의 키 값 추출, 추출값을 tracks에 저장.
        # get 메서드는 딕셔너리에서 값을 추출하는 데 사용된다.
        # 위 코드를 search_tracks에서 가져오면 안되나?(어차피 동일한데..) -> 함수의 역할과 독립성
        #  tracks = search_tracks(query, access_token) 이렇게 써도 되긴 함. 그런데 나중에 유지보수나 확장성에서 불리함
    else:
        tracks = []

    return render(request, 'spotipie/search_result.html', {'tracks': tracks, 'access_token': access_token})

def get_artist_info(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()