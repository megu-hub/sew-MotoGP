<?php
session_start();

$errorFormulario = false;

$errorValor       = "";
$errorCompleta    = "";
$errorDispo       = "";
$errorComentario  = "";
$errorMejoras     = "";

$formularioPOST  = "";


// Si se envía el formulario
if (count($_POST) > 0) {   

    $formularioPOST = $_POST;

    if(empty($_POST["valoracion"])){
        $errorValor = " * La valoración es obligatoria";
        $errorFormulario = true;
    }

    if(empty($_POST["completada"])){
        $errorCompleta = " * Debe indicar si completó la prueba";
        $errorFormulario = true;
    }

    if(empty($_POST["opcion"])){
        $errorDispo = " * Seleccione un dispositivo";
        $errorFormulario = true;
    }

    if(empty(trim($_POST["comentario"]))){
        $errorComentario = " * Escriba algún comentario";
        $errorFormulario = true;
    }

    if(empty(trim($_POST["mejoras"]))){
        $errorMejoras = " * Escriba posibles mejoras";
        $errorFormulario = true;
    }
}
if ($errorFormulario) {
        echo "<h4>Formulario NO PROCESADO en el servidor</h4>";
}

if ($formularioPOST && $errorFormulario == false) {

    $_SESSION["valoracion"]    = $_POST["valoracion"];
    $_SESSION["completada"]    = $_POST["completada"];
    $_SESSION["opcion"]        = $_POST["opcion"];
    $_SESSION["comentario"]    = $_POST["comentario"];
    $_SESSION["mejoras"]       = $_POST["mejoras"];

    // Si quieres redirigir:
    header("Location: observacion.php");
    exit();
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

<header>
    <h1>Evaluación de usabilidad de MotoGP-Desktop</h1>
</header>

<main>

    <h2>Preguntas finales</h2>

    <form action="#" method="post" name="formulario">

        <p>Valoración (0 - 10):</p>
        <p>
            <input type="number" name="valoracion" min="0" max="10"/>
            <span><?php echo $errorValor; ?></span>
        </p>

        <p>¿Completada?</p>
        <p>
            <input type='radio' name='completada' value='si'/> Sí
            <input type='radio' name='completada' value='no'/> No   
            <span><?php echo $errorCompleta; ?></span>
        </p>

        <p>Dispositivo:</p>
        <p>
            <select name='opcion'>
                <option value="">Seleccione</option>
                <option value='ordenador'>Ordenador</option>
                <option value='tablet'>Tablet</option>
                <option value='movil'>Móvil</option>
            </select>
            <span><?php echo $errorDispo; ?></span>
        </p>

        <p>Comentarios:</p>
        <p>
            <textarea name='comentario' rows='5' cols='40'></textarea>
            <span><?php echo $errorComentario; ?></span>
        </p>

        <p>Mejoras:</p>
        <p>
            <textarea name='mejoras' rows='5' cols='40'></textarea>
            <span><?php echo $errorMejoras; ?></span>
        </p>

        <p>
            <input type='submit' value='Enviar' />
        </p>

    </form>

</main>

</body>
</html>
