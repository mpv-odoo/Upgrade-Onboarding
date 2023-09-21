from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    case_pack = fields.Integer(related='product_id.case_pack')
    box_count = fields.Float(compute='_compute_box', string='Box Count', default=0, store=True)
    box_price = fields.Float(compute='_compute_box', string='Box Price')
    package_count = fields.Integer(compute='_compute_package_count', string='Package Count', default=0, store=True)

    @api.depends('product_uom_qty', 'product_id.case_pack','price_unit')
    def _compute_box(self):
        for record in self:
            if record.product_id.case_pack:
                record.box_count = record.product_uom_qty / record.product_id.case_pack
            record.box_price = record.price_unit * record.product_id.case_pack

    @api.depends('product_uom_qty', 'product_packaging_id.qty')
    def _compute_package_count(self):
        for record in self.filtered(lambda sol: sol.product_packaging_id.qty):
                record.package_count = record.product_uom_qty / record.product_packaging_id.qty
