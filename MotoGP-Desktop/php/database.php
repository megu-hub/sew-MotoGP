<?php 
    session_start();

    class Database{
        // clase para manejar las inserciones a las tablas

        private $db;

            function __construct(){
                $this->init();
            }
            
            function init(){
                $host = 'localhost';
                $user = 'DBUSER2025';
                $pass = 'DBPSWD2025';
                $dbname = 'UO299971_DB';

                this->$db = new mysqli($host, $user, $pass, $dbname);

                if ($db->connect_error) {
                    die("Conexión fallida: " . $db->connect_error);
                }
            }

            function insertarDatos($query){
                $preparedQuery = $this->db->prepare($query);
                $preparedQuery -> execute();
                $preparedQuery -> close();
                this->$db->close();
            }

            function __destruct() {
                $this->db->close();
            }
} 