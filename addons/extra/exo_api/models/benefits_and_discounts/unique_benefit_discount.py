from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UniqueBenefitDiscount(models.Model):
    _name = "unique.benefit.discount"
    _description = 'Beneficios y/o descuentos de Una Sola Vez'

    
     
    def _domain_transportist(self):
        return []

    name = fields.Text(string = 'Razón o comentario', required=True)
    product_tmpl_id = fields.Many2one('product.template', string="Producto de Referencia", required=True)
    product_quantity = fields.Integer("Cantidad", default=1, required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string="Cuenta Analítica", required=False)
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    amount = fields.Float("Precio Producto",  required=True, tracking=True)
    transaction_type = fields.Selection([('debit', 'Debito'), ('credit', 'Credito')], string="Tipo de Transacción", default='credit', required=True)
    move_line_id = fields.Many2one('account.move.line', string="Linea del Movimiento")     
    is_check = fields.Boolean(string='aprobacion', default=False)
    transaction_date = fields.Datetime(string="Transaction Date", required=True, default=fields.Datetime.today)
    transaction_ids = fields.One2many('unique.benefit.transaction', 'discount_id', string="Transactions" )
    carrier_ids = fields.Many2one('discount.carrier', string="Transportista")
    
    # 🆕 Fecha de factura (vía línea de asiento contable)
    invoice_date = fields.Date(
        string="Fecha de Factura",
        related="move_line_id.move_id.invoice_date",
        store=True,
        readonly=True
    )

    # 🆕 ID de carga asociada
    load_id = fields.Many2one('discount.load', string="Carga")
    
    @api.onchange("product_tmpl_id")
    def _onchange_product_tmpl_id(self):
        for record in self:
            record.amount = record.product_tmpl_id.list_price
            record.product_quantity = 1
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_autogenerated(self):
        for record in self:
            if record.move_line_id:
                raise ValidationError("Este registro ya fue utilizado por lo cual no permite la eliminación. Debe borrar la factura si aún se encuentra en borrador")
    
    def action_mark_as_checked(self):
       for record in self:
           record.is_check = True
    