from flask_smorest import Blueprint, abort
from flask import request, jsonify
from sqlalchemy import func, extract, text
from .models import db, Sales
from .schemas import SaleSchema, TopRevenueProductSchema
from . import cache
import time

analytics_bp = Blueprint("analytics", "analytics", url_prefix="/analytics")

@analytics_bp.route('/monthly-summary/no-cache')
def monthly_summary_no_cache():
    year = request.args.get('year', type=int)
    if not year:
        abort(400, message="Year is required")
    
    start = time.time()
    
    sql_query = text("""
        SELECT
            DATE_TRUNC('month', date) AS month,
            SUM(quantity) AS total_quantity,
            SUM(price * quantity) AS total_revenue
        FROM sales
        WHERE EXTRACT(YEAR FROM date) = :year
        GROUP BY month
        ORDER BY month
    """)
    result = db.session.execute(sql_query, {'year': year}).fetchall()
    
    duration = time.time() - start
    
    data = SaleSchema(many=True).dump(result)
    return jsonify({"data": data, "duration": duration}), 200

@analytics_bp.route('/monthly-summary/with-cache')
@cache.cached(timeout=600, query_string=True)
def monthly_summary_with_cache():
    return monthly_summary_no_cache()

