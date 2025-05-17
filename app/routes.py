from flask_smorest import Blueprint, abort
from flask import request, jsonify, Response
from sqlalchemy import func, extract, text
from .models import db, Sales
from .schemas import( 
    SaleSummarySchema,
    SaleSummaryResponseSchema,
    TopRevenueProductSchema,
    TopRevenueProductResponseSchema,
    MonthlySaleSummarySchema,
    MonthlySaleSummaryResponseSchema
)

from . import cache
import time
from datetime import datetime

analytics_bp = Blueprint("analytics", "analytics", url_prefix="/analytics")

@analytics_bp.route('/monthly-summary/no-cache')
@analytics_bp.response(200, MonthlySaleSummaryResponseSchema)
def monthly_summary_no_cache():
    """
    Get monthly sales summary for a given year (no cache).

    Query Parameters:
        year (int): The year for which to summarize sales.

    Returns:
        JSON response with monthly sales summary and query duration.
        HTTP 400 if year is not provided.
    """
    
    start_time = time.time()

    year = request.args.get('year', type=str)
    if not year or len(year) != 4 or not year.isdigit():
        abort(400, message="Year is required in format YYYY")
    
    year_start_date = year+'-01-01'
    year_end_date = year+'-12-31'
    
    if not year:
        abort(400, message="Year is required")
    
    sql_query = text("""
        SELECT
            DATE_TRUNC('month', date) AS month,
            SUM(quantity) AS total_quantity,
            SUM(price * quantity) AS total_revenue
        FROM sales
        WHERE date BETWEEN :year_start_date AND :year_end_date
        GROUP BY month
        ORDER BY month
    """)
    result = db.session.execute(sql_query, {'year_start_date':year_start_date, 'year_end_date':year_end_date}).fetchall()
    
    duration = time.time() - start_time
    
    data = MonthlySaleSummarySchema(many=True).dump(result)
    response_data =jsonify({"data": data, "duration": duration}) 
    return response_data, 200


@analytics_bp.route('/monthly-summary')
@analytics_bp.response(200, MonthlySaleSummaryResponseSchema)
@cache.cached(timeout=600, query_string=True)
def monthly_summary_with_cache():
    """
    Get monthly sales summary for a given year (cached).

    Query Parameters:
        year (int): The year for which to summarize sales.

    Returns:
        JSON response with monthly sales summary and query duration.
        HTTP 400 if year is not provided.
        Response is cached for 10 minutes.
    """
    result = monthly_summary_no_cache()
    if isinstance(result, tuple):
        response_data, status = result
    else:
        response_data, status = result, 200
    raw = response_data.get_data()
    return Response(raw, status=status, mimetype="application/json")
    



#top products by revenue
@analytics_bp.route('/top-products/no-cache')
@analytics_bp.response(200, TopRevenueProductResponseSchema)
def top_products_no_cache():
    """
    Get top 5 products by revenue for a given year (no cache).

    Query Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' format (required).
        end_date (str): End date in 'YYYY-MM-DD' format (required).
        

    Returns:
        JSON response with top 5 products and query duration.
        HTTP 400 if year is not provided or invalid.
    """    
    start_time = time.time()
    # Get the query parameters
    start_date= request.args.get('start_date')
    end_date= request.args.get('end_date')
    
    if not start_date or not end_date:
        abort(400, message="Start date and end date are required")
        
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        abort(400, message="Invalid date format. Use YYYY-MM-DD")
    

    sql_query = text("""
        SELECT
            product_id,
            product_name,
            SUM(revenue) AS total_revenue
        FROM sales
        WHERE date BETWEEN :start_date AND :end_date
        GROUP BY product_id, product_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """)
    result = db.session.execute(sql_query, {'start_date': start_date,
                                             'end_date': end_date}).fetchall()
    duration = time.time() - start_time
    data = TopRevenueProductSchema(many=True).dump(result)
    response_data = jsonify({"data": data, "duration": duration})
    return response_data, 200



@analytics_bp.route('/top-products')
@analytics_bp.response(200, TopRevenueProductResponseSchema)
@cache.cached(timeout=600)
def top_products_with_cache():
    """
    Get top 5 products by revenue for a given year (cached).

    Query Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' format (required).
        end_date (str): End date in 'YYYY-MM-DD' format (required).

    Returns:
        JSON response with top 5 products and query duration.
        HTTP 400 if year is not provided or invalid.
        Response is cached for 10 minutes.
    """
    result = top_products_no_cache()
    if isinstance(result, tuple):
        response_data, status = result
    else:
        response_data, status = result, 200
    raw = response_data.get_data()
    return Response(raw, status=status, mimetype="application/json")
    

    

#get sales by product, region and date
@analytics_bp.route('/sales-summary/no-cache')
@analytics_bp.response(200, SaleSummaryResponseSchema)
def sales_summary_no_cache():
    """
    Get sales summary by product, region, and date range (no cache).

    Query Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' format (required).
        end_date (str): End date in 'YYYY-MM-DD' format (required).
        product_id (str, optional): Product ID to filter.
        region (str, optional): Region to filter.

    Returns:
        JSON response with sales summary and query duration.
        HTTP 400 if required parameters are missing or invalid.
    """
    start_time = time.time()

    # Get the query parameters
    start_date= request.args.get('start_date')
    end_date= request.args.get('end_date')
    product_id= request.args.get('product_id')
    region= request.args.get('region', type=str)
    
    if not start_date or not end_date:
        abort(400, message="Start date and end date are required")
        
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        abort(400, message="Invalid date format. Use YYYY-MM-DD")
    
    sql= """
              SELECT 
                region,
                product_id,
                product_name,
                SUM(price * quantity) AS total_revenue
              FROM sales
              WHERE date BETWEEN :start_date AND :end_date
              """
    parameters = {"start_date": start_date, "end_date": end_date}
    
    if region:
        #capitalize the region for consistency
        region = region.upper()
        sql += " AND region LIKE :region"
        #match any string that starts with the region. It can use the index 
        parameters["region"]= f"{region}%"
    
    if product_id:
        sql += " AND product_id = :product_id"
        parameters["product_id"] = product_id
        
    sql += " GROUP BY region, product_id, product_name"
    
    
    # Execute the SQL query
    result = db.session.execute(text(sql), parameters).fetchall()
    duration= time.time() - start_time
    
    data = SaleSummarySchema(many=True).dump(result)
    response_data = jsonify({"data": data, "duration": duration})
    return response_data, 200


#get sales by product, region and date (cached)
@analytics_bp.route('/sales-summary')
@analytics_bp.response(200, SaleSummaryResponseSchema)
@cache.cached(timeout=600, query_string=True)
def sales_summary_with_cache():
    """
    Get sales summary by product, region, and date range (cached).

    Query Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' format (required).
        end_date (str): End date in 'YYYY-MM-DD' format (required).
        product_id (str, optional): Product ID to filter.
        region (str, optional): Region to filter.

    Returns:
        JSON response with sales summary and query duration.
        HTTP 400 if required parameters are missing or invalid.
        Response is cached for 10 minutes.
    """
    result = sales_summary_no_cache()
    if isinstance(result, tuple):
        response_data, status = result
    else:
        response_data, status = result, 200
    raw = response_data.get_data()
    return Response(raw, status=status, mimetype="application/json")
