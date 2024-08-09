# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _

class tour_package_product_line(models.Model):

    _name = "tour.package.product.line"
    _description = "Tour Package Product Line"

    tour_id = fields.Many2one('tour.package', 'Package')
    book_id = fields.Many2one('tour.booking',"Booking Id")
    product_id = fields.Many2one('product.product','Product')
    name = fields.Char('Description', required=True)
    qty = fields.Float('Quantity', required=True)
    unit_price = fields.Float('Price Unit', required=True)
    tax_id = fields.Many2many('account.tax','tax_package_rel','tour_id','tax_id','Taxes')
    subtotal = fields.Float('Sub Total',readonly=True)
    currency_id = fields.Many2one(related='tour_id.currency_id', store=True, string='Currency', readonly=True)
    price_subtotal = fields.Float('SubTotal', compute='_compute_subtotal' ,readonly=True)
    price_tax = fields.Float('Tax', compute='_compute_subtotal' ,readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            tax_lst = []
            if rec.product_id:
                if rec.product_id.taxes_id:
                    for a in rec.product_id.taxes_id:
                        tax_lst.append(a.id)
                rec.name = rec.product_id.name
                rec.qty = 1.0
                rec.unit_price = rec.product_id.lst_price
                rec.tax_id = [(6,0,tax_lst)]

    @api.depends('qty', 'unit_price', 'tax_id')
    def _compute_subtotal(self):
        for line in self:
            taxes = line.tax_id.compute_all(line.unit_price , line.tour_id.currency_id, line.qty, product=line.product_id, partner=None)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_subtotal': taxes['total_excluded'],
            })

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: