from werkzeug import urls

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)

class GenratePaymentLink(models.TransientModel):
    _inherit = "payment.link.wizard"
    _description = "Generate Payment Link Change"

    def _generate_link(self):
        """ Override of the base method to add the order_id in the link. """
        for payment_link in self:

            if payment_link.res_model == 'sale.order':
                base_url = self.env['ir.config_parameter'].sudo().search([('key', '=', 'products_url')], limit=1).value
                payment_link.link = ('%s/website_payment/pay?reference=%s&amount=%s&currency_id=%s'
                                    '&partner_id=%s&order_id=%s&company_id=%s&access_token=%s') % (
                                        base_url,
                                        urls.url_quote_plus(payment_link.description),
                                        payment_link.amount,
                                        payment_link.currency_id.id,
                                        payment_link.partner_id.id,
                                        payment_link.res_id,
                                        payment_link.company_id.id,
                                        payment_link.access_token
                                    )
            else:
                super(GenratePaymentLink, payment_link)._generate_link()
