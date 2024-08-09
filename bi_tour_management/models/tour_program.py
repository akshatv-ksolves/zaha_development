# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api

class tour_program(models.Model):

	_name = "tour.program"
	_description = "Tour Program"

	name = fields.Char("Tour Code")
	tour_id = fields.Many2one('tour.package', 'package')
	iternity_id = fields.Many2one("custom.tour.itinary",'Iternity Id')
	days = fields.Integer("Days", required =True, default ="0")
	description = fields.Char("Description", required=True)
	breakfast = fields.Boolean('Breakfast')
	lunch = fields.Boolean('Lunch')
	dinner = fields.Boolean('Dinner')
	site_ids = fields.Many2many('product.product')
	book_id = fields.Many2one("tour.booking")

	program_line_sale = fields.Float("Sale Price")
	program_line_cost = fields.Float("Cost Price")

	expected_line_sale = fields.Float("Sale Amount",compute="expected_sale")
	expected_line_cost = fields.Float("Cost Amount",compute="expected_cost")

	currency_id = fields.Many2one('res.currency', string='Currency')
	company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

	@api.depends('program_line_sale','days')
	def expected_sale(self):
		for ssl in self:
			if ssl.program_line_sale:
				ssl.expected_line_sale = ssl.program_line_sale * ssl.days
			else:
				ssl.expected_line_sale = 0.0

	@api.depends('program_line_cost','days')
	def expected_cost(self):
		for cot in self:
			if cot.program_line_cost:
				cot.expected_line_cost = cot.program_line_cost * cot.days
			else:
				cot.expected_line_cost = 0.0


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: