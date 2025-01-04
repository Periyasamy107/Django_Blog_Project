from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from blog.models import Post, AboutUs
from django.http import Http404
from django.core.paginator import Paginator 
from .forms import ContactForm


# Create your views here.

# posts = [
#         {'id' : 1,'title' : 'Post 1', 'content' : 'Post content 1'},
#         {'id' : 2,'title' : 'Post 2', 'content' : 'Post content 2'},
#         {'id' : 3,'title' : 'Post 3', 'content' : 'Post content 3'},
#         {'id' : 4,'title' : 'Post 4', 'content' : 'Post content 4'},
#         {'id' : 5,'title' : 'Post 5', 'content' : 'Post content 5'},
#         {'id' : 6,'title' : 'Post 6', 'content' : 'Post content 6'}
#     ]

def index(request):
    blog_title = 'Latest Posts'

    # Getting Data from Post model
    all_posts = Post.objects.all()

    # Pagination 
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', { 'blog_title' : blog_title, 'page_obj' : page_obj })

def details(request, slug):
    # Getting Static Data from posts in above list
    # post = next((item for item in posts if item['id'] == int(post_id)), None)

    try:
        # Getting Data from Post id 
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category=post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    # logger = logging.getLogger('TESTING')
    # logger.debug(f'Post value is : {post}')
    return render(request, 'blog/details.html', {'post': post, 'related_posts': related_posts})

def old_url_redirect(request):
    # return redirect('new_url')
    return redirect(reverse('blog:new_page_url'))

def new_url_view(request):
    return HttpResponse('<h1> This is new url view </h1>')

def contact_view(request):
    # logger = logging.getLogger('TESTING')
    # logger.debug(f'request.POST is : {request.POST}')
    if request.method == 'POST':
        form = ContactForm(request.POST)

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        logger = logging.getLogger('TESTING')
        if form.is_valid():
            logger.debug(f'Form value is : {form.cleaned_data}')
            # send an email or save data to database
            success_message = 'Form submitted successfully'
            return render(request, 'blog/contact.html', {'form':form, 'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request, 'blog/contact.html', {'form':form, 'name':name, 'email':email, 'message':message})
    return render(request, 'blog/contact.html')

def about_view(request):
    about_content = AboutUs.objects.first().content
    return render(request, 'blog/about.html', {'about_content':about_content})