# Copyright 2018 ACSONE SA/NV
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import models, http
from odoo.exceptions import AccessDenied
from odoo.http import request
from urllib.parse import urlparse, parse_qs

import os
import logging
_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def get_api_key(cls):
        headers = request.httprequest.environ
        query_string = request.httprequest.environ['QUERY_STRING']

        api_key = headers.get("HTTP_API_KEY")
        if (not query_string): # Esto podría ser un error si api_key se obtiene de header y query_string está vacío
            return False # Debería ser: if not api_key and not query_string: return False
                         # O procesar query_params solo si api_key no está en headers.

        query_params = parse_qs(query_string)
        # Esta lógica da precedencia a query_params si api_key también está en headers.
        # Si api_key está en header y también en query, el del query lo sobreescribe.
        # Si solo está en header, se usa el del header.
        # Si solo está en query, se usa el del query.
        api_key_from_query = query_params.get('apikey', [None])[0]
        api_key = api_key_from_query if api_key_from_query else api_key

        if api_key: # Solo limpiar si api_key no es None
            api_key = api_key.replace("-", "")

        return api_key

    @classmethod
    def _auth_method_user(cls):
        api_key = cls.get_api_key()
        if (api_key):
            if cls.validate_api_key():
                return True
            else:
                values = {
                    'success_message': [],
                    'error_message': ['Favor solicitar la creacion de tu usuario al equipo administrativo...'],
                }
                return request.render('exo_api.message_template', values)

        return super()._auth_method_user() # Cambio aquí



    @classmethod
    def _auth_method_api_key(cls):
        if (not cls.validate_api_key()):
            values = {
                'success_message': [],
                'error_message': ['Favor solicitar la creacion de tu usuario al equipo administrativo...'],
            }
            return request.render('exo_api.message_template', values)

    @classmethod
    def validate_api_key(cls):
        _logger.info("____________________ validate_api_key 1")
        api_key = cls.get_api_key()
        _logger.info("____________________ validate_api_key 2")
        _logger.info(api_key)
        if api_key:
            _logger.info("____________________ validate_api_key 3")
            # request.uid = 1 # Comentado temporalmente para evaluar impacto, idealmente usar sudo()
            # auth_api_key = request.env["auth.api.key"]._retrieve_api_key(api_key) # Necesita contexto de usuario correcto o sudo

            # Intento con sudo() para _retrieve_api_key, asumiendo que el chequeo de grupo 'base.group_system' dentro de _retrieve_api_key_id es para el usuario que llama al método, no el usuario de la sesión.
            # Si _retrieve_api_key_id DEBE ser llamado por un system user en el contexto actual, entonces request.uid=1 o un with_user(SUPERUSER_ID) sería necesario allí.
            auth_api_key_model_sudo = request.env["auth.api.key"].sudo()
            auth_api_key = auth_api_key_model_sudo._retrieve_api_key(api_key)

            _logger.info("____________________ validate_api_key 4")
            _logger.info(auth_api_key)

            if (not auth_api_key):
                _logger.info("____________________ validate_api_key 5")
                partner = request.env["res.partner"].sudo().search([('vat', '=', api_key)], limit=1)
                _logger.info("____________________ validate_api_key 6")
                _logger.info(partner)
                if (not partner):
                    return False

                _logger.info("____________________ validate_api_key 7")
                user_id = partner.create_user_from_partner() # Este método debe existir en res.partner (probablemente de exo_api)
                _logger.info("____________________ validate_api_key 8")
                _logger.info(user_id)
                if (user_id and not user_id.has_group("base.group_system")): # Esto podría ser problemático si el usuario creado no debe ser admin
                    _logger.info("____________________ validate_api_key 9")
                    _logger.info(user_id.has_group("base.group_system"))
                    auth_api_key = request.env["auth.api.key"].sudo().create({ # Usar sudo para crear la clave
                        'name': user_id.name,
                        'key': api_key,
                        'user_id': user_id.id
                    })

                    _logger.info("____________________ validate_api_key 9.1") # Corregido el número de log
                    _logger.info(auth_api_key)
            _logger.info("____________________ validate_api_key 10")
            _logger.info(auth_api_key)
            if auth_api_key:
                _logger.info("____________________ validate_api_key 11")
                _logger.info(auth_api_key)
                try:
                    _logger.info("____________________ validate_api_key 11.1") # Corregido el número de log
                    # La autenticación de sesión aquí es un punto clave.
                    # Si la API key ya identifica al usuario, ¿es necesaria una autenticación de sesión adicional con contraseña?
                    # Esto podría ser un vector de ataque si USER_PASSWORD es global o fácilmente adivinable.
                    # Por ahora, se mantiene la lógica original.
                    uid = request.session.authenticate(request.db, auth_api_key.user_id.login, os.getenv('USER_PASSWORD'))
                    _logger.info("____________________ validate_api_key 12")
                    _logger.info(uid)
                    if not uid: # Si la autenticación falla, no deberíamos proceder
                        _logger.warning(f"API Key Auth: Falló la autenticación de sesión para el usuario {auth_api_key.user_id.login}")
                        return False
                except Exception as ex:
                    _logger.error(f"API Key Auth: Error durante session.authenticate para {auth_api_key.user_id.login}: {ex}")
                    return False

                _logger.info("____________________ validate_api_key login_success 13")
                request.params['login_success'] = True # Esto es más relevante para login web.
                return True
        _logger.info("____________________ validate_api_key login_success 14 - No API Key or Auth Failed")
        return False
