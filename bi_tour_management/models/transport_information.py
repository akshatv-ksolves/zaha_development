# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _

class transport_information(models.Model):

    _name = "transport.information"
    _description = "Transport Information"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Not Available'),
        ],string="Status", default="draft")
    name = fields.Char("Transport Name" )
    partner_id = fields.Many2one('res.partner','Service Provider', required=True)
    transport_type_info_ids =fields.One2many("transport.type.info", 'transport_info_id','Transport Type Line')
    transport_recv_acc =fields.Many2one("account.account")
    transport_payble_acc = fields.Many2one('account.account')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.onchange('partner_id')
    def onchange_service_provider(self):
        for rec in self:
            rec.name=rec.partner_id.name

    def button_confirm(self):
        for rec in self:
            rec.state = 'confirm'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: