"""Print and sanity-check the local report aggregates."""

import json

from report import getReportData


report_data = getReportData()
top_product_revenues = [
    product["revenue"] for product in report_data["top_products_by_revenue"]
]

if any(revenue > report_data["total_revenue"] for revenue in top_product_revenues):
    raise ValueError("A product revenue cannot exceed total revenue.")

print(json.dumps(report_data, indent=2))