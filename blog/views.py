from django.shortcuts import render

# Create your views here.


'''
all blogs list
'''
def list(request):
    return render(request, 'blog/list.html',)


'''
user blog list
'''
def blogsList(request):
    return  render(request, 'blog/blogList.html', )