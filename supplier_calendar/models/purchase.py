# Copyright 2020 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def _get_date_planned(self, seller_info, po=False):
        date_planned = super()._get_date_planned(seller_info, po)
        partner = seller_info.get("partner_id")
        if partner and partner.factory_calendar_id:
            date_order = po.date_order if po else self.order_id.date_order
            if date_order:
                date_planned = partner.supplier_plan_days(
                    date_order, seller_info.get("delay", 0)
                )
            else:
                date_planned = partner.supplier_plan_days(
                    fields.Datetime.now(), seller_info.get("delay", 0)
                )
        return date_planned
