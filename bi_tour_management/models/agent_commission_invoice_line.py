# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class agent_commission_invoice_line(models.Model):


	_name = "agent.commission.invoice.line"
	_description = "Agent Commission Invoice Line"

	tour_cost = fields.Float('Tour Cost',compute = "_onchnage_booking")
	commission_line_id = fields.Many2one('agent.commission.invoice', 'Commission ID')
	tour_package_id = fields.Many2one('tour.package','Tour')
	customer_partner_id = fields.Many2one('res.partner','Customer Name')
	name = fields.Char('Description')
	tour_booking_id = fields.Many2one('tour.booking','Tour Booking ID',required=True)
	commission_percentage = fields.Float('Commission Percentage(%)' )
	commission_amount = fields.Float('Commission Amount(fixed)')
	company_id = fields.Many2one(
		related='commission_line_id.company_id',
		store=True, index=True, precompute=True)
	commission_ovell_amount = fields.Float("Commission Amount",compute = "_compute_com_amt")
	commission_type = fields.Selection([
		('type1', 'Commission Percentage'),
		('type2', 'Commission Amount')
		], required=True)
	
	currency_id = fields.Many2one('res.currency', string='Currency')


	@api.onchange('tour_booking_id')
	def _onchnage_booking(self):
		for line in self:
			line.tour_cost = line.tour_booking_id.total_amt

	@api.onchange("commission_percentage")
	def _onchange_com_percent(self):
		for rec in self:
			if rec.commission_percentage > 100 or rec.commission_percentage < 0:
				raise ValidationError(_('Please enter valid Commission Percentage!'))

	@api.onchange("tour_cost","commission_percentage","commission_amount")
	def _compute_com_amt(self):

		for i in self:
			com_amt= 0.0

			if i.commission_type == "type1" :
				com_amt = (i.tour_cost * i.commission_percentage)/100

			if i.commission_type == "type2":
				com_amt = i.commission_amount

			i.commission_ovell_amount = com_amt
 

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: