from odoo import api, fields, models
from odoo.tools import format_datetime, formatLang

class SeasonalOffer(models.Model):
    _name = "seasonal.offer"
    _description = "Seasonal Offer"

    name = fields.Char(string='Offer Name', required=True)
    season_id = fields.Many2one('tour.season', string='Season')
    hotel_id = fields.Many2many('res.partner', domain =[('is_hotel','=','True')])
    discount_coupon = fields.Char(string='Discount Coupon')
    compute_price = fields.Selection(
        selection=[
            ('fixed', "Fixed Price"),
            ('percentage', "Discount"),
        ],
        index=True, default='fixed', required=True)
    offer_rate = fields.Integer('Discount Price')
    offer_percentage = fields.Float('Discount Percentage')
    booking_date_from = fields.Date(string='Booking Date From', required=True)
    booking_date_to = fields.Date(string='Booking Date To', required=True)
    stay_date_from = fields.Date(string='Stay Date(from)')
    stay_date_to = fields.Date(string='Stay date(to)')
    terms_n_conditions = fields.Text(string='Terms & Conditions')
    rate_sheet = fields.One2many('product.rate','seasonal_offer_id' ,string='Rate Sheet')

    @api.depends('compute_price', 'offer_rate', 'offer_percentage')
    def _compute_name_and_price(self):
        for item in self:
            if item.compute_price == 'fixed':
                item.price = formatLang(
                    item.env, item.fixed_price, monetary=True, dp="Product Price", currency_obj=item.currency_id)
            elif item.compute_price == 'percentage':
                item.price = _("%s %% discount", item.percent_price)

class ProductRate(models.Model):
    _name = "product.rate"
    _description = "Product Rate"

    name = fields.Many2one('product.template','Name')
    min_qty = fields.Integer(string='Min. Quantity')
    seasonal_offer_id = fields.Many2one('seasonal.offer')