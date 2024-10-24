import psycopg2

class TemplateManager:
    def __init__(self):
        # Credenciales de conexión a la base de datos
        self.db_name = "raloy_productivo"
        self.db_user = "apps"
        self.db_password = "4pps_.Re4d0nly+"
        self.db_host = "10.150.4.190"
        self.db_port = "5432"

    def _connect(self):
        """Establece la conexión con la base de datos"""
        try:
            connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            return connection
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def fetch_template_suggestions(self, template_name):
        """Obtiene sugerencias de plantillas basadas en coincidencias parciales"""
        connection = self._connect()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            query = """
                SELECT DISTINCT ltt."name"
                FROM laboratory_template_tests ltt
                WHERE ltt."name" ILIKE %s
            """
            cursor.execute(query, ['%' + template_name + '%'])
            result_tuples = cursor.fetchall()
            return [{'name': row[0]} for row in result_tuples]

        except psycopg2.Error as e:
            print(f"Error al obtener sugerencias: {e}")
            return []

        finally:
            cursor.close()
            connection.close()

    def fetch_exact_template_data(self, template_name):
        """Obtiene los datos exactos de una plantilla seleccionada"""
        connection = self._connect()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            query = """
                SELECT ltt.id, ltt."name", ltr.t_numbers, lt."name" AS test_name, 
                       ltr.test_time, ltr.astmd, ltr.min_val, ltr.recurrent_val, 
                       ltr.max_val, ltr.val_result, ltr.price_unit
                FROM laboratory_template_tests ltt
                INNER JOIN laboratory_test_result ltr ON ltt.id = ltr.template_req_ref_id
                INNER JOIN laboratory_test lt ON lt.id = ltr.test_id
                WHERE ltt."name" = %s
            """
            cursor.execute(query, [template_name])
            result_tuples = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            result_dicts = [dict(zip(column_names, row)) for row in result_tuples]
            return result_dicts

        except psycopg2.Error as e:
            print(f"Error al obtener datos exactos: {e}")
            return []

        finally:
            cursor.close()
            connection.close()
