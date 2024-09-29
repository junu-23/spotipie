from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'artist', 'album_cover']

# forms.py 파일은 폼을 정의하는 역할. 사용자로 부터 입력 받기 위한 구조 제공