from ast import Del
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .models import Movie, Review, List
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.

class Home(TemplateView):
    template_name='home.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['lists']=List.objects.filter(user=self.request.user)
        context['films']= Movie.objects.all()
        return context

class MovieList(TemplateView):
    template_name= 'movie_list.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        name= self.request.GET.get('name')
        if name != None:
            context['movie']= Movie.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name}"

        else:
            context['movie']= Movie.objects.all()
            context['header']= f'Trending Movies'
        return context


class MovieCreate(CreateView):
    model=Movie
    fields=['name', 'image', 'year', 'description']
    template_name='movie_create.html'
    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.pk})

class MovieDetail(DetailView):
    model=Movie
    template_name= 'movie_detail.html'


class MovieUpdate(UpdateView):
    model= Movie
    fields= ['name', 'image', 'year', 'description']
    template_name= 'movie_update.html'
    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.pk})

class MovieDelete(DeleteView):
    model= Movie
    template_name= 'movie_delete_confirmation.html'
    success_url= '/movies/'

class ReviewCreate(View):
    def post(self, request, pk):
        title=request.POST.get('title')
        rating=request.POST.get('rating')
        reason=request.POST.get('reason')
        movie=Movie.objects.get(pk=pk)
        Review.objects.create(title=title, rating=rating, reason=reason, movie=movie)
        return redirect('movie_detail', pk=pk)

class ListMovieAssoc(View):

    def get(self, request, pk, movie_pk):
        # get the query param from the url
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            # get the playlist by the id and
            # remove from the join table the given movie_id
            List.objects.get(pk=pk).movies.remove(movie_pk)
        if assoc == "add":
            # get the playlist by the id and
            # add to the join table the given movie_id
            List.objects.get(pk=pk).movies.add(movie_pk)
        return redirect('/')

class ListDetail(DetailView, DeleteView):
    model=List
    template_name= 'list_detail.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['films']= Movie.objects.all()
        return context
    success_url= '/'

    
 

class ListCreate(CreateView):
    model = List
    fields = ['title']
    template_name = "list_create.html"
    # This is our new method that will add the user into our submitted form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ListCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('list_detail', kwargs={'pk': self.object.pk})



class Signup(View):
    # show a form to fill out
        def get(self, request):
            form = UserCreationForm()
            context = {"form": form}
            return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
        def post(self, request):
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("artist_list")
            else:
                context = {"form": form}
                return render(request, "registration/signup.html", context)
