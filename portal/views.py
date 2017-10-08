from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import LiteratureTypeForm, LiteratureForm, LiteratureForm_b, UserForm
from .models import LiteratureType, Literature


LIT_FILE_TYPES = ['pdf']


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'portal/login.html')
    else:
        # albums = Album.objects.filter(user=request.user)
        lit_types = LiteratureType.objects.all()
        lit_results = Literature.objects.all()
        query = request.GET.get("q")
        if query:
            lit_types = lit_types.filter(
                Q(lit_type_name__icontains=query)
            ).distinct()
            lit_results = lit_results.filter(
                Q(lit_title__icontains=query)
            ).distinct()
            return render(request, 'portal/index.html', {
                'lit_types': lit_types,
                'literatures': lit_results,
            })
        else:
            return render(request, 'portal/index.html', {'lit_types': lit_types})


def detail(request, lit_type_id):
    if not request.user.is_authenticated():
        return render(request, 'portal/login.html')
    else:
        user = request.user
        lit_type = get_object_or_404(LiteratureType, pk=lit_type_id)
        return render(request, 'portal/detail.html', {'lit_type': lit_type, 'user': user})


def literatures(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'portal/login.html')
    else:
        try:
            literature_ids = []
            #for album in Album.objects.filter(user=request.user):
            for lit_type in LiteratureType.objects.all():
                for literature in lit_type.literature_set.all():
                    literature_ids.append(literature.pk)
            users_literatures = Literature.objects.filter(pk__in=literature_ids)

        except LiteratureType.DoesNotExist:
            users_literatures = []
        return render(request, 'portal/literatures.html', {
            'literature_list': users_literatures,
            'filter_by': filter_by,
        })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                lit_types = LiteratureType.objects.all()
                return render(request, 'portal/index.html', {'lit_types': lit_types})
            else:
                return render(request, 'portal/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'portal/login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'portal/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
               # lit_types = LiteratureType.objects.filter(user=request.user)
                return render(request, 'portal/index.html')
    context = {
        "form": form,
    }
    return render(request, 'portal/register.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'portal/login.html', context)


def create_lit_type(request):
    if not request.user.is_authenticated():
        return render(request, 'portal/login.html')
    else:
        form = LiteratureTypeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            lit_type = form.save(commit=False)
            lit_type.user = request.user
            lit_type.save()
            return render(request, 'portal/detail.html', {'lit_type': lit_type})
        context = {
            "form": form,
        }
        return render(request, 'portal/create_lit_type.html', context)


def contribute(request, lit_type_id):
    form = LiteratureForm(request.POST or None, request.FILES or None)
    lit_type = get_object_or_404(LiteratureType, pk=lit_type_id)
    if form.is_valid():
        lit_type_lits = lit_type.literature_set.all()
        for l in lit_type_lits:
            if l.lit_title == form.cleaned_data.get("lit_title"):
                context = {
                    'lit_type': lit_type,
                    'form': form,
                    'error_message': 'You already added that literature',
                }
                return render(request, 'portal/contribute.html', context)
        literature = form.save(commit=False)
        literature.user = request.user
        literature.lit_type = lit_type
        literature.lit_file = request.FILES['lit_file']
        file_type = literature.lit_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in LIT_FILE_TYPES:
            context = {
                'lit_type': lit_type,
                'form': form,
                'error_message': 'Literature file must be PDF',
            }
            return render(request, 'portal/contribute.html', context)

        literature.save()
        return render(request, 'portal/detail.html', {'lit_type': lit_type})
    context = {
        'lit_type': lit_type,
        'form': form,
    }
    return render(request, 'portal/contribute.html', context)


def contribute_b(request):
    if not request.user.is_authenticated():
        return render(request, 'portal/login.html')
    else:
        form = LiteratureForm_b(request.POST or None, request.FILES or None)
        lit_type = request.POST.get('lit_type')
        if form.is_valid():
            lit_type_lits = lit_type.literature_set.all()
            for l in lit_type_lits:
                if l.lit_title == form.cleaned_data.get("lit_title"):
                    context = {
                        'form': form,
                        'error_message': 'You already added that literature',
                    }
                    return render(request, 'portal/contribute_b.html', context)
            literature = form.save(commit=False)
            literature.user = request.user
            literature.lit_type = lit_type
            literature.lit_file = request.FILES['lit_file']
            file_type = literature.lit_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in LIT_FILE_TYPES:
                context = {
                    'form': form,
                    'error_message': 'Literature file must be PDF',
                }
                return render(request, 'portal/contribute_b.html', context)

            literature.save()
            return render(request, 'portal/detail.html', {'lit_type': lit_type})
        context = {
            'form': form,
        }
        return render(request, 'portal/contribute_b.html', context)


def termsandcondition(request):
    return render(request, "portal/termsandcondition.html")
