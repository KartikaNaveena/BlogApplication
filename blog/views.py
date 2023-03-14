
from django.shortcuts import  render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.shortcuts import render,redirect,get_object_or_404
from .forms import UpdateUserForm, UpdateProfileForm
from django.urls import  reverse_lazy
from .models import Post,BlogComment,Profile
from django.views import View
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.forms import BlogPostForm,SignUpForm,NewCommentForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin





class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')




class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


   
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    

    def get_context_data(self, **kwargs):
        
        data = super().get_context_data(**kwargs)

        comments_connected = BlogComment.objects.filter(
            blogpost_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data
    def post(self, request, *args, **kwargs):
        new_comment = BlogComment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  blogpost_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			
			messages.info(request,"Incorrect details")
                
                 
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def BlogPostLike(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse("home"))
   





def add_blogs(request):
    form = BlogPostForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.slug = slugify(post.title)
        post.author = request.user
        post.status=1
        post.save()

        messages.success(request,"Post added successfully")
        return redirect("home")
    return render(request,"add_blogs.html",{"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")


def deletePost(request,slug):
    post = get_object_or_404(Post,slug=slug)

    post.delete()

    messages.success(request,"Post deleted successfully")

    return redirect("home")

def updatePost(request, slug):

    post = get_object_or_404(Post, slug=slug)
    form = BlogPostForm(request.POST or None,request.FILES or None,instance = post)
    if form.is_valid():
        post = form.save(commit=False)
        
        post.author = request.user
        post.save()

        messages.success(request,"Post updated successfully")
        return redirect("home")


    return render(request,"edit_blog.html",{"form":form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to home page
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register1.html', {'form': form})