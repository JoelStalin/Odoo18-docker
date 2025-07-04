from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    load_id = fields.Char(string="Load ID")
    load_number = fields.Char(string="Load Number")
