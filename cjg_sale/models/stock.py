from odoo import fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    box_count = fields.Float(related='sale_line_id.box_count')
    total_box_count = fields.Integer(related='group_id.sale_id.total_box_count')
    package_count = fields.Integer(related='sale_line_id.package_count')
    total_package_count = fields.Integer(related='group_id.sale_id.total_package_count')
