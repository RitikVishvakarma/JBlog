from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    paginator = Paginator(allPosts, 3)
    page = request.GET.get('page')
    allPosts = paginator.get_page(page)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    # print(allPosts)
    context = {'allPosts':allPosts, 'pages':pages}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    # print(comments, replies)
    # print(replyDict)
    context = {'post':post, 'comments':comments, 'user':request.user, 'replyDict':replyDict}
    return render(request, 'blog/blogPost.html', context)
    # return HttpResponse(f'This is blog: {slug}')

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your replay has been posted successfully")
    return redirect(f"/blog/{post.slug}")