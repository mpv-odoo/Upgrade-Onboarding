from odoo import fields, models

class Product(models.Model):
    _inherit = 'product.template'

    case_pack = fields.Integer(string='Case Pack') 
