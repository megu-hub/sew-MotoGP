<?php
session_start();

class Clasificacion {
    private $documento;

    public function __construct() {
        $this->documento = "xml/circuitoEsquema.xml";
    }

    public function consultar() {

        $datos = file_get_contents($this->documento);

        $xml = new SimpleXMLElement($datos);

        // Verificar que exista <clasificados>
        if (isset($xml->clasificados)) {
            echo "<h3>Clasificados:</h3><ul>";
            foreach ($xml->clasificados->clasificado as $item) {
                echo "<li>" . htmlentities($item) . "</li>";
            }
            echo "</ul>";
        } else {
            echo "<p>No existe el elemento &lt;clasificados&gt; en el XML.</p>";
        }
    }
}

$clasif = new Clasificacion();
?>



<!DOCTYPE HTML>

<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />
    <title>MotoGP-Clasificaciones</title>
	
	<meta name="keywords" content="Moto, MotoGP" />
	<meta name="author" content = "Clara Fernández" />
	<meta name = "description" content = "Información de las clasificaciones" />
	<meta name = "viewport" content = "width=device-width, initial-scale=1.0" />
	<link rel="icon" href="multimedia/icono.ico"/>
	<link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
	<link rel="stylesheet" type="text/css" href="estilo/layout.css" />
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
	<a href="clasificaciones.html" title="Información de las clasificaciones" class="active">Clasificaciones</a>
	<a href="juegos.html" title="Información de juegos">Juegos</a>
	<a href="ayuda.html" title="Información de Ayuda">Ayuda</a>
	</nav>
	</header>
	<p>Estás en:
	<a href="index.html" title="Inicio">Inicio</a> >> <strong>Clasificaciones</strong>
	</p>

	<main>
	<h2>Clasificaciones de MotoGP-Desktop</h2>

    <?php
        $clasif->consultar();
    ?>
	</main>
</body>
</html>