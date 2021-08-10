import pafy

url = 'https://www.youtube.com/watch?v=5FNA8Hsj8Vs&ab_channel=%EA%B8%B0%EB%AA%BD%EC%B4%88'
video = pafy.new(url)

print('TITLE : %s' % video.title)