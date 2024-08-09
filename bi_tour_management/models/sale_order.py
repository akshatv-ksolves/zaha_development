# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields

class sale_order(models.Model):

    _inherit = "sale.order"
    
    tour_book_id = fields.Many2one('tour.booking')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: