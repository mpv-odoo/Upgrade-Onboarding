# coding: utf-8
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    deliveries_generated = fields.Boolean(string='Delivery Generated', readonly=True)
    state = fields.Selection(selection_add=[
        ('deliveries_gen', 'Deliveries Generated'), ('done',)
    ])

    def _action_confirm(self):
        '''
        (Overridden) Inherited to that we can stop the picking for Ecommerce 
        orders.
        '''
        if not (self.website_id or self._context.get('skip_amazon_orders')):
            super(SaleOrder, self)._action_confirm()
            self.sudo().write({'deliveries_generated': True})

    def generate_deliveries(self):
        '''
        (New) Button that will generate the deliveries for order made through
        Amazon or Ecommerce.
        '''
        self.ensure_one()
        if self.state not in ['sale', 'done']:
            raise UserError(_("You can not create picking in the current state:  %s !" % self.state))
        '''Call method that makes the procurement and then the picking.'''
        self.order_line._action_launch_stock_rule()
        self.sudo().write({
            'deliveries_generated': True,
            'state': 'deliveries_gen'
        })


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_type', 'product_uom_qty', 'qty_delivered', 'state', 'move_ids', 'product_uom')
    def _compute_qty_to_deliver(self):
        '''
        (Overridden) Inherited the compute to show the visibility of the
        inventory widget all the time.
        '''
        for line in self:
            line.qty_to_deliver = line.product_uom_qty - line.qty_delivered
            line.display_qty_widget = line.product_type == 'product' and line.product_uom

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        '''
        (Overridden) If 'skip_amazon_orders' is in the context, don't generate 
        the deliveries for amazon orders
        '''
        if self._context.get('skip_amazon_orders'):
            self = self.filtered(lambda l: not l.order_id.amazon_order_ref)
        return super(SaleOrderLine, self)._action_launch_stock_rule(previous_product_uom_qty)
