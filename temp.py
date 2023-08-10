import re

video_url="https://www.youtube.com/watch?v=wcIf3huwFhc&ab_channel=WRG%EC%9A%B0%EB%A6%AC%EA%B0%80%EB%93%A3%EA%B3%A0%EC%8B%B6%EC%96%B4%EC%84%9C%EC%97%B0%EC%A3%BC%ED%95%9Cplaylist"
reg = re.compile("\?v=.*&")
video_id = reg.search(video_url).group()[3:-1]
thumbnail_url= f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'

