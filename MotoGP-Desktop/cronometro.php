<?php
session_start();

class Cronometro {
    private $tiempo;
    protected $inicio = 0;

    public function __construct(){
        $this->tiempo = 0;
    }

    public function arrancar(){
        if ($this->inicio == 0) {
            $this->inicio = microtime(true);
        }
    }

    public function parar(){
        if ($this->inicio != 0) {
            $this->tiempo += microtime(true) - $this->inicio;
            $this->inicio = 0;
        }
    }

    public function mostrar(){
        $total = $this->tiempo;

        if ($this->inicio != 0) {
            $total += microtime(true) - $this->inicio;
        }

        $min = floor($total / 60);
        $seg = floor($total) % 60;
        $ms = floor(($total - floor($total)) * 1000); 

        return sprintf("%02d:%02d:%01d", $min, $seg, $ms);
    }
}


if (!isset($_SESSION['cronometro'])) {
    $_SESSION['cronometro'] = new Cronometro();
}
$mostrarTiempo = "";

if ($_POST) {
    $miCronometro = $_SESSION['cronometro']; 

    if (isset($_POST['botonArrancar'])) $miCronometro->arrancar();
    if (isset($_POST['botonParar'])) $miCronometro->parar();
    if (isset($_POST['botonMostrar'])) {
        $mostrarTiempo = $miCronometro->mostrar();
    }

    $_SESSION['cronometro'] = $miCronometro;
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
	<meta name = "description" content = "Información de los juegos" />
	<meta name = "viewport" content = "width=device-width, initial-scale=1.0" />
	<link rel="icon" href="multimedia/icono.ico"/>
	<link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
	<link rel="stylesheet" type="text/css" href="estilo/layout.css" />
    <script src="js/cronometro.js"></script>
</head>

<body>
    <!-- Datos con el contenidos que aparece en el navegador -->
	<header>
    <h1><a href="index.html" title="Inicio"></a>MotoGP Desktop</h1>
	<nav>
	<a href="index.html" title="Inicio">Inicio</a>
	<a href="piloto.html" title="Información del Marco Bezzecchi">Piloto</a>
	<a href="circuito.html" title="Información del circuito">Circuito</a>
	<a href="meteorologia.html" title="Información de la meteorología">Meteorología</a>
	<a href="clasificaciones.php" title="Información de las clasificaciones">Clasificaciones</a>
	<a href="juegos.html" title="Información de juegos" class="active">Juegos</a>
	<a href="ayuda.html" title="Información de Ayuda">Ayuda</a>
	</nav>
	</header>
    <p>Estás en:
	<a href="index.html" title="Inicio">Inicio</a> >> <a href="juegos.html" title="Juegos">Juegos</a> >> <strong>Cronómetro PHP</strong>
	</p>

    <main>

    <form action="#" method="post" name="botones">
        <section>
            <h3>Pulse un botón</h3>
            <?php if ($mostrarTiempo !== "") echo "<p>$mostrarTiempo</p>"; ?>
            <input type="submit" class="button" name="botonArrancar" value="Arrancar"/>
            <input type="submit" class="button" name="botonParar" value="Parar"/>
            <input type="submit" class="button" name="botonMostrar" value="Mostrar"/>
        </section>
        
    </form>
    
    </main>

		
	


</body>
</html>