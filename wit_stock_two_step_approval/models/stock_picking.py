# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    state = fields.Selection(selection_add=[("recount", "Recount"), ('recount_done', 'Recount Done'), ("done", )])
    first_validation_by = fields.Many2one(string="First Count By", comodel_name="res.users", readonly=True, copy=False)
    recount_by = fields.Many2one(string="Recounted By", comodel_name="res.users", readonly=True, copy=False)
    second_validation_by = fields.Many2one( string="Final Validation By", comodel_name="res.users", readonly=True, copy=False)

    @api.depends("state")
    def _compute_show_validate(self):
        super()._compute_show_validate()
        for picking in self.filtered(lambda p: p.picking_type_code == 'incoming'):
            if picking.state == "recount_done":
                picking.show_validate = self.env.user.has_group(
                    "purchase.group_purchase_user")
            if picking.state == "recount":
                picking.show_validate = True

    def button_validate(self):
        res = super().button_validate()
        if res is not True or self.picking_type_code != 'incoming':
            return res
        if self.env.user.has_group("purchase.group_purchase_user"):
            self._send_notification_email(
                "wit_stock_two_step_approval.wit_mail_template_receipt_validation_sale"
            )
            self.second_validation_by = self.env.user
            return res
        else:
            raise AccessError(_("You do not have permission to do this. Please contact the Purchase user."))

    def _pre_action_done_hook(self):
        if self.state not in ['recount', 'recount_done', 'done'] \
                            and self.picking_type_code == 'incoming':
            self.mapped("move_lines").set_done_first_to_done()
            self.first_validation_by = self.env.user
            self._send_notification_email(
                "wit_stock_two_step_approval.wit_mail_template_receipt_validation_purchase"
            )
            self.state = "recount" if any(self.mapped("move_lines.recount")) else "recount_done"
            return False
        if self.state == 'recount' and self.picking_type_code == 'incoming':
            self.recount_by = self.env.user
            self.state = 'recount_done'
            return False
        return super()._pre_action_done_hook()

    def _send_notification_email(self, template_xml):
        template = self.env.ref(template_xml)
        for picking in self:
            template.send_mail(picking.id,
                               notif_layout="mail.mail_notification_light",
                               force_send=True)
            picking.message_post(body='Email sent.')

    def reset_done_quantities(self):
        self.mapped("move_lines").reset_quantity()
        if not any(self.mapped("move_lines.recount")):
            self.state = 'recount_done'


class StockMove(models.Model):
    _inherit = "stock.move"

    quantity_done_first = fields.Float( string="Quantity Done First", digits="Product Unit of Measure", readonly=True, copy=False)
    recount = fields.Boolean(string="Recount", compute="_compute_recount")

    @api.depends('quantity_done_first', 'product_uom_qty')
    def _compute_recount(self):
        for move in self:
            move.recount = move.quantity_done_first not in [move.product_uom_qty, 0]

    def set_done_first_to_done(self):
        for move in self:
            move.quantity_done_first = move.quantity_done

    def reset_quantity(self):
        for move in self.filtered(lambda m: m.recount):
            move.quantity_done = 0
