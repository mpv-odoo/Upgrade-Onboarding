# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        if res is not True or self.picking_type_code != 'incoming':
            return res
        # Create a new landed cost record in draft mode.
        landed_cost_product = self.env.ref('wit_stock_landed_cost.wit_product_landed_cost')
        accounts_data = landed_cost_product.product_tmpl_id.get_product_accounts()
        landed_cost = self.env['stock.landed.cost'].create({
            'picking_ids': [(6, 0, self.ids)],
            'cost_lines': [(0, 0, {
                'product_id': landed_cost_product.id,
                'split_method': landed_cost_product.product_tmpl_id.split_method_landed_cost or 'equal',
                'name': landed_cost_product.name or '',
                'price_unit': landed_cost_product.standard_price or 0.0,
                'account_id': accounts_data['stock_input'].id
            })]
        })
        msg_body = _("The landed cost <a href=# data-oe-model=stock.landed.cost data-oe-id=%s>%s</a> has been created.",
                     landed_cost.id, landed_cost.name)
        self.message_post(body=msg_body)
        # Display the landed cost in a popup window.
        return {
            'name': _('Landed Cost'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.landed.cost',
            'target': 'new',
            'res_id': landed_cost.id
        }
