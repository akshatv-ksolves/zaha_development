# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class room_type(models.Model):

    _name = "room.type"
    _description = "Room Type"

    name = fields.Char('Name',required=True)
    room_type_id  = fields.Many2one('product.product','Room Type ',required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: