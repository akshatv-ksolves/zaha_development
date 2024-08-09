# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class tour_destination(models.Model):

    _name = "tour.destination"
    _description = "Tour Destination"

    name = fields.Char('Destination', required=True)
    code = fields.Char('Code',required=True)
    country_id = fields.Many2one('res.country','Country')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: