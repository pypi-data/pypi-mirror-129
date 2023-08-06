#Cmd Packaging libs in python

# to upgrade tools 
> python3 -m pip install --user --upgrade setuptools wheel
> python3 -m pip install --user --upgrade twine


#to upload library:
>cd $folder_lib_name

>python3 setup.py sdist bdist_wheel	#Genera los archivos para subir a www.pypi.org
>twine upload dist/* 			#Sube los archivos para distribución, previo configurar una cuenta en www.pypi.org 


#to install de library
pip install $lib_name			#se descarga en este caso se creo la demo para el proy integrador: calc_demo_pi


#using lib: (eg: ipython)
In [1]: from calc_demo_pi.Chebychev import func    #se importa la bibl 
In [2]: func.run()				   #corre una funcion print.


Out[2]: 'Successful!'

