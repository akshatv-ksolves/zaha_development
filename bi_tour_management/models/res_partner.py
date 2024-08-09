# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class res_partner(models.Model):
	
    _inherit = 'res.partner'
    
    tour_partner_history_ids = fields.One2many('tour.booking','customer_id','History Lines')
    agent=fields.Boolean('Agent')
    is_hotel=fields.Boolean('Hotel')
    hotel_type_id = fields.Many2one('hotel.type', 'Hotel Type')
    commisision_ids = fields.One2many('agent.commission.line','agent_partner_id','Commission')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: