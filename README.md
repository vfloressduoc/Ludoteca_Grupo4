**IMPORTANTE**

Recordar crear el siguiente usuario en la base de datos SQL PLUS, para poder conectarse a la database que trabajamos como grupo, la misma que esta indicada en settings.py - cambiar a orcl o ex, dependiendo del tipo de conexión que esté en su computadora.
```
SQL> conn sys as sysdba
SQL> alter session set "_ORACLE_SCRIPT"=true;
SQL> create user c##ludoteca identified by 12345;
SQL> grant connect, resource to c##ludoteca;
SQL> alter user c##ludoteca default tablespace users quota unlimited on users;
```

Creamos un **botón llamado “Llenar tablas”** en la esquina superior izquierda, al presionar una vez, ejecuta una función que inserta las categorías, proveedores y productos iniciales (es una alternativa al [script](https://github.com/vfloressduoc/Ludoteca_Grupo4/files/15157442/inserts.txt)), como las vistas recurren a la bbdd es necesario tener los productos cargados en la base de datos para verlos.

<img width="495" alt="1" src="https://github.com/vfloressduoc/Ludoteca_Grupo4/assets/145572948/560f9765-5732-4f23-9162-dfc2bb12f81d">


**La vista como administrador** (requiere crear y conectarse con un superusuario de la tabla User) cuenta con funciones diferentes a la vista de usuario normal, como manipular usuarios, productos, categorías, proveedores y pedidos (CRUD), ejemplo:


<img width="495" alt="2" src="https://github.com/vfloressduoc/Ludoteca_Grupo4/assets/145572948/2636642f-eee6-42a6-baa9-ea5eb10b89cf">



