<?php
    session_start();
    class Configuracion {
        private $db;
        
        function init(){
            $host = 'localhost';
            $user = 'DBUSER2025';
            $pass = 'DBPSWD2025';
            $dbname = 'UO299971_DB';

            $db = new mysqli($host, $user, $pass, $dbname);

            if ($db->connect_error) {
                die("Conexión fallida: " . $db->connect_error);
            }
        }
        
        function exportarCSV(){
            $tablesResult = $db->query("SHOW TABLES");
            while ($row = $tablesResult->fetch_array()) {
                $table = $row[0];
                
                $result = $db->query("SELECT * FROM `$table`");
                $numFields = $result->field_count;

                $filename = $table . ".csv";
                $fp = fopen($filename, 'w');

                $headers = [];
                while ($fieldInfo = $result->fetch_field()) {
                    $headers[] = $fieldInfo->name;
                }
                fputcsv($fp, $headers);

                while ($rowData = $result->fetch_assoc()) {
                    fputcsv($fp, $rowData);
                }

                fclose($fp);
            }

        }

        // elimina la db, tablas y datos relacionados
        function eliminarDB(){
            $sql= "DROP DATABASE UO299971_DB";
            $db->query($sql);

        }
        
        // reinicia la base de datos, borra todos los datos de la db
        function reiniciarDB(){
            $tables = ['usuarios', 'resultados', 'observaciones'];
            foreach ($tables as $table) {
                $db->query("TRUNCATE TABLE $table");
            }
        }

        function importarCSV(){
            
        }
    }
?>