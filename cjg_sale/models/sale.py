from odoo import fields, models, api


class Sale(models.Model):
    _inherit = 'sale.order'

    total_box_count = fields.Integer(compute='_compute_packaging_total', string='Total Box Count')
    total_package_count = fields.Integer(compute='_compute_packaging_total', string='Total Package Count')

    @api.depends('order_line', 'order_line.box_count', 'order_line.package_count')
    def _compute_packaging_total(self):
        for order in self:
            order.total_box_count = sum(order.order_line.mapped('box_count'))
            order.total_package_count = sum(order.order_line.mapped('package_count'))
