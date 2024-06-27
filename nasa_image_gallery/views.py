# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.transport.transport import getAllImages
from .layers.generic.mapper import fromRequestIntoNASACard

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    api_images = getAllImages()  # obtienes todas las imágenes de la API
    favourite_list = []
    
    # con el mapper transformamos el json en una estructura que el html pueda leer
    images = []  
    for api_image in api_images:  
        image = fromRequestIntoNASACard(api_image)  
        images.append(image)  

    return images, favourite_list


# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    images, favourite_list = getAllImagesAndFavouriteList(request)  
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )




# # función utilizada en el buscador.
# def search(request):
#     images, favourite_list = getAllImagesAndFavouriteList(request)
#     search_msg = request.POST.get('query', '')

#     # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
#     pass


def search(request):  
    # Obtén el mensaje de búsqueda del POST request  
    search_msg = request.POST.get('query', None)  
  
    if search_msg is not None and search_msg != '':  
        # Si se proporcionó una palabra clave, obtén las imágenes que coinciden con esa palabra clave  
        images = getAllImages(input=search_msg)  
    else:  
        # Si no se proporcionó una palabra clave, obtén todas las imágenes  
        images = getAllImages()  
  
    # Convierte cada imagen a un formato que tu template pueda entender  
    images = [fromRequestIntoNASACard(api_image) for api_image in images]  
  
    # Obtén la lista de imágenes favoritas del usuario  
    favourite_list = []  
  
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})  




# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    pass


@login_required
def deleteFavourite(request):
    pass


@login_required
def exit(request):
    pass