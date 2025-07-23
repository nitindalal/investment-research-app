import yfinance as yf
import pandas as pd
import requests
import json
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class CompanyAnalyzer:
    """Service for analyzing company information, financials, and competitive position"""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
        self.base_url = "https://www.alphavantage.co/query"
        
    def get_company_info(self, company_input: str) -> Optional[Dict[str, Any]]:
        """Get basic company information by name or symbol. Tries yfinance first, then resolves name to symbol using Yahoo Finance search API if needed."""
        try:
            # Try to get info using yfinance
            ticker = yf.Ticker(company_input)
            info = ticker.info

            if not info or info.get('regularMarketPrice') is None:
                # Try to resolve company name to symbol using Yahoo Finance search API
                search_url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company_input}"
                try:
                    resp = requests.get(search_url, timeout=5)
                    logger.info(f"Yahoo search API response for '{company_input}': {resp.status_code}")
                    if resp.status_code == 200:
                        data = resp.json()
                        logger.info(f"Yahoo API quotes for '{company_input}': {data.get('quotes')}")
                        if data.get('quotes'):
                            for quote in data['quotes']:
                                logger.info(f"Trying quote: {quote}")
                                if quote.get('quoteType') == 'EQUITY' and 'symbol' in quote:
                                    resolved_symbol = quote['symbol']
                                    logger.info(f"Trying resolved symbol: {resolved_symbol}")
                                    ticker = yf.Ticker(resolved_symbol)
                                    info = ticker.info
                                    if info and info.get('regularMarketPrice') is not None:
                                        logger.info(f"Resolved symbol '{resolved_symbol}' for input '{company_input}'")
                                        break
                                    else:
                                        logger.info(f"Symbol '{resolved_symbol}' did not return valid info.")
                                        info = None
                                        continue
                            else:
                                logger.warning(f"No valid equity symbol found for '{company_input}' in Yahoo API results.")
                                return None
                        else:
                            logger.warning(f"No quotes found in Yahoo API for '{company_input}'")
                            return None
                    else:
                        logger.error(f"Yahoo search API failed for '{company_input}' with status {resp.status_code}")
                        return None
                except Exception as e:
                    logger.error(f"Error resolving symbol for {company_input}: {str(e)}")
                    return None

            if not info or info.get('regularMarketPrice') is None:
                logger.warning(f"No valid info found for '{company_input}' after all attempts.")
                return None

            return {
                'symbol': info.get('symbol', company_input.upper()),
                'name': info.get('longName', info.get('shortName', 'Unknown')),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap'),
                'enterprise_value': info.get('enterpriseValue'),
                'description': info.get('longBusinessSummary', ''),
                'website': info.get('website', ''),
                'country': info.get('country', ''),
                'employees': info.get('fullTimeEmployees'),
                'ceo': info.get('companyOfficers', [{}])[0].get('name', 'Unknown') if info.get('companyOfficers') else 'Unknown'
            }

        except Exception as e:
            logger.error(f"Error getting company info for {company_input}: {str(e)}")
            return None
    
    def get_financial_data(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive financial data for a company"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get financial statements
            income_stmt = ticker.financials
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            # Get key metrics
            info = ticker.info
            
            # Calculate key ratios
            financial_data = {
                'revenue_sources': self._analyze_revenue_sources(income_stmt),
                'cost_drivers': self._analyze_cost_drivers(income_stmt),
                'profitability_metrics': {
                    'gross_margin': info.get('grossMargins'),
                    'operating_margin': info.get('operatingMargins'),
                    'net_margin': info.get('profitMargins'),
                    'roa': info.get('returnOnAssets'),
                    'roe': info.get('returnOnEquity'),
                    'roic': info.get('returnOnCapital')
                },
                'growth_metrics': self._calculate_growth_metrics(income_stmt),
                'liquidity_metrics': {
                    'current_ratio': info.get('currentRatio'),
                    'quick_ratio': info.get('quickRatio'),
                    'debt_to_equity': info.get('debtToEquity'),
                    'interest_coverage': info.get('interestCoverage')
                },
                'efficiency_metrics': {
                    'asset_turnover': info.get('assetTurnover'),
                    'inventory_turnover': info.get('inventoryTurnover'),
                    'receivables_turnover': info.get('receivablesTurnover')
                },
                'historical_data': {
                    'revenue_5y': self._get_historical_metric(income_stmt, 'Total Revenue', 5),
                    'earnings_5y': self._get_historical_metric(income_stmt, 'Net Income', 5),
                    'cash_flow_5y': self._get_historical_metric(cash_flow, 'Operating Cash Flow', 5)
                }
            }
            
            return financial_data
            
        except Exception as e:
            logger.error(f"Error getting financial data for {symbol}: {str(e)}")
            return {}
    
    def _analyze_revenue_sources(self, income_stmt: pd.DataFrame) -> Dict[str, Any]:
        """Analyze revenue sources and breakdown"""
        try:
            if income_stmt.empty:
                return {'primary_sources': [], 'geographic_breakdown': {}, 'segment_breakdown': {}}
            
            # Get revenue line items
            revenue_items = [col for col in income_stmt.index if 'revenue' in col.lower() or 'sales' in col.lower()]
            
            revenue_sources = {}
            for item in revenue_items:
                if item in income_stmt.index:
                    revenue_sources[item] = income_stmt.loc[item].iloc[0] if not income_stmt.loc[item].empty else 0
            
            return {
                'primary_sources': revenue_sources,
                'geographic_breakdown': {},  # Would need additional data source
                'segment_breakdown': {}      # Would need additional data source
            }
            
        except Exception as e:
            logger.error(f"Error analyzing revenue sources: {str(e)}")
            return {'primary_sources': [], 'geographic_breakdown': {}, 'segment_breakdown': {}}
    
    def _analyze_cost_drivers(self, income_stmt: pd.DataFrame) -> Dict[str, Any]:
        """Analyze cost drivers and breakdown"""
        try:
            if income_stmt.empty:
                return {'primary_costs': [], 'cost_structure': {}}
            
            # Get cost line items
            cost_items = [col for col in income_stmt.index if any(cost in col.lower() for cost in ['cost', 'expense', 'operating'])]
            
            cost_drivers = {}
            for item in cost_items:
                if item in income_stmt.index:
                    cost_drivers[item] = income_stmt.loc[item].iloc[0] if not income_stmt.loc[item].empty else 0
            
            return {
                'primary_costs': cost_drivers,
                'cost_structure': {
                    'fixed_costs': {},  # Would need additional analysis
                    'variable_costs': {} # Would need additional analysis
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing cost drivers: {str(e)}")
            return {'primary_costs': [], 'cost_structure': {}}
    
    def _calculate_growth_metrics(self, income_stmt: pd.DataFrame) -> Dict[str, float]:
        """Calculate growth metrics over time"""
        try:
            if income_stmt.empty or income_stmt.shape[1] < 2:
                return {}
            
            growth_metrics = {}
            
            # Revenue growth
            if 'Total Revenue' in income_stmt.index:
                revenue = income_stmt.loc['Total Revenue']
                if len(revenue) >= 2:
                    growth_metrics['revenue_growth_1y'] = (revenue.iloc[0] - revenue.iloc[1]) / revenue.iloc[1] if revenue.iloc[1] != 0 else 0
            
            # Earnings growth
            if 'Net Income' in income_stmt.index:
                earnings = income_stmt.loc['Net Income']
                if len(earnings) >= 2:
                    growth_metrics['earnings_growth_1y'] = (earnings.iloc[0] - earnings.iloc[1]) / earnings.iloc[1] if earnings.iloc[1] != 0 else 0
            
            return growth_metrics
            
        except Exception as e:
            logger.error(f"Error calculating growth metrics: {str(e)}")
            return {}
    
    def _get_historical_metric(self, df: pd.DataFrame, metric: str, years: int) -> List[float]:
        """Get historical values for a specific metric"""
        try:
            if df.empty or metric not in df.index:
                return []
            
            values = df.loc[metric].head(years).tolist()
            return [float(v) if v is not None else 0 for v in values]
            
        except Exception as e:
            logger.error(f"Error getting historical metric {metric}: {str(e)}")
            return []
    
    def get_competitive_analysis(self, symbol: str) -> Dict[str, Any]:
        """Analyze competitive position and market share"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get competitors (this would need additional data source)
            competitors = self._get_competitors(symbol)
            
            return {
                'market_position': {
                    'market_share': info.get('marketCap'),  # Would need total market size
                    'competitive_advantages': self._identify_advantages(info),
                    'moat_analysis': self._analyze_moat(info),
                    'swot_analysis': self._perform_swot_analysis(info)
                },
                'competitors': competitors,
                'competitive_threats': self._identify_threats(info),
                'barriers_to_entry': self._analyze_barriers(info),
                'porters_five_forces': self._porters_five_forces(info)
            }
        except Exception as e:
            logger.error(f"Error getting competitive analysis for {symbol}: {str(e)}")
            return {}

    def _porters_five_forces(self, info: Dict[str, Any]) -> Dict[str, str]:
        """Generate a basic Porter's Five Forces analysis"""
        # These are simple heuristics; in a real app, use more data
        forces = {}
        # 1. Threat of New Entrants
        barriers = info.get('barriersToEntry', 'moderate')
        if info.get('marketCap', 0) > 1e11:
            barriers = 'high'
        elif info.get('marketCap', 0) < 1e9:
            barriers = 'low'
        forces['threat_of_new_entrants'] = f"Barriers to entry are {barriers}. Large established players and high capital requirements may deter new entrants."
        # 2. Bargaining Power of Suppliers
        forces['bargaining_power_of_suppliers'] = "Supplier power is moderate. The company may have multiple suppliers, but unique components or raw materials could increase supplier influence."
        # 3. Bargaining Power of Buyers
        if info.get('grossMargins', 0) > 0.4:
            buyer_power = 'low'
        else:
            buyer_power = 'moderate'
        forces['bargaining_power_of_buyers'] = f"Buyer power is {buyer_power}. Strong brand or differentiated products reduce buyer leverage."
        # 4. Threat of Substitute Products
        forces['threat_of_substitutes'] = "Threat of substitutes is moderate. Innovation and changing consumer preferences could introduce alternatives."
        # 5. Rivalry Among Existing Competitors
        if info.get('marketCap', 0) > 1e11:
            rivalry = 'high'
        else:
            rivalry = 'moderate'
        forces['rivalry_among_competitors'] = f"Competitive rivalry is {rivalry}. The industry has several strong players and competition is intense."
        return forces
    
    def _get_competitors(self, symbol: str) -> List[Dict[str, Any]]:
        """Get list of competitors (placeholder implementation)"""
        # This would typically use a database or API to get competitors
        # For now, return empty list
        return []
    
    def _identify_advantages(self, info: Dict[str, Any]) -> List[str]:
        """Identify competitive advantages"""
        advantages = []
        
        if info.get('grossMargins', 0) > 0.4:
            advantages.append("High gross margins indicating pricing power")
        
        if info.get('returnOnEquity', 0) > 0.15:
            advantages.append("Strong return on equity")
        
        if info.get('debtToEquity', 0) < 0.5:
            advantages.append("Low debt levels")
        
        return advantages
    
    def _analyze_moat(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze economic moat"""
        moat_score = 0
        moat_factors = []
        
        # Brand value
        if info.get('brandValue'):
            moat_score += 1
            moat_factors.append("Strong brand value")
        
        # Network effects (would need additional data)
        # Switching costs (would need additional data)
        # Cost advantages (would need additional data)
        
        return {
            'moat_score': moat_score,
            'moat_factors': moat_factors,
            'moat_strength': 'Strong' if moat_score >= 3 else 'Moderate' if moat_score >= 1 else 'Weak'
        }
    
    def _perform_swot_analysis(self, info: Dict[str, Any]) -> Dict[str, List[str]]:
        """Perform SWOT analysis"""
        swot = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'threats': []
        }
        
        # Strengths
        if info.get('grossMargins', 0) > 0.3:
            swot['strengths'].append("Strong profitability")
        
        if info.get('currentRatio', 0) > 1.5:
            swot['strengths'].append("Good liquidity position")
        
        # Weaknesses
        if info.get('debtToEquity', 0) > 1.0:
            swot['weaknesses'].append("High debt levels")
        
        if info.get('returnOnEquity', 0) < 0.1:
            swot['weaknesses'].append("Low return on equity")
        
        return swot
    
    def _identify_threats(self, info: Dict[str, Any]) -> List[str]:
        """Identify competitive threats"""
        threats = []
        
        # Market saturation
        if info.get('marketCap', 0) > 100000000000:  # $100B
            threats.append("Large market cap may limit growth potential")
        
        # Regulatory risks
        if info.get('sector') in ['Healthcare', 'Financial Services']:
            threats.append("Regulatory risks in sector")
        
        return threats
    
    def _analyze_barriers(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze barriers to entry"""
        barriers = {
            'capital_requirements': 'High' if info.get('marketCap', 0) > 10000000000 else 'Medium',
            'regulatory_barriers': 'High' if info.get('sector') in ['Healthcare', 'Financial Services'] else 'Low',
            'technology_barriers': 'Medium',  # Would need additional analysis
            'brand_barriers': 'High' if info.get('brandValue') else 'Low'
        }
        
        return barriers
    
    def get_industry_analysis(self, sector: str) -> Dict[str, Any]:
        """Analyze industry position and trends"""
        try:
            return {
                'sector_performance': self._get_sector_performance(sector),
                'industry_trends': self._get_industry_trends(sector),
                'regulatory_environment': self._get_regulatory_environment(sector),
                'growth_prospects': self._get_growth_prospects(sector)
            }
            
        except Exception as e:
            logger.error(f"Error getting industry analysis for {sector}: {str(e)}")
            return {}
    
    def _get_sector_performance(self, sector: str) -> Dict[str, Any]:
        """Get sector performance metrics"""
        # This would typically use market data APIs
        return {
            'sector_growth_rate': 0.05,  # Placeholder
            'sector_pe_ratio': 15.0,     # Placeholder
            'sector_market_cap': 1000000000000  # Placeholder
        }
    
    def _get_industry_trends(self, sector: str) -> List[str]:
        """Get industry trends"""
        trends = {
            'Technology': ['Digital transformation', 'AI/ML adoption', 'Cloud computing'],
            'Healthcare': ['Telemedicine', 'Personalized medicine', 'Digital health'],
            'Financial Services': ['Fintech disruption', 'Digital banking', 'Regulatory changes'],
            'Consumer Discretionary': ['E-commerce growth', 'Sustainability focus', 'Digital marketing']
        }
        
        return trends.get(sector, ['General market trends'])
    
    def _get_regulatory_environment(self, sector: str) -> Dict[str, str]:
        """Get regulatory environment assessment"""
        regulatory_risk = {
            'Technology': 'Low',
            'Healthcare': 'High',
            'Financial Services': 'High',
            'Consumer Discretionary': 'Medium'
        }
        
        return {
            'regulatory_risk': regulatory_risk.get(sector, 'Medium'),
            'compliance_requirements': 'Standard' if sector not in ['Healthcare', 'Financial Services'] else 'High'
        }
    
    def _get_growth_prospects(self, sector: str) -> Dict[str, Any]:
        """Get growth prospects for the sector"""
        return {
            'projected_growth_rate': 0.05,  # Placeholder
            'key_drivers': ['Market expansion', 'Technology adoption'],
            'risks': ['Economic downturn', 'Regulatory changes']
        }
    
    def search_companies(self, query: str) -> List[Dict[str, Any]]:
        """Search for companies by name or symbol"""
        try:
            # This would typically use a company database or API
            # For now, return a simple search using yfinance
            results = []
            
            # Try direct ticker lookup
            try:
                ticker = yf.Ticker(query.upper())
                info = ticker.info
                if info and info.get('regularMarketPrice'):
                    results.append({
                        'symbol': info.get('symbol'),
                        'name': info.get('longName', info.get('shortName')),
                        'sector': info.get('sector', 'Unknown')
                    })
            except:
                pass
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching companies: {str(e)}")
            return []
    
    def generate_recommendation(self, financial_data: Dict, market_data: Dict, 
                              sentiment_data: Dict, valuations: Dict) -> Dict[str, Any]:
        """Generate investment recommendation based on all analysis"""
        try:
            # Calculate recommendation score
            score = 0
            factors = []
            
            # Financial health (40% weight)
            if financial_data.get('profitability_metrics', {}).get('roa', 0) > 0.05:
                score += 0.4
                factors.append("Strong return on assets")
            
            # Valuation (30% weight)
            if valuations.get('pe_ratio', 0) < 20:
                score += 0.3
                factors.append("Reasonable P/E ratio")
            
            # Sentiment (20% weight)
            if sentiment_data.get('overall_sentiment', 0) > 0.5:
                score += 0.2
                factors.append("Positive market sentiment")
            
            # Market position (10% weight)
            if market_data.get('market_cap', 0) > 10000000000:  # $10B
                score += 0.1
                factors.append("Large market cap")
            
            # Determine recommendation
            if score >= 0.7:
                recommendation = "BUY"
                confidence = "High"
            elif score >= 0.5:
                recommendation = "HOLD"
                confidence = "Medium"
            else:
                recommendation = "SELL"
                confidence = "Low"
            
            return {
                'recommendation': recommendation,
                'confidence': confidence,
                'score': score,
                'factors': factors,
                'risk_level': 'Low' if score >= 0.7 else 'Medium' if score >= 0.5 else 'High'
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendation: {str(e)}")
            return {
                'recommendation': 'HOLD',
                'confidence': 'Low',
                'score': 0.5,
                'factors': ['Insufficient data'],
                'risk_level': 'Medium'
            } 