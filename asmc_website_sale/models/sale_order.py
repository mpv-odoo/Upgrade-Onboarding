# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import date, timedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_type = fields.Selection(
        [
            ("pickup", "Pick-Up"),
            ("ship", "Ship"),
        ],
        string="Type",
        compute="_compute_sale_type",
        store=True,
        readonly=False,
    )
    ship_pickup_date = fields.Date(string="Pick-Up/Ship Date")

    @api.depends("order_line")
    def _compute_sale_type(self):
        for record in self:
            res = False
            delivery_line = record.mapped("order_line").filtered(
                lambda r: r.product_id.categ_id.is_shipping
            )
            if delivery_line:
                carrier = self.env["delivery.carrier"].search(
                    [("product_id", "=", delivery_line[0].product_id.id)]
                )
                if carrier:
                    if carrier.is_pick_up:
                        res = "pickup"
                    else:
                        res = "ship"
            record.sale_type = res

    def get_non_shippable_products(self):
        for record in self:
            non_shippable_products = record.order_line.mapped("product_id").filtered(
                lambda r: r.is_shippable is False and r.type != "service"
            )
            return non_shippable_products if non_shippable_products else False

    def get_earliest_ship_pickup_date(self):
        for record in self:
            today = date.today()
            longest_lead_time = max(
                record.order_line.mapped("product_id")
                .mapped("categ_id")
                .mapped("lead_time")
            )
            earliest = today + timedelta(days=longest_lead_time)
            holidays = set(record.env["sale.holiday"].search([]).mapped("date"))
            buffer_days = 0

            for day_ord in range(today.toordinal(), earliest.toordinal() + 1):
                day = date.fromordinal(day_ord)

                # if any days within leadtime are holidays or Sundays
                if day in holidays or day.weekday() == 6:
                    buffer_days += 1

            earliest += timedelta(days=buffer_days)

            return earliest or today
