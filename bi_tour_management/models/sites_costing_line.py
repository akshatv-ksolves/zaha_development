# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class sites_costing_line(models.Model):

    _name = "sites.costing.line"
    _description = "Sites Costing Line"
    								
    iternity_id = fields.Many2one("custom.tour.itinary",'Iternity Id')
    name = fields.Many2one("product.product",'Site Names',required=True,domain = [('type','=','service')])
    new_cost_price = fields.Char('Cost Price/Person')
    new_sale_price = fields.Char('Sale Price/Person')
    total_cost_price = fields.Float('Total Cost Price')
    total_sale_price = fields.Float('Total Sale Price')
    book_id = fields.Many2one("tour.booking")
    package_id = fields.Many2one("tour.package")
    company_id = fields.Many2one(
        related='iternity_id.company_id',
        store=True, index=True, precompute=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: