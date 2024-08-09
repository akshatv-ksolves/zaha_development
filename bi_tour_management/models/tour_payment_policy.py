# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _

class tour_payment_policy(models.Model):
	
    _name = "tour.payment.policy"
    _description = "Tour Payment Policy"

    name = fields.Char('Policy Name')
    before_book_date_perc = fields.Integer('Payment Percentage Before Booking Date ')
    before_pay_date_perc = fields.Integer('Payment Percentage After Booking Date', compute='set_value', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.depends('before_book_date_perc')
    def set_value(self):
        for each in self:
            each.before_pay_date_perc = 100 - each.before_book_date_perc

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: