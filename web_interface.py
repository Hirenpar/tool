#!/usr/bin/env python3
"""
Web Interface for Advanced SEO Audit Software
Flask-based web application for easy access to SEO auditing features
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import threading
from datetime import datetime
from seo_audit import SEOAuditor
import io
import csv

app = Flask(__name__)
app.secret_key = 'seo_audit_secret_key_2024'

# Store audit results temporarily
audit_results_cache = {}

@app.route('/')
def index():
    """Main page with audit form"""
    return render_template('index.html')

@app.route('/audit', methods=['POST'])
def start_audit():
    """Start SEO audit for given URL"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        api_key = data.get('api_key', '').strip() or None
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Generate unique audit ID
        audit_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(url) % 10000}"
        
        # Start audit in background thread
        def run_audit():
            auditor = SEOAuditor(pagespeed_api_key=api_key)
            results = auditor.audit_website(url)
            results['audit_id'] = audit_id
            results['report'] = auditor.generate_report()
            audit_results_cache[audit_id] = results
        
        thread = threading.Thread(target=run_audit)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'audit_id': audit_id,
            'message': 'Audit started successfully',
            'status': 'running'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audit/<audit_id>/status')
def audit_status(audit_id):
    """Check audit status"""
    if audit_id in audit_results_cache:
        return jsonify({
            'status': 'completed',
            'audit_id': audit_id
        })
    else:
        return jsonify({
            'status': 'running',
            'audit_id': audit_id
        })

@app.route('/audit/<audit_id>/results')
def audit_results(audit_id):
    """Get audit results"""
    if audit_id not in audit_results_cache:
        return jsonify({'error': 'Audit not found or still running'}), 404
    
    results = audit_results_cache[audit_id]
    return jsonify(results)

@app.route('/audit/<audit_id>/report')
def audit_report(audit_id):
    """Display audit report"""
    if audit_id not in audit_results_cache:
        return render_template('error.html', message='Audit not found or still running')
    
    results = audit_results_cache[audit_id]
    return render_template('report.html', results=results, audit_id=audit_id)

@app.route('/audit/<audit_id>/download/json')
def download_json(audit_id):
    """Download audit results as JSON"""
    if audit_id not in audit_results_cache:
        return jsonify({'error': 'Audit not found'}), 404
    
    results = audit_results_cache[audit_id]
    
    # Create in-memory file
    output = io.StringIO()
    json.dump(results, output, indent=2, default=str)
    output.seek(0)
    
    # Create BytesIO for file download
    mem_file = io.BytesIO()
    mem_file.write(output.getvalue().encode('utf-8'))
    mem_file.seek(0)
    
    return send_file(
        mem_file,
        mimetype='application/json',
        as_attachment=True,
        download_name=f'seo_audit_{results.get("domain", "unknown")}_{audit_id}.json'
    )

@app.route('/audit/<audit_id>/download/csv')
def download_csv(audit_id):
    """Download audit results as CSV"""
    if audit_id not in audit_results_cache:
        return jsonify({'error': 'Audit not found'}), 404
    
    results = audit_results_cache[audit_id]
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['Category', 'Item', 'Status', 'Value', 'Recommendation'])
    
    # Write data from each category
    categories = ['technical_seo', 'on_page_seo', 'off_page_seo', 'user_experience', 'security_performance']
    
    for category in categories:
        if category in results:
            category_data = results[category]
            for item_key, item_data in category_data.items():
                if isinstance(item_data, dict):
                    status = item_data.get('status', 'N/A')
                    value = str(item_data.get('value', item_data.get('score', 'N/A')))
                    recommendation = item_data.get('recommendation', 'N/A')
                    writer.writerow([category.replace('_', ' ').title(), item_key.replace('_', ' ').title(), status, value, recommendation])
    
    output.seek(0)
    
    # Create BytesIO for file download
    mem_file = io.BytesIO()
    mem_file.write(output.getvalue().encode('utf-8'))
    mem_file.seek(0)
    
    return send_file(
        mem_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'seo_audit_{results.get("domain", "unknown")}_{audit_id}.csv'
    )

@app.route('/api/docs')
def api_docs():
    """API documentation"""
    return render_template('api_docs.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Starting SEO Audit Web Interface...")
    print("📍 Access the application at: http://localhost:5000")
    print("📚 API Documentation at: http://localhost:5000/api/docs")
    
    app.run(debug=True, host='0.0.0.0', port=5000)