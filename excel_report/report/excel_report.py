from odoo import models



class ReportSalesExcel(models.AbstractModel):
    _name = 'report.excel_report.report_sale_order_xls'
    _inherit = 'report.report_xlsx.abstract'



    def generate_xlsx_report(self, workbook, data, sale):
        print("sale",sale)
        sheet = workbook.add_worksheet("Sale Oder")
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center'})
        for obj in sale:
            report_name = obj.partner_id.name
            row = 3
            col = 3

            sheet.set_column('D:H', 25)


            row += 1
            sheet.merge_range(row, col, row +1, col + 4, 'Sale Oder', format_1)

            row += 2
            sheet.write(row, col, 'Order No:', format_1)
            sheet.write(row, col + 1, obj.name)

            sheet.write(row, col + 3, 'Date:', format_1)
            sheet.write(row, col + 4, obj.date_order)

            row += 1
            sheet.merge_range(row, col, row+6, col,'Customer Details:', format_1)
            sheet.write(row, col + 1,obj.partner_id.name)
            sheet.write(row + 1, col + 1,obj.partner_id.street)
            sheet.write(row + 2, col + 1,obj.partner_id.street2)
            sheet.write(row + 3, col + 1, obj.partner_id.city )
            sheet.write(row + 4, col + 1, obj.partner_id.state_id.name)
            sheet.write(row + 5, col + 1, obj.partner_id.zip)
            sheet.write(row + 6, col + 1, obj.partner_id.country_id.name)

            # col += 3
            # sheet.merge_range(row, col, row + 6, col, 'Company Details:', format_1)
            # sheet.write(row, col + 1, obj.company_id.name)
            # sheet.write(row + 1, col + 1, obj.company_id.street)
            # sheet.write(row + 2, col + 1, obj.company_id.street2)
            # sheet.write(row + 3, col + 1, obj.company_id.city)
            # sheet.write(row + 4, col + 1, obj.company_id.state_id.name)
            # sheet.write(row + 5, col + 1, obj.company_id.zip)
            # sheet.write(row + 6, col + 1, obj.company_id.country_id.name)

            row += 7

            sheet.write(row, col, 'Sales Person:', format_1)
            sheet.write(row , col + 1, obj.user_id.name)




