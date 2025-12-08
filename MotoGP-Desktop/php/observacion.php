<?php
session_start();

$errorFormulario = false;

$errorNombre     = "";

$formularioPOST  = "";

if (count($_POST)>0) 
    {   
        $formularioPOST  = $_POST;

        if($_POST["comentario"] == ""){
            $errorNombre = " * Escriba un comentario ";
            $errorFormulario = true;
        }

    }

if ($formularioPOST) {

    if ($errorFormulario == true){
         echo "<h4>Formulario NO PROCESADO en el servidor</h4>";
    }
    else {
        $host = 'localhost';
        $user = 'DBUSER2025';
        $pass = 'DBPSWD2025';
        $dbname = 'UO299971_DB';

        $db = new mysqli($host, $user, $pass, $dbname);
        header("Location: ../index.html");
        exit();
    }

}


?>
<!DOCTYPE HTML>
<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />
    <title>MotoGP-Juegos</title>
	
	<meta name="keywords" content="Moto, MotoGP" />
	<meta name="author" content = "Clara Fernández" />
	<meta name = "description" content = "Formulario para pruebas de usabilidad" />
	<meta name = "viewport" content = "width=device-width, initial-scale=1.0" />
	<link rel="icon" href="multimedia/icono.ico"/>
	<link rel="stylesheet" type="text/css" href="../estilo/estilo.css" />
	<link rel="stylesheet" type="text/css" href="../estilo/layout.css" />

</head>

<body>
    <!-- Datos con el contenidos que aparece en el navegador -->
    <header>
        
        <h1>Test de usabilidad de MotoGP-Desktop</h1>
    </header>
    <main>
        
        <h2>Observaciones del desarrollador</h2>
        <form action='#' method='post' name='formulario'>

            <p>Comentarios</p>
            <p>
                <textarea name='comentario' rows='5' cols='40'>
                </textarea>
            </p>
            
            <p>
                <input type='submit' value='Finalizar prueba'/>
            </p>
        </form>
    
    
    </main>

</body>
</html>

