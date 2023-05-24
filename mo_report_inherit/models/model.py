from odoo import fields, models, api


class MrpReport(models.Model):
    _inherit = 'mrp.report'
    _description = "Manufacturing Report"
    _auto = False


    date_planned_start = fields.Datetime(
            'Scheduled Date', copy=False,help="Date at which you plan to start the production.")

    def _select(self):
        select_str = """
            SELECT
                min(mo.id)             AS id,
                mo.id                  AS production_id,
                mo.date_planned_start  AS date_planned_start,
                mo.company_id          AS company_id,
                mo.date_finished       AS date_finished,
                mo.product_id          AS product_id,
                prod_qty.product_qty   AS qty_produced,
                comp_cost.total * currency_table.rate                                                                                   AS component_cost,
                op_cost.total * currency_table.rate                                                                                     AS operation_cost,
                (comp_cost.total + op_cost.total) * currency_table.rate                                                                 AS total_cost,
                op_cost.total_duration                                                                                                  AS duration,
                comp_cost.total * (1 - cost_share.byproduct_cost_share) / prod_qty.product_qty * currency_table.rate                    AS unit_component_cost,
                op_cost.total * (1 - cost_share.byproduct_cost_share) / prod_qty.product_qty * currency_table.rate                      AS unit_operation_cost,
                (comp_cost.total + op_cost.total) * (1 - cost_share.byproduct_cost_share) / prod_qty.product_qty * currency_table.rate  AS unit_cost,
                op_cost.total_duration / prod_qty.product_qty                                                                           AS unit_duration,
                (comp_cost.total + op_cost.total) * cost_share.byproduct_cost_share * currency_table.rate                               AS byproduct_cost
        """

        return select_str