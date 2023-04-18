"""Loan request Views."""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from .models import LoanRequest
from .forms import LoanForm
import requests


def admin_login(request):
    """
    Vista para el inicio de sesión de los administradores del sistema.

    Si el método de solicitud es POST, se verifica la autenticidad del usuario y
    se le redirige a la página de administración de préstamos. En caso contrario, se
    muestra la plantilla de inicio de sesión.

    Args:
        request: Objeto HttpRequest que contiene los metadatos acerca de la solicitud HTTP.

    Returns:
        HttpResponse: Un objeto de respuesta HTTP con la plantilla de inicio de sesión de
            los administradores del sistema.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/prestamos/")
        else:
            error_message = "Invalid login credentials"
    else:
        error_message = ""
    return render(request, "admin_login.html", {"error_message": error_message})


def es_admin(user):
    """
    Esta función comprueba si el usuario es un administrador o no.

    Args:
        user: Un objeto User de Django.

    Returns:
        Un valor booleano que indica si el usuario es un administrador o no.
    """
    return user.is_authenticated and user.is_staff


def solo_administradores(view_func):
    """
    Esta función es un decorador.

    Comprueba si el usuario es un administrador antes de permitir que se ejecute la vista.

    Args:
        view_func: La vista que se está decorando.

    Returns:
        La vista decorada.
    """
    decorated_view_func = user_passes_test(
        lambda user: es_admin(user), login_url="/admin_login/"
    )(view_func)
    return decorated_view_func


def solicitar_prestamo(request):
    """
    Esta función maneja la solicitud de préstamo.

    Si se envía un formulario, llama a una API para obtener una respuesta, actualiza el estado del préstamo y guarda la solicitud en la base
    de datos.

    Args:
        request: El objeto HttpRequest de Django.

    Returns:
        Un objeto HttpResponse de Django que contiene una página HTML que indica si el préstamo
        fue aprobado o no.
    """
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]

            headers = {"credential": "ZGpzOTAzaWZuc2Zpb25kZnNubm5u"}
            url = f"https://api.moni.com.ar/api/v4/scoring/pre-score/{dni}"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return render(request, "error.html")
            else:
                if response.json()["status"] == "approve":
                    aprobado = True
                else:
                    aprobado = False

            loan_request = form.save(commit=False)
            loan_request.aprobado = aprobado
            loan_request.respuesta_api = response.content
            loan_request.save()

            return render(request, "resultado.html", {"aprobado": aprobado})
        else:
            return render(request, "pedido.html", {"form": form})
    else:
        form = LoanForm()
        return render(request, "pedido.html", {"form": form})


@solo_administradores
def listar_prestamos_solicitados(request):
    """
    Esta función muestra una lista de todas las solicitudes de préstamo.

    Args:
        request: El objeto HttpRequest de Django.

    Returns:
        Un objeto HttpResponse de Django que contiene una página HTML que muestra una lista de todas
        las solicitudes de préstamo.
    """
    loan_requests = LoanRequest.objects.all()
    return render(
        request, "prestamos_solicitados.html", {"loan_requests": loan_requests}
    )


@solo_administradores
def editar_prestamo_solicitado(request, pk):
    """
    Esta función permite editar una solicitud de préstamo existente.

    Args:
        request: El objeto HttpRequest de Django.
        pk: La clave primaria de la solicitud de préstamo que se está editando.

    Returns:
        Un objeto HttpResponse de Django que contiene una página HTML con un formulario que permite
        editar la solicitud de préstamo.
    """
    loan_request = LoanRequest.objects.get(id=pk)
    form = LoanForm(instance=loan_request)
    if request.method == "POST":
        form = LoanForm(request.POST, instance=loan_request)
        if form.is_valid():
            form.save()
            loan_requests = LoanRequest.objects.all
            return render(
                request, "prestamos_solicitados.html", {"loan_requests": loan_requests}
            )
    else:
        form = LoanForm(loan_request)
        return render(request, "editar_solicitud.html", {"form": loan_request})


@solo_administradores
def eliminar_prestamo_solicitado(request, pk):
    """
    Esta función permite eliminar una solicitud de préstamo existente.

    Args:
        request: El objeto HttpRequest de Django.
        pk: La clave primaria de la solicitud de préstamo que se está eliminando.

    Returns:
        Un objeto HttpResponse de Django que contiene una página HTML que indica que la solicitud de
        préstamo ha sido eliminada.
    """
    loan_request = LoanRequest.objects.get(id=pk)
    if request.method == "POST":
        loan_request.delete()
        loan_requests = LoanRequest.objects.all()
        return render(
            request, "prestamos_solicitados.html", {"loan_requests": loan_requests}
        )
    return render(request, "eliminar_solicitud.html", {"item": loan_request})
