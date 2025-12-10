<?php
session_start();

$errorFormulario = false;

$errorID    = "";
$errorProf  = "";
$errorEdad  = "";
$errorGenero = "";
$errorInfo  = "";

$formularioPOST  = "";


//Solo se ejecutará si se han enviado los datos desde el formulario al pulsar el boton Enviar
if(count($_POST) > 0) {   
    $formularioPOST  = $_POST;

    if(empty($_POST["profesion"])){
        $errorProf = " * La profesión es obligatoria";
        $errorFormulario = true;
    }

    if(empty($_POST["edad"])){
        $errorEdad = " * La edad es obligatoria";
        $errorFormulario = true;
    }

    if(empty($_POST["genero"])) {
        $errorGenero = " * El género es obligatorio";
        $errorFormulario = true;
    }

    if(empty($_POST["informatica"])){
        $errorInfo = " * La pericia informática es obligatoria";
        $errorFormulario = true;
    }
}


if ($formularioPOST) {

    if ($errorFormulario == true){
        echo "<h4>Formulario NO PROCESADO en el servidor</h4>";
    }
    else{

        $_SESSION["profesion"]     = $_POST["profesion"];
        $_SESSION["edad"]          = $_POST["edad"];
        $_SESSION["genero"]        = $_POST["genero"];
        $_SESSION["informatica"]   = $_POST["informatica"];

        header("Location: preguntas.php");
        exit();
    }
}
?>
<!DOCTYPE HTML>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <title>MotoGP-Juegos</title>
    <link rel="stylesheet" type="text/css" href="../estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="../estilo/layout.css" />
</head>

<body>
<header><h1>Información del usuario para el test de usabilidad</h1></header>

<main>
    <h2>Información del usuario</h2>

    <form action="#" method="post" name="formulario">

        <p>Profesión:</p> 
        <p>
            <input type='text' name='profesion'/>
            <span><?php echo $errorProf; ?></span>
        </p>

        <p>Edad:</p>
        <p>
            <input type='number' name='edad'/>
            <span><?php echo $errorEdad; ?></span>
        </p>

        <p>Género:</p>
        <p>
            <input type='radio' name='genero' value='Hombre'/>Hombre
            <input type='radio' name='genero' value='Mujer'/>Mujer
            <input type='radio' name='genero' value='Otros'/>Otros    
            <span><?php echo $errorGenero; ?></span> 
        </p>

        <p>Pericia informática:</p>
        <p>
            <input type='radio' name='informatica' value='si'/>Sí
            <input type='radio' name='informatica' value='no'/>No
            <span><?php echo $errorInfo; ?></span>
        </p>

        <p>
            <input type='submit' value='Iniciar Prueba' />
        </p>
    </form>

</main>

</body>
</html>
