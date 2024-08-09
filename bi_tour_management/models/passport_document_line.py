# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class passport_document_line(models.Model):

    _name = "passport.document.line"
    _description = "Passport Document Line"

    passport_book_id = fields.Many2one('passport.booking', 'passport Booking id')
    document_type_id = fields.Many2one('document.management', 'Document Type', required = True)
    name = fields.Char('Xerox Copy/Photo Copy ', required = True)
    orignal_copy = fields.Integer('Original Copy ')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
class visa_document_line(models.Model):

    _name = "visa.document.line"
    _description = "Visa Document Line"
    _rec_name = 'name'

    passport_booking_id = fields.Many2one('passport.booking', 'passport Booking id',required=True,)
    customer_visa_id = fields.Many2one(string="Customer",related='visa_book_id.customer_id',store=True)

    visa_book_id = fields.Many2one('visa.booking', 'Visa Booking id')
    document_type_id = fields.Many2one('document.management', 'Document Type', required = True)
    name = fields.Char('Xerox Copy/Photo Copy ', required = True)
    orignal_copy = fields.Integer('Original Copy ')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: