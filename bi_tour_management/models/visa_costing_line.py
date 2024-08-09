# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields,api

class visa_costing_line(models.Model):
	
    _name = "visa.costing.line"
    _description = "Visa Costing Line"

    iternity_id = fields.Many2one("custom.tour.itinary",'Iternity Id')
    country_id = fields.Many2one("res.country",required=True)
    name = fields.Char("Visa")
    visa_type = fields.Selection([
        ('Tourist Visa (Single Entry)', 'Tourist Visa (Single Entry)'),
        ('Tourist Visa (Double Entry)', 'Tourist Visa (Double Entry)')
        ],string="Visa Type")
    cost_price = fields.Float("Visa Cost Price")
    sale_price = fields.Float("Visa Sale Price")
    total_person = fields.Integer("No.Of Person",required=True)
    total_cost_price = fields.Float("Total Cost Price",compute="onchange_quantity",readonly=True)
    total_sale_price = fields.Float("Total Sale Price",compute="onchange_quantity",readonly=True)
    sale_tax_ids = fields.Many2many("account.tax","visa_costing_sale_ref",domain = [('type_tax_use','=','sale')])
    pur_tax_ids = fields.Many2many("account.tax","visa_costing_purchase_ref",domain = [('type_tax_use','=','purchase')])
    # pur_tax_ids =fields.Many2many("account.tax",string="purchase tax")
    book_id = fields.Many2one("tour.booking")
    package_id = fields.Many2one("tour.package")
    company_id = fields.Many2one(
        related='iternity_id.company_id',
        store=True, index=True, precompute=True)
    visa_pln_sale = fields.Float("Sale Amount",compute ="Onchange_sale_visa")
    visa_pln_purchase = fields.Float("Purchase Amount",compute ="Onchnage_cost_visa")

    sale_tax_amount_visa = fields.Float("Sale Tax Amount",compute="Onchnage_cost_visa")
    purchse_tax_amount_visa = fields.Float("Purchse Tax Amount",compute="Onchnage_cost_visa") 

    currency_id = fields.Many2one('res.currency', string='Currency')


    @api.onchange('cost_price','sale_price','total_person')
    def onchange_quantity(self):
        for cost_visa in self:
            cost_visa.total_cost_price = cost_visa.cost_price * cost_visa.total_person
            cost_visa.visa_pln_purchase =cost_visa.total_cost_price
            cost_visa.total_sale_price = cost_visa.sale_price * cost_visa.total_person
            cost_visa.visa_pln_sale = cost_visa.total_sale_price

    @api.onchange("pur_tax_ids","sale_tax_ids")
    def Onchnage_cost_visa(self):

        for cost_visa in self:

            visa_pur = cost_visa.pur_tax_ids.compute_all(cost_visa.total_cost_price)
            cost_visa.visa_pln_purchase =visa_pur['total_included']
            cost_visa.purchse_tax_amount_visa = cost_visa.visa_pln_purchase - cost_visa.total_cost_price
            


            visa_sale = cost_visa.sale_tax_ids.compute_all(cost_visa.total_sale_price)
            cost_visa.visa_pln_sale =visa_sale['total_included']

            cost_visa.sale_tax_amount_visa = cost_visa.visa_pln_sale - cost_visa.total_sale_price

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: