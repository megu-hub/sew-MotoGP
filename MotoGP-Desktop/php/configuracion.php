<?php
    session_start();
    class Configuracion {
        private $db;
        function init(){
            $host = 'localhost';
            $user = 'DBUSER2025';
            $pass = 'DBPSWD2025';
            $dbname = 'UO299971_DB';

            $conn = new mysqli($host, $user, $pass, $dbname);

            if ($conn->connect_error) {
                die("Conexión fallida: " . $conn->connect_error);
            }
        }
        
        function exportarCSV(){
            $tablesResult = $conn->query("SHOW TABLES");
            while ($row = $tablesResult->fetch_array()) {
                $table = $row[0];
                
                $result = $conn->query("SELECT * FROM `$table`");
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
    }
?>