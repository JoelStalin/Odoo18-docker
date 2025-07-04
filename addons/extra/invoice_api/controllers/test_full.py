from odoo import http, SUPERUSER_ID
import json

class PublicAPIController(http.Controller):

    # Ejemplo GET sin acceso a base de datos
    @http.route('/api/public', auth='none', type='http', methods=['GET'], csrf=False)
    def public_api_get(self, **kwargs):
        response_data = {
            "message": "¡Esta es una API pública!",
            "status": "success"
        }
        return http.Response(
            json.dumps(response_data),
            content_type='application/json; charset=utf-8',
            status=200
        )

    # Ejemplo POST con tipo JSON
    @http.route('/api/public/post', auth='none', type='json', methods=['POST'], csrf=False)
    def public_api_post(self, **post_data):
        return {
            "received_data": post_data,
            "status": "success"
        }

    # Ejemplo GET con acceso a base de datos
    @http.route('/api/public/items', auth='none', type='http', methods=['GET'], csrf=False)
    def get_public_items(self, **kwargs):
        try:
            if not request.db:
                raise Exception("Base de datos no especificada")
            
            env = request.env(user=SUPERUSER_ID, db=request.db)
            items = env['product.product'].search_read([], ['name', 'list_price'])
            
            return http.Response(
                json.dumps({"items": items}),
                content_type='application/json; charset=utf-8',
                status=200
            )
        except Exception as e:
            return http.Response(
                json.dumps({"error": str(e)}),
                content_type='application/json; charset=utf-8',
                status=500
            )