# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class product_product(models.Model):
	
    _inherit = 'product.product'

    is_tour=fields.Boolean('Is Tour')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: