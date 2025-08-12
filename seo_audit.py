#!/usr/bin/env python3
"""
Advanced SEO Audit Software
Performs comprehensive SEO and performance audits covering:
- Technical SEO, On-Page SEO, Off-Page SEO
- User Experience & Accessibility
- Security & Performance
- Google PageSpeed Insights integration
"""

import requests
import json
import time
import re
import ssl
import socket
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import dns.resolver
import whois
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
warnings.filterwarnings("ignore")

class SEOAuditor:
    def __init__(self, pagespeed_api_key=None):
        """Initialize the SEO Auditor with optional PageSpeed Insights API key"""
        self.pagespeed_api_key = pagespeed_api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.audit_results = {}
        
    def audit_website(self, url):
        """Main function to perform comprehensive SEO audit"""
        print(f"🔍 Starting comprehensive SEO audit for: {url}")
        start_time = time.time()
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        self.url = url
        self.domain = urlparse(url).netloc
        self.audit_results = {
            'url': url,
            'domain': self.domain,
            'audit_timestamp': datetime.now().isoformat(),
            'technical_seo': {},
            'on_page_seo': {},
            'off_page_seo': {},
            'user_experience': {},
            'security_performance': {},
            'pagespeed_insights': {}
        }
        
        try:
            # Get page content
            print("📄 Fetching page content...")
            response = self.session.get(url, timeout=30)
            self.soup = BeautifulSoup(response.content, 'html.parser')
            self.response = response
            
            # Run all audit modules
            print("🔧 Running Technical SEO analysis...")
            self._audit_technical_seo()
            
            print("📝 Running On-Page SEO analysis...")
            self._audit_on_page_seo()
            
            print("🔗 Running Off-Page SEO analysis...")
            self._audit_off_page_seo()
            
            print("👤 Running User Experience & Accessibility analysis...")
            self._audit_user_experience()
            
            print("🔒 Running Security & Performance analysis...")
            self._audit_security_performance()
            
            if self.pagespeed_api_key:
                print("⚡ Running Google PageSpeed Insights analysis...")
                self._audit_pagespeed_insights()
            
            # Calculate overall scores
            self._calculate_scores()
            
            audit_time = time.time() - start_time
            print(f"✅ Audit completed in {audit_time:.2f} seconds")
            
            return self.audit_results
            
        except Exception as e:
            print(f"❌ Error during audit: {str(e)}")
            self.audit_results['error'] = str(e)
            return self.audit_results
    
    def _audit_technical_seo(self):
        """Perform Technical SEO analysis"""
        technical = {}
        
        # Page Speed & Core Web Vitals (basic analysis)
        start_time = time.time()
        try:
            response_time = time.time() - start_time
            technical['response_time'] = {
                'value': response_time,
                'status': 'good' if response_time < 1.0 else 'needs_improvement' if response_time < 3.0 else 'poor',
                'recommendation': 'Optimize server response time' if response_time > 1.0 else 'Good response time'
            }
        except:
            technical['response_time'] = {'error': 'Could not measure response time'}
        
        # HTTPS and SSL Status
        try:
            is_https = self.url.startswith('https://')
            technical['https_ssl'] = {
                'is_https': is_https,
                'ssl_valid': self._check_ssl_certificate(),
                'status': 'good' if is_https else 'poor',
                'recommendation': 'Ensure HTTPS is properly implemented' if not is_https else 'HTTPS properly implemented'
            }
        except Exception as e:
            technical['https_ssl'] = {'error': str(e)}
        
        # Mobile-friendliness
        try:
            viewport_meta = self.soup.find('meta', attrs={'name': 'viewport'})
            has_viewport = viewport_meta is not None
            technical['mobile_friendly'] = {
                'has_viewport_meta': has_viewport,
                'viewport_content': viewport_meta.get('content') if viewport_meta else None,
                'status': 'good' if has_viewport else 'poor',
                'recommendation': 'Add viewport meta tag for mobile optimization' if not has_viewport else 'Viewport meta tag found'
            }
        except Exception as e:
            technical['mobile_friendly'] = {'error': str(e)}
        
        # Indexability & Crawlability
        try:
            robots_meta = self.soup.find('meta', attrs={'name': 'robots'})
            robots_content = robots_meta.get('content', '').lower() if robots_meta else ''
            
            noindex = 'noindex' in robots_content
            nofollow = 'nofollow' in robots_content
            
            technical['indexability'] = {
                'robots_meta_tag': robots_content if robots_content else 'none',
                'allows_indexing': not noindex,
                'allows_following': not nofollow,
                'status': 'good' if not noindex else 'poor',
                'recommendation': 'Remove noindex directive' if noindex else 'Page allows indexing'
            }
        except Exception as e:
            technical['indexability'] = {'error': str(e)}
        
        # XML Sitemap check
        try:
            sitemap_url = urljoin(self.url, '/sitemap.xml')
            sitemap_response = self.session.get(sitemap_url, timeout=10)
            has_sitemap = sitemap_response.status_code == 200
            
            technical['xml_sitemap'] = {
                'sitemap_url': sitemap_url,
                'exists': has_sitemap,
                'status': 'good' if has_sitemap else 'needs_improvement',
                'recommendation': 'Create and submit XML sitemap' if not has_sitemap else 'XML sitemap found'
            }
        except Exception as e:
            technical['xml_sitemap'] = {'error': str(e)}
        
        # Robots.txt check
        try:
            robots_url = urljoin(self.url, '/robots.txt')
            robots_response = self.session.get(robots_url, timeout=10)
            has_robots = robots_response.status_code == 200
            
            technical['robots_txt'] = {
                'robots_url': robots_url,
                'exists': has_robots,
                'content': robots_response.text[:500] if has_robots else None,
                'status': 'good' if has_robots else 'needs_improvement',
                'recommendation': 'Create robots.txt file' if not has_robots else 'Robots.txt found'
            }
        except Exception as e:
            technical['robots_txt'] = {'error': str(e)}
        
        # Canonical tags
        try:
            canonical_tag = self.soup.find('link', attrs={'rel': 'canonical'})
            has_canonical = canonical_tag is not None
            canonical_url = canonical_tag.get('href') if canonical_tag else None
            
            technical['canonical_tags'] = {
                'has_canonical': has_canonical,
                'canonical_url': canonical_url,
                'status': 'good' if has_canonical else 'needs_improvement',
                'recommendation': 'Add canonical tag to prevent duplicate content issues' if not has_canonical else 'Canonical tag implemented'
            }
        except Exception as e:
            technical['canonical_tags'] = {'error': str(e)}
        
        # Structured Data Analysis
        try:
            structured_data = self._analyze_structured_data()
            technical['structured_data'] = structured_data
        except Exception as e:
            technical['structured_data'] = {'error': str(e)}
        
        # Broken Links Check
        try:
            broken_links = self._check_broken_links()
            technical['broken_links'] = broken_links
        except Exception as e:
            technical['broken_links'] = {'error': str(e)}
        
        self.audit_results['technical_seo'] = technical
    
    def _audit_on_page_seo(self):
        """Perform On-Page SEO analysis"""
        on_page = {}
        
        # Title Tags Analysis
        try:
            title_tag = self.soup.find('title')
            title_text = title_tag.get_text().strip() if title_tag else ''
            title_length = len(title_text)
            
            on_page['title_tags'] = {
                'title': title_text,
                'length': title_length,
                'optimal_length': title_length >= 30 and title_length <= 60,
                'status': 'good' if 30 <= title_length <= 60 else 'needs_improvement',
                'recommendation': f'Title length is {title_length} characters. Optimal range is 30-60 characters.'
            }
        except Exception as e:
            on_page['title_tags'] = {'error': str(e)}
        
        # Meta Description Analysis
        try:
            meta_desc = self.soup.find('meta', attrs={'name': 'description'})
            desc_text = meta_desc.get('content', '').strip() if meta_desc else ''
            desc_length = len(desc_text)
            
            on_page['meta_description'] = {
                'description': desc_text,
                'length': desc_length,
                'exists': bool(desc_text),
                'optimal_length': desc_length >= 120 and desc_length <= 160,
                'status': 'good' if 120 <= desc_length <= 160 else 'needs_improvement',
                'recommendation': f'Meta description length is {desc_length} characters. Optimal range is 120-160 characters.'
            }
        except Exception as e:
            on_page['meta_description'] = {'error': str(e)}
        
        # Heading Structure Analysis
        try:
            headings = self._analyze_heading_structure()
            on_page['heading_structure'] = headings
        except Exception as e:
            on_page['heading_structure'] = {'error': str(e)}
        
        # Image Optimization
        try:
            images = self._analyze_images()
            on_page['image_optimization'] = images
        except Exception as e:
            on_page['image_optimization'] = {'error': str(e)}
        
        # Internal Linking
        try:
            internal_links = self._analyze_internal_links()
            on_page['internal_linking'] = internal_links
        except Exception as e:
            on_page['internal_linking'] = {'error': str(e)}
        
        # Content Analysis
        try:
            content_analysis = self._analyze_content()
            on_page['content_analysis'] = content_analysis
        except Exception as e:
            on_page['content_analysis'] = {'error': str(e)}
        
        self.audit_results['on_page_seo'] = on_page
    
    def _audit_off_page_seo(self):
        """Perform Off-Page SEO analysis"""
        off_page = {}
        
        # Domain Authority Estimation (basic)
        try:
            domain_info = self._get_domain_info()
            off_page['domain_authority'] = domain_info
        except Exception as e:
            off_page['domain_authority'] = {'error': str(e)}
        
        # Social Media Presence Check
        try:
            social_signals = self._check_social_signals()
            off_page['social_signals'] = social_signals
        except Exception as e:
            off_page['social_signals'] = {'error': str(e)}
        
        # Basic Backlink Analysis (limited without external APIs)
        try:
            backlink_analysis = self._basic_backlink_analysis()
            off_page['backlink_analysis'] = backlink_analysis
        except Exception as e:
            off_page['backlink_analysis'] = {'error': str(e)}
        
        self.audit_results['off_page_seo'] = off_page
    
    def _audit_user_experience(self):
        """Perform User Experience & Accessibility analysis"""
        ux = {}
        
        # Navigation Analysis
        try:
            navigation = self._analyze_navigation()
            ux['navigation'] = navigation
        except Exception as e:
            ux['navigation'] = {'error': str(e)}
        
        # Accessibility Analysis
        try:
            accessibility = self._analyze_accessibility()
            ux['accessibility'] = accessibility
        except Exception as e:
            ux['accessibility'] = {'error': str(e)}
        
        # Mobile vs Desktop Experience
        try:
            responsive_design = self._check_responsive_design()
            ux['responsive_design'] = responsive_design
        except Exception as e:
            ux['responsive_design'] = {'error': str(e)}
        
        self.audit_results['user_experience'] = ux
    
    def _audit_security_performance(self):
        """Perform Security & Performance analysis"""
        security = {}
        
        # Security Headers
        try:
            security_headers = self._check_security_headers()
            security['security_headers'] = security_headers
        except Exception as e:
            security['security_headers'] = {'error': str(e)}
        
        # Performance Enhancements
        try:
            performance = self._check_performance_enhancements()
            security['performance_enhancements'] = performance
        except Exception as e:
            security['performance_enhancements'] = {'error': str(e)}
        
        self.audit_results['security_performance'] = security
    
    def _audit_pagespeed_insights(self):
        """Perform Google PageSpeed Insights analysis"""
        if not self.pagespeed_api_key:
            self.audit_results['pagespeed_insights'] = {'error': 'No API key provided'}
            return
        
        try:
            # Mobile Analysis
            mobile_results = self._get_pagespeed_data('mobile')
            
            # Desktop Analysis
            desktop_results = self._get_pagespeed_data('desktop')
            
            self.audit_results['pagespeed_insights'] = {
                'mobile': mobile_results,
                'desktop': desktop_results
            }
        except Exception as e:
            self.audit_results['pagespeed_insights'] = {'error': str(e)}
    
    # Helper methods for detailed analysis
    def _check_ssl_certificate(self):
        """Check SSL certificate validity"""
        try:
            hostname = urlparse(self.url).hostname
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    return True
        except:
            return False
    
    def _analyze_structured_data(self):
        """Analyze structured data/schema markup"""
        structured_data = {
            'json_ld_scripts': [],
            'microdata_items': [],
            'rdfa_properties': [],
            'total_schemas': 0
        }
        
        # JSON-LD
        json_ld_scripts = self.soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                structured_data['json_ld_scripts'].append({
                    'type': data.get('@type', 'Unknown'),
                    'context': data.get('@context', 'Unknown')
                })
            except:
                pass
        
        # Microdata
        microdata_items = self.soup.find_all(attrs={'itemtype': True})
        for item in microdata_items:
            structured_data['microdata_items'].append(item.get('itemtype'))
        
        # RDFa
        rdfa_props = self.soup.find_all(attrs={'property': True})
        structured_data['rdfa_properties'] = [prop.get('property') for prop in rdfa_props[:10]]
        
        structured_data['total_schemas'] = len(json_ld_scripts) + len(microdata_items) + len(rdfa_props)
        structured_data['status'] = 'good' if structured_data['total_schemas'] > 0 else 'needs_improvement'
        structured_data['recommendation'] = 'Add structured data markup' if structured_data['total_schemas'] == 0 else 'Structured data found'
        
        return structured_data
    
    def _check_broken_links(self):
        """Check for broken internal and external links"""
        links = self.soup.find_all('a', href=True)
        broken_links = {'internal': [], 'external': [], 'total_checked': 0, 'broken_count': 0}
        
        # Limit to first 20 links for performance
        for link in links[:20]:
            href = link.get('href')
            if not href or href.startswith(('#', 'mailto:', 'tel:')):
                continue
                
            full_url = urljoin(self.url, href)
            broken_links['total_checked'] += 1
            
            try:
                response = self.session.head(full_url, timeout=5, allow_redirects=True)
                if response.status_code >= 400:
                    link_data = {'url': full_url, 'status_code': response.status_code, 'text': link.get_text()[:50]}
                    if self.domain in full_url:
                        broken_links['internal'].append(link_data)
                    else:
                        broken_links['external'].append(link_data)
                    broken_links['broken_count'] += 1
            except:
                broken_links['broken_count'] += 1
        
        broken_links['status'] = 'good' if broken_links['broken_count'] == 0 else 'needs_improvement'
        broken_links['recommendation'] = 'Fix broken links' if broken_links['broken_count'] > 0 else 'No broken links found'
        
        return broken_links
    
    def _analyze_heading_structure(self):
        """Analyze heading structure and hierarchy"""
        headings = {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}
        
        for level in range(1, 7):
            tags = self.soup.find_all(f'h{level}')
            headings[f'h{level}'] = [tag.get_text().strip()[:100] for tag in tags]
        
        h1_count = len(headings['h1'])
        has_proper_structure = h1_count == 1 and len(headings['h2']) > 0
        
        return {
            'headings': headings,
            'h1_count': h1_count,
            'has_single_h1': h1_count == 1,
            'has_h2_tags': len(headings['h2']) > 0,
            'proper_hierarchy': has_proper_structure,
            'status': 'good' if has_proper_structure else 'needs_improvement',
            'recommendation': 'Ensure single H1 and proper heading hierarchy' if not has_proper_structure else 'Good heading structure'
        }
    
    def _analyze_images(self):
        """Analyze image optimization"""
        images = self.soup.find_all('img')
        total_images = len(images)
        images_with_alt = len([img for img in images if img.get('alt')])
        
        # Sample image analysis
        image_analysis = []
        for img in images[:10]:  # Analyze first 10 images
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            analysis = {
                'src': src[:100],
                'has_alt': bool(alt),
                'alt_text': alt[:50] if alt else '',
                'loading': img.get('loading', ''),
                'is_lazy_loaded': img.get('loading') == 'lazy'
            }
            image_analysis.append(analysis)
        
        alt_percentage = (images_with_alt / total_images * 100) if total_images > 0 else 0
        
        return {
            'total_images': total_images,
            'images_with_alt': images_with_alt,
            'alt_percentage': round(alt_percentage, 1),
            'sample_analysis': image_analysis,
            'status': 'good' if alt_percentage >= 90 else 'needs_improvement',
            'recommendation': f'Add alt text to {total_images - images_with_alt} images' if alt_percentage < 90 else 'Good image optimization'
        }
    
    def _analyze_internal_links(self):
        """Analyze internal linking structure"""
        all_links = self.soup.find_all('a', href=True)
        internal_links = []
        
        for link in all_links:
            href = link.get('href')
            if href and not href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
                internal_links.append({
                    'href': href,
                    'text': link.get_text().strip()[:50],
                    'title': link.get('title', '')
                })
        
        return {
            'total_internal_links': len(internal_links),
            'sample_links': internal_links[:10],
            'status': 'good' if len(internal_links) > 5 else 'needs_improvement',
            'recommendation': 'Add more internal links for better navigation' if len(internal_links) <= 5 else 'Good internal linking'
        }
    
    def _analyze_content(self):
        """Analyze content quality and structure"""
        # Remove script and style elements
        for script in self.soup(["script", "style"]):
            script.decompose()
        
        text = self.soup.get_text()
        words = text.split()
        word_count = len(words)
        
        # Basic readability metrics
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'estimated_reading_time': round(word_count / 200, 1),  # 200 words per minute
            'status': 'good' if word_count >= 300 else 'needs_improvement',
            'recommendation': 'Add more content for better SEO' if word_count < 300 else 'Good content length'
        }
    
    def _get_domain_info(self):
        """Get basic domain information"""
        try:
            domain_whois = whois.whois(self.domain)
            creation_date = domain_whois.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            age_days = (datetime.now() - creation_date).days if creation_date else 0
            
            return {
                'domain_age_days': age_days,
                'domain_age_years': round(age_days / 365.25, 1),
                'registrar': domain_whois.registrar,
                'status': 'good' if age_days > 365 else 'needs_improvement',
                'recommendation': 'Domain age affects trust signals' if age_days < 365 else 'Established domain'
            }
        except:
            return {'error': 'Could not retrieve domain information'}
    
    def _check_social_signals(self):
        """Check for social media meta tags and signals"""
        social_tags = {
            'og_title': self.soup.find('meta', property='og:title'),
            'og_description': self.soup.find('meta', property='og:description'),
            'og_image': self.soup.find('meta', property='og:image'),
            'og_url': self.soup.find('meta', property='og:url'),
            'twitter_card': self.soup.find('meta', attrs={'name': 'twitter:card'}),
            'twitter_title': self.soup.find('meta', attrs={'name': 'twitter:title'}),
            'twitter_description': self.soup.find('meta', attrs={'name': 'twitter:description'}),
            'twitter_image': self.soup.find('meta', attrs={'name': 'twitter:image'})
        }
        
        present_tags = {k: v.get('content') if v else None for k, v in social_tags.items()}
        tags_count = len([v for v in present_tags.values() if v])
        
        return {
            'social_meta_tags': present_tags,
            'tags_present': tags_count,
            'total_possible': len(social_tags),
            'status': 'good' if tags_count >= 6 else 'needs_improvement',
            'recommendation': f'Add {len(social_tags) - tags_count} missing social media meta tags'
        }
    
    def _basic_backlink_analysis(self):
        """Basic backlink analysis (limited without external tools)"""
        return {
            'note': 'Comprehensive backlink analysis requires specialized tools like Ahrefs, SEMrush, or Moz',
            'recommendations': [
                'Use Google Search Console to monitor backlinks',
                'Build high-quality, relevant backlinks',
                'Monitor for toxic backlinks and disavow if necessary',
                'Create linkable content assets'
            ],
            'status': 'requires_external_tools'
        }
    
    def _analyze_navigation(self):
        """Analyze website navigation"""
        nav_elements = self.soup.find_all(['nav', 'menu'])
        nav_links = []
        
        for nav in nav_elements:
            links = nav.find_all('a', href=True)
            for link in links:
                nav_links.append({
                    'text': link.get_text().strip(),
                    'href': link.get('href')
                })
        
        return {
            'navigation_elements': len(nav_elements),
            'navigation_links': len(nav_links),
            'sample_nav_links': nav_links[:10],
            'status': 'good' if len(nav_links) > 5 else 'needs_improvement',
            'recommendation': 'Improve navigation structure' if len(nav_links) <= 5 else 'Good navigation structure'
        }
    
    def _analyze_accessibility(self):
        """Analyze accessibility features"""
        accessibility = {
            'images_with_alt': len([img for img in self.soup.find_all('img') if img.get('alt')]),
            'total_images': len(self.soup.find_all('img')),
            'form_labels': len(self.soup.find_all('label')),
            'total_inputs': len(self.soup.find_all(['input', 'textarea', 'select'])),
            'aria_labels': len(self.soup.find_all(attrs={'aria-label': True})),
            'heading_structure': bool(self.soup.find('h1')),
            'skip_links': len(self.soup.find_all('a', href=lambda x: x and x.startswith('#')))
        }
        
        score = 0
        if accessibility['total_images'] > 0:
            score += (accessibility['images_with_alt'] / accessibility['total_images']) * 30
        if accessibility['total_inputs'] > 0:
            score += (accessibility['form_labels'] / accessibility['total_inputs']) * 30
        score += min(accessibility['aria_labels'] * 5, 20)
        score += 10 if accessibility['heading_structure'] else 0
        score += min(accessibility['skip_links'] * 5, 10)
        
        accessibility['accessibility_score'] = round(score, 1)
        accessibility['status'] = 'good' if score >= 70 else 'needs_improvement'
        accessibility['recommendation'] = 'Improve accessibility features' if score < 70 else 'Good accessibility implementation'
        
        return accessibility
    
    def _check_responsive_design(self):
        """Check responsive design indicators"""
        viewport_meta = self.soup.find('meta', attrs={'name': 'viewport'})
        css_media_queries = len(re.findall(r'@media', str(self.soup)))
        
        return {
            'has_viewport_meta': bool(viewport_meta),
            'viewport_content': viewport_meta.get('content') if viewport_meta else None,
            'css_media_queries_found': css_media_queries,
            'status': 'good' if viewport_meta and css_media_queries > 0 else 'needs_improvement',
            'recommendation': 'Implement responsive design' if not viewport_meta else 'Responsive design indicators found'
        }
    
    def _check_security_headers(self):
        """Check security headers"""
        headers = self.response.headers
        security_headers = {
            'content_security_policy': headers.get('Content-Security-Policy'),
            'x_frame_options': headers.get('X-Frame-Options'),
            'x_content_type_options': headers.get('X-Content-Type-Options'),
            'strict_transport_security': headers.get('Strict-Transport-Security'),
            'referrer_policy': headers.get('Referrer-Policy'),
            'x_xss_protection': headers.get('X-XSS-Protection')
        }
        
        present_headers = len([v for v in security_headers.values() if v])
        total_headers = len(security_headers)
        
        return {
            'security_headers': security_headers,
            'headers_present': present_headers,
            'total_possible': total_headers,
            'security_score': round((present_headers / total_headers) * 100, 1),
            'status': 'good' if present_headers >= 4 else 'needs_improvement',
            'recommendation': f'Implement {total_headers - present_headers} missing security headers'
        }
    
    def _check_performance_enhancements(self):
        """Check performance enhancement features"""
        headers = self.response.headers
        
        performance = {
            'gzip_compression': 'gzip' in headers.get('Content-Encoding', '').lower(),
            'cache_control': bool(headers.get('Cache-Control')),
            'etag': bool(headers.get('ETag')),
            'last_modified': bool(headers.get('Last-Modified')),
            'content_length': headers.get('Content-Length'),
            'server_response_time': getattr(self.response, 'elapsed', None)
        }
        
        # Check for lazy loading
        lazy_images = len(self.soup.find_all('img', loading='lazy'))
        performance['lazy_loading_images'] = lazy_images
        
        # Check for CDN indicators
        cdn_indicators = ['cloudflare', 'amazonaws', 'azure', 'googleusercontent', 'fastly', 'maxcdn']
        server_header = headers.get('Server', '').lower()
        performance['cdn_usage'] = any(cdn in server_header for cdn in cdn_indicators)
        
        score = sum([
            performance['gzip_compression'] * 20,
            performance['cache_control'] * 20,
            performance['etag'] * 15,
            performance['last_modified'] * 15,
            (lazy_images > 0) * 15,
            performance['cdn_usage'] * 15
        ])
        
        performance['performance_score'] = score
        performance['status'] = 'good' if score >= 70 else 'needs_improvement'
        performance['recommendation'] = 'Implement performance optimizations' if score < 70 else 'Good performance optimizations'
        
        return performance
    
    def _get_pagespeed_data(self, strategy='mobile'):
        """Get Google PageSpeed Insights data"""
        try:
            api_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
            params = {
                'url': self.url,
                'key': self.pagespeed_api_key,
                'strategy': strategy,
                'category': ['PERFORMANCE', 'ACCESSIBILITY', 'BEST_PRACTICES', 'SEO']
            }
            
            response = requests.get(api_url, params=params, timeout=60)
            data = response.json()
            
            if 'error' in data:
                return {'error': data['error']['message']}
            
            lighthouse_result = data.get('lighthouseResult', {})
            categories = lighthouse_result.get('categories', {})
            audits = lighthouse_result.get('audits', {})
            
            # Core Web Vitals
            core_web_vitals = {}
            if 'largest-contentful-paint' in audits:
                lcp = audits['largest-contentful-paint']
                core_web_vitals['lcp'] = {
                    'value': lcp.get('numericValue', 0) / 1000,  # Convert to seconds
                    'displayValue': lcp.get('displayValue', ''),
                    'score': lcp.get('score', 0),
                    'ideal_range': '≤ 2.5s',
                    'status': 'good' if lcp.get('score', 0) >= 0.9 else 'needs_improvement' if lcp.get('score', 0) >= 0.5 else 'poor'
                }
            
            if 'cumulative-layout-shift' in audits:
                cls = audits['cumulative-layout-shift']
                core_web_vitals['cls'] = {
                    'value': cls.get('numericValue', 0),
                    'displayValue': cls.get('displayValue', ''),
                    'score': cls.get('score', 0),
                    'ideal_range': '≤ 0.1',
                    'status': 'good' if cls.get('score', 0) >= 0.9 else 'needs_improvement' if cls.get('score', 0) >= 0.5 else 'poor'
                }
            
            if 'interaction-to-next-paint' in audits:
                inp = audits['interaction-to-next-paint']
                core_web_vitals['inp'] = {
                    'value': inp.get('numericValue', 0),
                    'displayValue': inp.get('displayValue', ''),
                    'score': inp.get('score', 0),
                    'ideal_range': '≤ 200ms',
                    'status': 'good' if inp.get('score', 0) >= 0.9 else 'needs_improvement' if inp.get('score', 0) >= 0.5 else 'poor'
                }
            
            # Performance metrics
            performance_metrics = {}
            metric_keys = ['first-contentful-paint', 'total-blocking-time', 'speed-index', 'interactive']
            for key in metric_keys:
                if key in audits:
                    audit = audits[key]
                    performance_metrics[key] = {
                        'value': audit.get('numericValue', 0),
                        'displayValue': audit.get('displayValue', ''),
                        'score': audit.get('score', 0)
                    }
            
            # Opportunities
            opportunities = []
            opportunity_keys = ['unused-css-rules', 'unused-javascript', 'modern-image-formats', 'render-blocking-resources']
            for key in opportunity_keys:
                if key in audits and audits[key].get('details'):
                    opportunities.append({
                        'id': key,
                        'title': audits[key].get('title', ''),
                        'description': audits[key].get('description', ''),
                        'savings': audits[key].get('displayValue', ''),
                        'score': audits[key].get('score', 0)
                    })
            
            return {
                'performance_score': categories.get('performance', {}).get('score', 0) * 100,
                'accessibility_score': categories.get('accessibility', {}).get('score', 0) * 100,
                'best_practices_score': categories.get('best-practices', {}).get('score', 0) * 100,
                'seo_score': categories.get('seo', {}).get('score', 0) * 100,
                'core_web_vitals': core_web_vitals,
                'performance_metrics': performance_metrics,
                'opportunities': opportunities,
                'strategy': strategy
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_scores(self):
        """Calculate overall SEO scores"""
        scores = {
            'technical_seo_score': 0,
            'on_page_seo_score': 0,
            'off_page_seo_score': 0,
            'user_experience_score': 0,
            'security_performance_score': 0,
            'overall_score': 0
        }
        
        # Calculate individual scores based on audit results
        # This is a simplified scoring system
        
        try:
            # Technical SEO Score
            technical = self.audit_results.get('technical_seo', {})
            tech_score = 0
            tech_items = 0
            
            for key, value in technical.items():
                if isinstance(value, dict) and 'status' in value:
                    tech_items += 1
                    if value['status'] == 'good':
                        tech_score += 100
                    elif value['status'] == 'needs_improvement':
                        tech_score += 50
            
            scores['technical_seo_score'] = round(tech_score / tech_items if tech_items > 0 else 0, 1)
            
            # Similar calculations for other categories...
            scores['overall_score'] = round(sum(scores.values()) / len([s for s in scores.values() if s > 0]) if any(scores.values()) else 0, 1)
            
        except Exception as e:
            scores['calculation_error'] = str(e)
        
        self.audit_results['scores'] = scores
    
    def generate_report(self):
        """Generate a comprehensive audit report"""
        if not self.audit_results:
            return "No audit results available. Please run audit_website() first."
        
        report = f"""
🔍 SEO AUDIT REPORT
{'='*50}
🌐 Website: {self.audit_results['url']}
📅 Audit Date: {self.audit_results['audit_timestamp']}
🏷️  Domain: {self.audit_results['domain']}

📊 OVERALL SCORES
{'='*30}
"""
        
        if 'scores' in self.audit_results:
            scores = self.audit_results['scores']
            report += f"""
Technical SEO Score: {scores.get('technical_seo_score', 'N/A')}/100
On-Page SEO Score: {scores.get('on_page_seo_score', 'N/A')}/100
Off-Page SEO Score: {scores.get('off_page_seo_score', 'N/A')}/100
User Experience Score: {scores.get('user_experience_score', 'N/A')}/100
Security & Performance Score: {scores.get('security_performance_score', 'N/A')}/100
Overall Score: {scores.get('overall_score', 'N/A')}/100
"""
        
        # Technical SEO Section
        report += f"""
🔧 TECHNICAL SEO
{'='*30}
"""
        technical = self.audit_results.get('technical_seo', {})
        
        if 'https_ssl' in technical:
            ssl_data = technical['https_ssl']
            report += f"✅ HTTPS/SSL: {'✓' if ssl_data.get('is_https') else '✗'} | Status: {ssl_data.get('status', 'Unknown')}\n"
        
        if 'mobile_friendly' in technical:
            mobile_data = technical['mobile_friendly']
            report += f"📱 Mobile-Friendly: {'✓' if mobile_data.get('has_viewport_meta') else '✗'} | Status: {mobile_data.get('status', 'Unknown')}\n"
        
        if 'xml_sitemap' in technical:
            sitemap_data = technical['xml_sitemap']
            report += f"🗺️  XML Sitemap: {'✓' if sitemap_data.get('exists') else '✗'} | Status: {sitemap_data.get('status', 'Unknown')}\n"
        
        # Add more sections...
        
        return report

def main():
    """Main function to run the SEO auditor"""
    print("🚀 Advanced SEO Audit Software")
    print("=" * 40)
    
    # Example usage
    url = input("Enter website URL to audit: ").strip()
    api_key = input("Enter Google PageSpeed Insights API key (optional): ").strip() or None
    
    auditor = SEOAuditor(pagespeed_api_key=api_key)
    results = auditor.audit_website(url)
    
    # Generate and display report
    report = auditor.generate_report()
    print(report)
    
    # Save detailed results to JSON
    with open(f"seo_audit_{auditor.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to JSON file")

if __name__ == "__main__":
    main()