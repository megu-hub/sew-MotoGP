<?php
session_start();

$errorFormulario = false;

// Variables de errores para cada pregunta
$error1 = $error2 = $error3 = $error4 = $error5 = "";
$error6 = $error7 = $error8 = $error9 = $error10 = "";

$formularioPOST = "";

// Validación del formulario
if (count($_POST) > 0) {   

    $formularioPOST = $_POST;

    if (empty($_POST["pregunta1"])) {
        $error1 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta2"])) {
        $error2 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta3"])) {
        $error3 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta4"])) {
        $error4 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta5hora"])) {
        $error5 = " * La hora es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta5minutos"])) {
        $error5 = " * Los minutos son obligatorios";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta6"])) {
        $error6 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta7"])) {
        $error7 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta8"])) {
        $error8 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta9"])) {
        $error9 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }

    if (empty($_POST["pregunta10"])) {
        $error10 = " * Esta pregunta es obligatoria";
        $errorFormulario = true;
    }
}

if ($formularioPOST) {

    if ($errorFormulario) {
        echo "<h4>Formulario NO PROCESADO en el servidor</h4>";
    } else {
        header("Location: resultado.php");
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

<header>
    <h1>Test de usabilidad de MotoGP-Desktop</h1>
</header>

<main>

    <h2>Preguntas de MotoGP-Desktop</h2>

    <form action="#" method="post" name="formulario">

        <p>1. ¿Qué es el control de tracción?</p>
        <textarea name='pregunta1' rows='3' cols='80'></textarea>
        <span><?php echo $error1; ?></span>

        <p>2. ¿Cuántas fotografías hay en la sección de piloto?</p>
        <input type="number" name="pregunta2" min = "0"/>
        <span><?php echo $error2; ?></span>

        <p>3. ¿Cuántas cartas hay en el juego de memoria?</p>
        <input type="number" name="pregunta3" min = "0"/>
        <span><?php echo $error3; ?></span>

        <p>4. ¿Cuántos botones tiene el cronómetro?</p>
        <input type="number" name="pregunta4" min = "0"/>
        <span><?php echo $error4; ?></span>

        <p>5. ¿A qué hora comenzó la carrera en Termas del Rio Hondo?</p>
        <input type="number" name="pregunta5hora" min = "0" max="23"/>:<input type="number" name="pregunta5minutos" min = "0" max="60"/>
        <span><?php echo $error5; ?></span>

        <p>6. ¿Para cuántos días de entreno se muestra su meteorología?</p>
        <input type="number" name="pregunta6"/>
        <span><?php echo $error6; ?></span>

        <p>7. ¿Cuántas referencias se encuentran en la sección del circuito?</p>
        <input type="number" name="pregunta7"/>
        <span><?php echo $error7; ?></span>

        <p>8. ¿Quién quedó primero de los clasificados de la carrera?</p>
        <input type="text" name="pregunta8"/>
        <span><?php echo $error8; ?></span>

        <p>9. ¿Cuál es la localidad más próxima al circuito Termas del Rio Hondo?</p>
        <input type="text" name="pregunta9"/>
        <span><?php echo $error9; ?></span>

        <p>10. ¿Cuántas entradas hay en la sección de ayuda?</p>
        <input type="number" name="pregunta10"/>
        <span><?php echo $error10; ?></span>

        <p>
            <input type="submit" value="Terminar prueba"/>
        </p>

    </form>

</main>
</body>
</html>
