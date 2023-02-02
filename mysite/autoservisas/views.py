from .models import Automobilio_modelis, Automobilis, Uzsakymas, Uzsakymo_eilute, Paslauga
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import UzsakymoKomentaraiForma, UserUpdateForm, ProfilisUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if username:
            if password == password2:
                # tikriname, ar neužimtas username
                if User.objects.filter(username=username).exists():
                    messages.error(request, f'Vartotojo vardas {username} užimtas!')
                    return redirect('register')
                else:
                    # tikriname, ar nėra tokio pat email
                    if User.objects.filter(email=email).exists():
                        messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                        return redirect('register')
                    else:
                        # jeigu viskas tvarkoje, sukuriame naują vartotoją
                        User.objects.create_user(username=username, email=email, password=password)
                        messages.info(request, f'Vartotojas {username} užregistruotas!')
                        return redirect('login')
            else:
                messages.error(request, 'Slaptažodžiai nesutampa!')
                return redirect('register')
        else:
            messages.error(request, 'Vartotojo vardas neįvestas!')
    return render(request, 'registration/register.html')


def index(request):
    num_paslaugu = Paslauga.objects.count()
    num_atliktos_paslaugos = Uzsakymo_eilute.objects.filter(status__exact='s').count()
    num_automobiliu = Automobilis.objects.count()
    num_vizitai = request.session.get('num_vizitai', 1)
    request.session['num_vizitai'] = num_vizitai + 1
    context = {
        'num_paslaugu': num_paslaugu,
        'num_atliktos_paslaugos': num_atliktos_paslaugos,
        'num_automobiliu': num_automobiliu,
        'num_vizitai': num_vizitai,
    }
    return render(request, 'index.html', context=context)


def automobiliai(request):
    paginator = Paginator(Automobilis.objects.all(), 2)
    page_number = request.GET.get('page')
    puslapiuoti_automobiliai = paginator.get_page(page_number)
    kontekstas = {
        'automobiliai': puslapiuoti_automobiliai
    }
    return render(request, 'automobiliai.html', context=kontekstas)


def automobilis(request, automobilis_id):
    vienas_automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, "automobilis.html", {'automobilis': vienas_automobilis})


class UzsakymaiListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 2
    template_name = 'uzsakymai.html'


class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas.html'
    context_object_name = "uzsakymas"
    form_class = UzsakymoKomentaraiForma

    def get_success_url(self):
        return reverse('uzsakymai_detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.komentatorius = self.request.user
        form.save()
        return super(UzsakymasDetailView, self).form_valid(form)


class UzsakymasByUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'manouzsakymai.html'
    paginate_by = 2

    def get_queryset(self):
        return Uzsakymas.objects.filter(uzsakovas=self.request.user).order_by('ivykdytas_iki')

# class UzsakymasUserCreateView(LoginRequiredMixin, generic.CreateView):
#     model = Uzsakymas
#     fields = ['automobilis_id', 'ivykdytas_iki']
#     success_url = 'autoservisas/manouzsakymai/'
#     template_name =
#
#     def form_valid(self, form):
#         form.instance.uzsakovas = self.request.user
#         return super().form_valid(form)



def paslaugos(request):
    paslaugos = Paslauga.objects.all()
    return render(request, 'paslaugos.html', context={'paslaugos': paslaugos})


def paslauga(request, paslauga_id):
    viena_pasaluaga = get_object_or_404(Paslauga, pk=paslauga_id)
    return render(request, 'paslauga.html', context={'paslauga': viena_pasaluaga})


def search(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(valstybinis_nr__icontains=query) |
                                                Q(vin_kodas__icontains=query) |
                                                Q(kliento_v__icontains=query) |
                                                Q(valstybinis_nr__icontains=query) |
                                                Q(automobilio_modelis_id__marke__icontains=query) |
                                                Q(automobilio_modelis_id__modelis__icontains=query)
                                                )
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    kontekstas = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', kontekstas)
