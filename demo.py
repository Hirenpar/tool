#!/usr/bin/env python3
"""
Demo script for Advanced SEO Audit Tool
Demonstrates all major features and capabilities
"""

import json
import time
from seo_audit import SEOAuditor

def demo_seo_audit():
    """Run demonstration of SEO audit features"""
    print("🚀 Advanced SEO Audit Tool - Demo")
    print("=" * 50)
    
    # Sample websites for testing
    demo_sites = [
        {
            'url': 'https://example.com',
            'description': 'Simple test site'
        },
        {
            'url': 'https://google.com', 
            'description': 'High-performance site'
        },
        {
            'url': 'https://github.com',
            'description': 'Developer platform'
        }
    ]
    
    print("\n📋 Available demo sites:")
    for i, site in enumerate(demo_sites, 1):
        print(f"{i}. {site['url']} - {site['description']}")
    
    print("\n4. Enter custom URL")
    print("5. Run all demo sites")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == '5':
        # Run all demo sites
        for site in demo_sites:
            run_audit_demo(site['url'])
    elif choice == '4':
        # Custom URL
        url = input("Enter website URL: ").strip()
        if url:
            run_audit_demo(url)
    elif choice in ['1', '2', '3']:
        # Selected demo site
        site = demo_sites[int(choice) - 1]
        run_audit_demo(site['url'])
    else:
        print("Invalid selection")

def run_audit_demo(url):
    """Run comprehensive audit demonstration"""
    print(f"\n🔍 Starting audit for: {url}")
    print("-" * 40)
    
    # Initialize auditor (without API key for demo)
    auditor = SEOAuditor()
    
    # Run audit
    start_time = time.time()
    results = auditor.audit_website(url)
    audit_time = time.time() - start_time
    
    # Display results summary
    print(f"\n✅ Audit completed in {audit_time:.2f} seconds")
    print("\n📊 AUDIT SUMMARY")
    print("=" * 30)
    
    # Technical SEO highlights
    if 'technical_seo' in results:
        print("\n🔧 Technical SEO Highlights:")
        tech_seo = results['technical_seo']
        
        if 'https_ssl' in tech_seo:
            https_status = "✅ HTTPS" if tech_seo['https_ssl'].get('is_https') else "❌ HTTP only"
            print(f"  • Security: {https_status}")
        
        if 'mobile_friendly' in tech_seo:
            mobile_status = "✅ Mobile-friendly" if tech_seo['mobile_friendly'].get('has_viewport_meta') else "⚠️ Needs mobile optimization"
            print(f"  • Mobile: {mobile_status}")
        
        if 'structured_data' in tech_seo:
            schema_count = tech_seo['structured_data'].get('total_schemas', 0)
            print(f"  • Structured Data: {schema_count} schemas found")
        
        if 'broken_links' in tech_seo:
            broken_count = tech_seo['broken_links'].get('broken_count', 0)
            link_status = "✅ No broken links" if broken_count == 0 else f"⚠️ {broken_count} broken links"
            print(f"  • Links: {link_status}")
    
    # On-Page SEO highlights
    if 'on_page_seo' in results:
        print("\n📝 On-Page SEO Highlights:")
        on_page = results['on_page_seo']
        
        if 'title_tags' in on_page:
            title_length = on_page['title_tags'].get('length', 0)
            title_status = "✅ Optimal" if 30 <= title_length <= 60 else f"⚠️ {title_length} chars"
            print(f"  • Title Tag: {title_status}")
        
        if 'meta_description' in on_page:
            desc_exists = on_page['meta_description'].get('exists', False)
            desc_status = "✅ Present" if desc_exists else "❌ Missing"
            print(f"  • Meta Description: {desc_status}")
        
        if 'heading_structure' in on_page:
            h1_count = on_page['heading_structure'].get('h1_count', 0)
            h1_status = "✅ Single H1" if h1_count == 1 else f"⚠️ {h1_count} H1 tags"
            print(f"  • Heading Structure: {h1_status}")
        
        if 'image_optimization' in on_page:
            alt_percentage = on_page['image_optimization'].get('alt_percentage', 0)
            alt_status = "✅ Good" if alt_percentage >= 90 else f"⚠️ {alt_percentage}% have alt text"
            print(f"  • Image Alt Text: {alt_status}")
    
    # User Experience highlights
    if 'user_experience' in results:
        print("\n👤 User Experience Highlights:")
        ux = results['user_experience']
        
        if 'accessibility' in ux:
            acc_score = ux['accessibility'].get('accessibility_score', 0)
            acc_status = "✅ Good" if acc_score >= 70 else f"⚠️ {acc_score}/100"
            print(f"  • Accessibility Score: {acc_status}")
        
        if 'responsive_design' in ux:
            responsive = ux['responsive_design'].get('has_viewport_meta', False)
            resp_status = "✅ Responsive" if responsive else "⚠️ Not responsive"
            print(f"  • Responsive Design: {resp_status}")
    
    # Security & Performance highlights
    if 'security_performance' in results:
        print("\n🔒 Security & Performance Highlights:")
        security = results['security_performance']
        
        if 'security_headers' in security:
            sec_score = security['security_headers'].get('security_score', 0)
            sec_status = "✅ Good" if sec_score >= 70 else f"⚠️ {sec_score}/100"
            print(f"  • Security Headers: {sec_status}")
        
        if 'performance_enhancements' in security:
            perf_score = security['performance_enhancements'].get('performance_score', 0)
            perf_status = "✅ Optimized" if perf_score >= 70 else f"⚠️ {perf_score}/100"
            print(f"  • Performance: {perf_status}")
    
    # Overall scores
    if 'scores' in results:
        print("\n⭐ Overall Scores:")
        scores = results['scores']
        for score_name, score_value in scores.items():
            if score_name != 'calculation_error' and score_value > 0:
                score_display = score_name.replace('_', ' ').title()
                score_status = get_score_status(score_value)
                print(f"  • {score_display}: {score_value}/100 {score_status}")
    
    # Top recommendations
    print("\n💡 Top Recommendations:")
    recommendations = generate_recommendations(results)
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"  {i}. {rec}")
    
    # Save results
    filename = f"demo_audit_{results.get('domain', 'unknown')}_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {filename}")
    
    # Option to view detailed report
    view_detail = input("\nView detailed report? (y/n): ").strip().lower()
    if view_detail == 'y':
        detailed_report = auditor.generate_report()
        print("\n" + "="*60)
        print(detailed_report)
        print("="*60)

def get_score_status(score):
    """Get emoji status for score"""
    if score >= 80:
        return "🟢"
    elif score >= 60:
        return "🟡"
    else:
        return "🔴"

def generate_recommendations(results):
    """Generate prioritized recommendations based on audit results"""
    recommendations = []
    
    # Check for critical issues
    if 'technical_seo' in results:
        tech = results['technical_seo']
        
        if tech.get('https_ssl', {}).get('status') != 'good':
            recommendations.append("🔴 CRITICAL: Implement HTTPS/SSL security")
        
        if not tech.get('mobile_friendly', {}).get('has_viewport_meta'):
            recommendations.append("🔴 CRITICAL: Add viewport meta tag for mobile")
        
        if not tech.get('xml_sitemap', {}).get('exists'):
            recommendations.append("🟡 HIGH: Create and submit XML sitemap")
        
        if tech.get('structured_data', {}).get('total_schemas', 0) == 0:
            recommendations.append("🟡 MEDIUM: Add structured data markup")
    
    if 'on_page_seo' in results:
        on_page = results['on_page_seo']
        
        if not on_page.get('meta_description', {}).get('exists'):
            recommendations.append("🔴 HIGH: Add meta description")
        
        title_length = on_page.get('title_tags', {}).get('length', 0)
        if not (30 <= title_length <= 60):
            recommendations.append("🟡 MEDIUM: Optimize title tag length (30-60 chars)")
        
        alt_percentage = on_page.get('image_optimization', {}).get('alt_percentage', 0)
        if alt_percentage < 90:
            recommendations.append("🟡 MEDIUM: Add alt text to all images")
    
    if 'security_performance' in results:
        security = results['security_performance']
        
        sec_score = security.get('security_headers', {}).get('security_score', 0)
        if sec_score < 70:
            recommendations.append("🟡 MEDIUM: Implement security headers")
        
        perf_score = security.get('performance_enhancements', {}).get('performance_score', 0)
        if perf_score < 70:
            recommendations.append("🟡 MEDIUM: Optimize performance (compression, caching)")
    
    # Add default recommendations if none found
    if not recommendations:
        recommendations.extend([
            "✅ Great! Your website is well-optimized",
            "🚀 Consider adding more structured data for rich snippets",
            "📱 Test mobile user experience regularly",
            "⚡ Monitor Core Web Vitals performance",
            "🔄 Schedule regular SEO audits"
        ])
    
    return recommendations

def demo_api_features():
    """Demonstrate API integration features"""
    print("\n🌐 API Integration Demo")
    print("-" * 30)
    
    print("The SEO Audit Tool provides RESTful API endpoints:")
    print("• POST /audit - Start new audit")
    print("• GET /audit/{id}/status - Check status")
    print("• GET /audit/{id}/results - Get results")
    print("• GET /audit/{id}/download/json - Download JSON")
    print("• GET /audit/{id}/download/csv - Download CSV")
    
    print("\nExample API usage:")
    print("curl -X POST http://localhost:5000/audit \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"url\": \"https://example.com\"}'")

if __name__ == "__main__":
    try:
        demo_seo_audit()
        
        # Optional API demo
        api_demo = input("\nShow API integration demo? (y/n): ").strip().lower()
        if api_demo == 'y':
            demo_api_features()
        
        print("\n🎉 Demo completed! Thank you for trying the SEO Audit Tool.")
        print("📚 For more information, visit: http://localhost:5000/api/docs")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying the SEO Audit Tool!")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        print("This might be due to missing dependencies or network issues.")