# 🔍 Advanced SEO Audit Tool

A comprehensive SEO auditing software that performs detailed website analysis covering Technical SEO, On-Page optimization, User Experience, Performance, and Security. Built with Python and Flask, featuring a modern web interface and Google PageSpeed Insights integration.

![SEO Audit Tool](https://img.shields.io/badge/SEO-Audit%20Tool-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔧 Technical SEO Analysis
- **Page Speed & Core Web Vitals**: LCP, INP, CLS measurements with optimization suggestions
- **Mobile-Friendliness**: Responsive design and viewport configuration checks
- **HTTPS & SSL**: Security protocol validation and certificate verification
- **Indexability & Crawlability**: Robots meta tags and directive analysis
- **XML Sitemap & Robots.txt**: Presence and accessibility verification
- **Canonical Tags**: Duplicate content prevention analysis
- **Structured Data**: Schema markup detection (JSON-LD, Microdata, RDFa)
- **Broken Links**: Internal and external link validation
- **Redirects**: 301/302 redirect chain analysis

### 📝 On-Page SEO Analysis
- **Title Tags**: Length optimization (30-60 characters) and keyword usage
- **Meta Descriptions**: Character count (120-160 optimal) and uniqueness
- **Heading Structure**: H1-H6 hierarchy validation
- **Keyword Density**: Content analysis and semantic relevance
- **Image Optimization**: Alt text coverage, file formats, and lazy loading
- **Internal Linking**: Navigation structure and anchor text analysis
- **Content Quality**: Word count, readability, and uniqueness assessment

### 🔗 Off-Page SEO Analysis
- **Domain Authority**: Age-based trust score estimation
- **Social Media Signals**: Open Graph and Twitter Card implementation
- **Backlink Analysis**: Recommendations for external link building
- **Trust Indicators**: Domain registration and authority metrics

### 👤 User Experience & Accessibility
- **Mobile vs Desktop**: Responsive design implementation
- **Navigation Clarity**: Menu structure and user flow analysis
- **Accessibility Features**: ARIA labels, contrast ratios, form labels
- **WCAG Compliance**: Web accessibility guidelines adherence

### 🔒 Security & Performance Enhancements
- **Security Headers**: CSP, X-Frame-Options, HSTS implementation
- **CDN Usage**: Content delivery network detection
- **Compression**: Gzip/Brotli encoding verification
- **Caching**: Browser and server-side caching analysis
- **Resource Optimization**: CSS/JS minification and unused code detection

### ⚡ Google PageSpeed Insights Integration
Complete integration with detailed analysis including:
- **Performance Scores**: Mobile and desktop performance metrics
- **Core Web Vitals**: LCP, INP, CLS with ideal ranges
- **Field Data**: Real-world user experience from Chrome UX Report
- **Lab Data**: Controlled environment testing results
- **Opportunities**: Specific optimization recommendations
- **Diagnostics**: Advanced technical insights
- **Lighthouse Integration**: Full Lighthouse audit results

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/seo-audit-tool.git
cd seo-audit-tool
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Get Google PageSpeed Insights API Key (Optional):**
   - Visit [Google Developers Console](https://developers.google.com/speed/docs/insights/v5/get-started)
   - Create a new project or select existing
   - Enable PageSpeed Insights API
   - Generate API key

### Usage

#### Web Interface (Recommended)

1. **Start the web server:**
```bash
python web_interface.py
```

2. **Access the application:**
   - Open your browser to `http://localhost:5000`
   - Enter website URL and optional API key
   - Start audit and view comprehensive results

#### Command Line Interface

```bash
python seo_audit.py
```

#### Programmatic Usage

```python
from seo_audit import SEOAuditor

# Initialize auditor
auditor = SEOAuditor(pagespeed_api_key='your_api_key')

# Run audit
results = auditor.audit_website('https://example.com')

# Generate report
report = auditor.generate_report()
print(report)

# Access specific data
print(f"Technical SEO Score: {results['scores']['technical_seo_score']}")
print(f"Page Speed: {results['technical_seo']['response_time']['value']:.2f}s")
```

## 📖 API Documentation

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/audit` | Start new SEO audit |
| GET | `/audit/{id}/status` | Check audit status |
| GET | `/audit/{id}/results` | Get JSON results |
| GET | `/audit/{id}/report` | View HTML report |
| GET | `/audit/{id}/download/json` | Download JSON file |
| GET | `/audit/{id}/download/csv` | Download CSV file |
| GET | `/health` | API health check |

### Example API Usage

**Start Audit:**
```bash
curl -X POST http://localhost:5000/audit \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "api_key": "your_key"}'
```

**Check Status:**
```bash
curl http://localhost:5000/audit/audit_123/status
```

**Get Results:**
```bash
curl http://localhost:5000/audit/audit_123/results
```

## 📊 Sample Output

### Technical SEO Results
```json
{
  "technical_seo": {
    "https_ssl": {
      "is_https": true,
      "ssl_valid": true,
      "status": "good",
      "recommendation": "HTTPS properly implemented"
    },
    "mobile_friendly": {
      "has_viewport_meta": true,
      "viewport_content": "width=device-width, initial-scale=1.0",
      "status": "good"
    },
    "structured_data": {
      "total_schemas": 5,
      "json_ld_scripts": [{"type": "Organization", "context": "https://schema.org"}],
      "status": "good"
    }
  }
}
```

### PageSpeed Insights Results
```json
{
  "pagespeed_insights": {
    "mobile": {
      "performance_score": 87,
      "core_web_vitals": {
        "lcp": {"value": 2.1, "status": "good", "ideal_range": "≤ 2.5s"},
        "cls": {"value": 0.05, "status": "good", "ideal_range": "≤ 0.1"},
        "inp": {"value": 180, "status": "good", "ideal_range": "≤ 200ms"}
      }
    }
  }
}
```

## 🛠️ Configuration

### Environment Variables
```bash
# Optional: Set default API key
export PAGESPEED_API_KEY=your_google_api_key

# Optional: Configure server port
export FLASK_PORT=5000
```

### Custom Configuration
Create `config.py` for advanced settings:
```python
# Custom timeout settings
REQUEST_TIMEOUT = 30
AUDIT_TIMEOUT = 300

# Custom user agent
USER_AGENT = "SEO-Audit-Tool/1.0"

# Enable debug mode
DEBUG = True
```

## 📋 Requirements

### Core Dependencies
- **requests**: HTTP requests and web scraping
- **beautifulsoup4**: HTML parsing and analysis
- **flask**: Web framework for interface
- **selenium**: Browser automation (optional)
- **python-whois**: Domain information retrieval
- **dnspython**: DNS lookups and validation

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB for dependencies
- **Network**: Internet connection for external analysis

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Test with sample websites:
```bash
# Test popular websites
python seo_audit.py
# Enter: https://google.com
# Enter: https://github.com
# Enter: https://stackoverflow.com
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 seo_audit.py

# Run type checking
mypy seo_audit.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [API Docs](http://localhost:5000/api/docs)
- **Issues**: [GitHub Issues](https://github.com/yourusername/seo-audit-tool/issues)
- **Discord**: [Community Server](https://discord.gg/seo-audit)
- **Email**: support@seoaudit.com

## 🔮 Roadmap

### Version 2.0 (Coming Soon)
- [ ] Advanced keyword analysis
- [ ] Competitor comparison
- [ ] Historical tracking
- [ ] PDF report generation
- [ ] WordPress plugin
- [ ] Chrome extension

### Version 1.1 (In Progress)
- [x] Web interface
- [x] API endpoints
- [x] CSV export
- [ ] Docker support
- [ ] Batch auditing
- [ ] Scheduled audits

## 🙏 Acknowledgments

- **Google PageSpeed Insights** for performance data
- **Lighthouse** for technical analysis framework
- **Schema.org** for structured data standards
- **WCAG** for accessibility guidelines
- **Bootstrap** for UI framework

## 📈 Performance

- **Audit Speed**: 30-60 seconds per website
- **Concurrent Audits**: Up to 10 simultaneous
- **Memory Usage**: ~50MB per audit
- **API Rate Limits**: 100 requests/hour (PageSpeed)

---

**Made with ❤️ for better web optimization**

*This tool helps developers, SEO professionals, and website owners improve their search engine rankings through comprehensive analysis and actionable recommendations.*