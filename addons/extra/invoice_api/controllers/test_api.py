from odoo import http
from odoo.http import Response
import json

class MiControlador(http.Controller):

    @http.route(['/api/test', '/api/example'], type='http', auth='none', methods=['GET'], csrf=False)
    def manejar_rutas(self, **kwargs):
        respuesta = {
            'estado': 'éxito',
            'mensaje': '¡Conexión exitosa sin sesión! 🚀'
        }

        # Desactivamos cache de sesión con encabezados mínimos
        headers = [
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'no-store'),
            ('Pragma', 'no-cache'),
        ]

        return Response(
            json.dumps(respuesta),
            headers=headers,
            status=200
        )

