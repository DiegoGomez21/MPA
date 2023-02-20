Proyecto MPA con DJANGO-REST-FRAMEWORK y motor de plantillas de django

Autor: Diego Alejandro Gómez Pedraza
Código: 2211060

La vista principal del proyecto se encuentra en esta URL


->   http://127.0.0.1:8000/api/auth/login

FUNCIONAMIENTOS DE LA APLICACION
los post que son privados solo podrán ser visualizados y editados por el administrador superusuario o por el usuario creador del post
Le superusuario tiene derecho sobre todos los END-Point de la aplicacion
El username con el que se iniciará sesion será el EMAIL como valor unico e irrepetible

Tambien se puede acceder a la pagina de administrador de django para poder ver detalladamente cada modelo con sus elementos en la base de datos

->    http://127.0.0.1:8000/admin

Tambien incluí el sistema de documentacion para los END-points cuya direccion serán

->    http://127.0.0.1:8000/docs
->    http://127.0.0.1:8000/redocs
