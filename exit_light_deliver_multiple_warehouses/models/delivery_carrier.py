# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    type = fields.Char(string='Delivery Type')

    '''
    (Overridden) Need to override the name get function to use the new field
    type as a workaround until there is a fix for the amazon shipping connector.
    '''

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, rec.type if rec.type else ''))
        return res
