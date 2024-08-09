# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class agent_commission_invoice(models.Model):

    _name = "agent.commission.invoice"
    _description = "Agent Commission Invoice"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('invoice','Invoiced'),
        ('done','Done'),
        ('cancel','Cancel')
        ],string="Status",readonly=True, default="draft")
    current_date = fields.Date('Date',required = True)
    name = fields.Char('Name', readonly=True)
    agent_partner_id = fields.Many2one('res.partner','Agent',required = True)
    product_pricelist_id = fields.Many2one('res.currency', 'Pricelist',required = True)
    commission_line = fields.One2many('agent.commission.invoice.line','commission_line_id','Invoice  Lines')
    total_amount = fields.Float('Commission Amount',compute='amount_all',readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    invoice_count = fields.Integer("Invoice",compute="_Invoice_count")

    def amount_all(self):
      total_amount=0.0
      for each in self:
        for commision in each.commission_line:
          total_amount += commision.commission_ovell_amount
        each.total_amount=total_amount
    
    @api.model
    def create(self,vals):
      vals['name'] = self.env['ir.sequence'].get('agent.commission.invoice') or '/'
      res = super(agent_commission_invoice, self).create(vals)
      return res
  
    def confirm_commission(self):
      for rec in self:
        rec.write({'state':'confirm'})

    def action_done(self):
      for rec in self:
        rec.write({'state':'done'})

    def create_invoice(self):
      invoice_line_list=[]
      ir_property_obj = self.env['ir.property']
      if not self.agent_partner_id.company_id:
          raise UserError(_('Please set the company of Agent'))
      agent_commission_inv_line_obj = self.env['agent.commission.invoice.line'].search([('commission_line_id','=',self.id)])
      for line in agent_commission_inv_line_obj:
        invoice_line_tax_ids=[tax.id for tax in line.tour_package_id.product_id.taxes_id if tax.id ]
        invoice_line_account_id = False            
        if line.tour_package_id.product_id:                
          invoice_line_account_id = line.tour_package_id.product_id.property_account_income_id.id or line.tour_package_id.product_id.categ_id.property_account_income_categ_id.id or False             
          if not invoice_line_account_id: 
            invoice_line_account_id = ir_property_obj.get('property_account_income_categ_id', 'product.category')
          if not invoice_line_account_id:                
            raise UserError(_('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') % (line.tour_package_id.product_id.name,))
        invoice_lines = {
                        'name':line.tour_package_id.product_id.name,
                        'account_id':invoice_line_account_id,
                        'price_unit':line.commission_ovell_amount,
                        'quantity':1,
                        'product_uom_id':line.tour_package_id.product_id.uom_id.id or False,
                        'product_id':line.tour_package_id.product_id.id or False,
                        'tax_ids':([(6,0,invoice_line_tax_ids)])
                      }
        invoice_line_list.append((0,0,invoice_lines))
      journal_ids = self.env['account.journal'].search([('type','=','sale')])   
      account_vals = {
                      'name':self.name,
                      'move_type':'out_invoice',
                      'journal_id':journal_ids and journal_ids[0].id or False,
                      'partner_id':self.agent_partner_id.id or False,
                      'partner_shipping_id':self.agent_partner_id.id or False,
                      'currency_id':self.product_pricelist_id.id,
                      'invoice_payment_term_id':False,
                      'team_id':False,
                      'company_id':self.agent_partner_id.company_id.id or False,
                      'invoice_line_ids':invoice_line_list
                    }
      self.env['account.move'].create(account_vals)
      self.write({'state':'invoice'})

    def _Invoice_count(self):
        for invoi_count in self:
            invoice_order_ids = self.env["account.move"].search([('name','=',invoi_count.name)])
            
            invoi_count.invoice_count = len(invoice_order_ids)

    def button_count_invoice(self):
        self.ensure_one()
        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'res_model': 'account.move',
            'domain': [('name','=',self.name)],
        }						
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: