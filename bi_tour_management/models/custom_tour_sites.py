# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class custom_tour_sites(models.Model):
	
    _name = "custom.tour.sites"
    _description = "Custom Tour Sites"
    
    custom_tour_dest_id = fields.Many2one('custom.tour.destination','Destination')
    name = fields.Char("Sites Name",required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: