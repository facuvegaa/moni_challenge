from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import LoanRequest
from .forms import LoanForm
import requests

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/prestamos/')
        else:
            error_message = 'Invalid login credentials'
    else:
        error_message = ''
    return render(request, 'admin_login.html', {'error_message': error_message})

def es_admin(user):
    return user.is_authenticated and user.is_staff

def solo_administradores(view_func):
    decorated_view_func = user_passes_test(
        lambda user: es_admin(user),
        login_url='/admin_login/'
    )(view_func)
    return decorated_view_func

def solicitar_prestamo(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']

            # Llamada a la API para obtener la respuesta
            headers = {'credential': 'ZGpzOTAzaWZuc2Zpb25kZnNubm5u'}
            url = f'https://api.moni.com.ar/api/v4/scoring/pre-score/{dni}'
            response = requests.get(url, headers=headers)

            # Si la respuesta es exitosa, se actualiza el estado de aprobado
            if response.status_code != 200:
                return render(request, "error.html")
            else:
                if response.json()['status'] == "approve":
                    aprobado = True
                else:
                    aprobado = False

            # Crear la instancia del modelo y guardarla en la base de datos
            loan_request = form.save(commit=False)
            loan_request.aprobado = aprobado
            loan_request.respuesta_api = response.content
            loan_request.save()

            # Renderizar la plantilla de respuesta
            return render(request, 'resultado.html', {'aprobado': aprobado})
        else:
            # Si el formulario no es válido, volver a renderizar el formulario con los errores
            return render(request, 'pedido.html', {'form': form})
    else:
        # Si el método no es POST, renderizar la plantilla del formulario con un formulario vacío
        form = LoanForm()
        return render(request, 'pedido.html', {'form': form})


@solo_administradores
def listar_prestamos_solicitados(request):
    loan_requests = LoanRequest.objects.all()
    return render(request, 'prestamos_solicitados.html', {'loan_requests': loan_requests})


@solo_administradores
def editar_prestamo_solicitado(request, pk):
    loan_request = LoanRequest.objects.get(id=pk)
    form = LoanForm(instance=loan_request)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan_request)
        if form.is_valid():
            form.save()
            loan_requests = LoanRequest.objects.all
            return render(request, 'prestamos_solicitados.html', {'loan_requests': loan_requests})
    else:
        form = LoanForm(loan_request)
        return render(request, 'editar_solicitud.html', {'form': loan_request})


@solo_administradores
def eliminar_prestamo_solicitado(request, pk):
    loan_request = LoanRequest.objects.get(id=pk)
    if request.method == 'POST':
        loan_request.delete()
        loan_requests = LoanRequest.objects.all()
        return render(request, 'prestamos_solicitados.html', {'loan_requests': loan_requests})
    return render(request, 'eliminar_solicitud.html', {'item' : loan_request})
