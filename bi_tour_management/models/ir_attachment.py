# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class ir_attachment(models.Model):
	
    _inherit = "ir.attachment"

    passport_book_id = fields.Many2one('passport.booking', 'passport Booking id')
    visa_book_id = fields.Many2one('visa.booking', 'Visa Booking id')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: