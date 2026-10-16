# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
# Copyright 2022 Tecnativa - Pedro M. Baeza
import logging

from odoo import models
from odoo.tools import SQL

_logger = logging.getLogger(__name__)


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    def _select_list(self, table):
        """Put quantity to be billed as 0 if it has been forced."""
        select_list = super()._select_list(table)
        alias = " AS qty_to_be_billed"
        for index, item in enumerate(select_list):
            code, params, to_flush = item._sql_tuple
            if code.rstrip().endswith(alias):
                expression = SQL(
                    code.rstrip()[: -len(alias)], *params, to_flush=to_flush
                )
                select_list[index] = SQL(
                    "CASE WHEN %s THEN 0.0 ELSE %s END AS qty_to_be_billed",
                    table.order_id.force_invoiced,
                    expression,
                )
                break
        else:
            _logger.error(
                "Query substitution failed. Check 'purchase/report/purchase_report.py "
                "for changes"
            )
        return select_list
