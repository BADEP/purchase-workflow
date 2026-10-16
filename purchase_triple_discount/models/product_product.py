# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_last_po_seller_info(self, partner_id=False, company_id=False):
        """In 20.0, confirming a PO no longer creates vendor pricelists: the last
        confirmed PO line acts as fallback seller. Propagate its discounts."""
        res = super()._get_last_po_seller_info(
            partner_id=partner_id, company_id=company_id
        )
        if res:
            last_line = self._get_last_po_line(
                partner_id=partner_id, company_id=company_id
            )
            res.update(
                {
                    fname: last_line[fname]
                    for fname in last_line._get_multiple_discount_field_names()
                }
            )
        return res
