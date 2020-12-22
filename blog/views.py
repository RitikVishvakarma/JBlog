from django.shortcuts import render, HttpResponse
from blog.models import Post
# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    # print(allPosts)
    context = {'allPosts':allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    return render(request, 'blog/blogPost.html')
    # return HttpResponse(f'This is blog: {slug}')