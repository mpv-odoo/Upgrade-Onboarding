# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.product'

    '''
    (New) New public method to get the inventory amount per warehouse for the
    widget
    '''

    def get_stock_values_per_warehouse(self):
        self.ensure_one()
        return self.env['stock.warehouse'].search([]).mapped(
            lambda warehouse: {
                'id': warehouse.id,
                'name': warehouse.name,
                'qty_available': self.with_context(warehouse=warehouse.id).qty_available,
                'virtual_available': self.with_context(warehouse=warehouse.id).virtual_available,
                'free_qty': self.with_context(warehouse=warehouse.id).free_qty
            })
