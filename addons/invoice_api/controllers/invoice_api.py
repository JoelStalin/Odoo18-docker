from odoo import http
from odoo.http import request
from datetime import datetime
import base64
import logging

_logger = logging.getLogger(__name__)

class InvoiceAPI(http.Controller):

    @http.route('/api/customer_invoice', auth='public', type='json', methods=['POST'], csrf=False)
    def create_customer_invoice(self, **kwargs):
        _logger.info("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥[API] Llamada recibida para crear factura 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")

        data = request.jsonrequest
        _logger.debug(f"📦 Payload recibido: {data}")

        partner_data = data.get('partner')
        invoice_date = data.get('invoice_date')
        lines_data = data.get('lines', [])

        # Buscar o crear el cliente
        partner = request.env['res.partner'].sudo().search([('vat', '=', partner_data['rnc'])], limit=1)
        if not partner:
            _logger.info(f"👤 Cliente no encontrado. Creando nuevo: {partner_data['name']}")
            partner = request.env['res.partner'].sudo().create({
                'name': partner_data['name'],
                'vat': partner_data['rnc'],
                'customer_rank': 1,
            })

        # Preparar líneas de factura
        invoice_lines = []
        for line in lines_data:
            _logger.debug(f"🔍 Buscando producto: {line['name']} ({line['code']})")
            product = request.env['product.product'].sudo().search([
                '|',
                ('default_code', '=', line['code']),
                ('name', '=', line['name'])
            ], limit=1)

            if not product:
                _logger.info(f"📦 Producto no encontrado. Creando: {line['name']}")
                product = request.env['product.product'].sudo().create({
                    'name': line['name'],
                    'default_code': line['code'],
                    'lst_price': line['price'],
                    'type': 'product',
                })

            invoice_lines.append((0, 0, {
                'product_id': product.id,
                'quantity': line['quantity'],
                'price_unit': line['price'],
                'load_id': line.get('load', {}).get('loadId'),
                'load_number': line.get('load', {}).get('loadNumber'),
            }))

        _logger.info("🧾 Creando factura...")
        invoice = request.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': invoice_date,
            'invoice_line_ids': invoice_lines,
        })

        invoice.action_post()
        _logger.info(f"✅ Factura creada y publicada: {invoice.name}")

        journal = request.env['account.journal'].sudo().search([('type', '=', 'bank')], limit=1)
        _logger.info(f"💳 Registrando pago en diario: {journal.name}")

        payment_register = request.env['account.payment.register'].with_context(active_ids=invoice.ids).sudo().create({
            'payment_date': invoice.invoice_date,
            'amount': invoice.amount_total,
            'journal_id': journal.id,
        })
        payment_register._create_payments()

        _logger.info("📄 Generando PDF de la factura...")
        pdf_content = request.env.ref('account.account_invoices').sudo()._render_qweb_pdf([invoice.id])[0]

        attachment = request.env['ir.attachment'].sudo().create({
            'name': f"{invoice.name}.pdf",
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'account.move',
            'res_id': invoice.id,
            'mimetype': 'application/pdf',
        })

        # Generar token de acceso público
        attachment.generate_access_token()

        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        pdf_url = f"{base_url}/web/content/{attachment.id}?access_token={attachment.access_token}"

        return {
            'status': 'success',
            'invoice_id': invoice.id,
            'invoice_number': invoice.name,
            'pdf_url': pdf_url,
        }
