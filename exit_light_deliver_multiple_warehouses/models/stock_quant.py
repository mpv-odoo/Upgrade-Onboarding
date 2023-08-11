# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', compute='_compute_warehouse_id', store=True)

    @api.depends('location_id')
    def _compute_warehouse_id(self):
        '''
        (New) Getting the warehouse for the given location in quant.
        '''
        for rec in self:
            warehouse_id = rec.location_id.warehouse_id
            if warehouse_id:
                rec.warehouse_id = warehouse_id.id
