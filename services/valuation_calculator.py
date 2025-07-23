import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ValuationCalculator:
    """Service for calculating various valuation metrics and methodologies"""
    
    def __init__(self):
        self.risk_free_rate = 0.04  # 4% risk-free rate
        self.market_risk_premium = 0.06  # 6% market risk premium
        
    def calculate_valuations(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive valuation metrics"""
        try:
            return {
                'dcf_valuation': self._calculate_dcf_basic(financial_data),
                'relative_valuations': self._calculate_relative_valuations(financial_data),
                'asset_based_valuation': self._calculate_asset_based(financial_data),
                'dividend_discount_model': self._calculate_ddm(financial_data),
                'valuation_ratios': self._calculate_valuation_ratios(financial_data)
            }
        except Exception as e:
            logger.error(f"Error calculating valuations: {str(e)}")
            return {}
    
    def calculate_dcf(self, symbol: str, growth_rate: float = 0.05, 
                     discount_rate: float = 0.10) -> Dict[str, Any]:
        """Calculate Discounted Cash Flow valuation"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get financial data
            cash_flow = ticker.cashflow
            balance_sheet = ticker.balance_sheet
            info = ticker.info
            
            if cash_flow.empty:
                return {'error': 'No cash flow data available'}
            
            # Get free cash flow
            if 'Operating Cash Flow' in cash_flow.index:
                operating_cf = cash_flow.loc['Operating Cash Flow'].iloc[0] if not cash_flow.loc['Operating Cash Flow'].empty else 0
            else:
                operating_cf = 0
            
            if 'Capital Expenditure' in cash_flow.index:
                capex = abs(cash_flow.loc['Capital Expenditure'].iloc[0]) if not cash_flow.loc['Capital Expenditure'].empty else 0
            else:
                capex = 0
            
            fcf = operating_cf - capex
            
            # Calculate terminal value
            terminal_value = fcf * (1 + growth_rate) / (discount_rate - growth_rate)
            
            # Calculate present value of FCF for 5 years
            pv_fcf = 0
            for year in range(1, 6):
                future_fcf = fcf * (1 + growth_rate) ** year
                pv_fcf += future_fcf / (1 + discount_rate) ** year
            
            # Calculate enterprise value
            enterprise_value = pv_fcf + terminal_value / (1 + discount_rate) ** 5
            
            # Get debt and cash
            if 'Total Debt' in balance_sheet.index:
                total_debt = balance_sheet.loc['Total Debt'].iloc[0] if not balance_sheet.loc['Total Debt'].empty else 0
            else:
                total_debt = 0
            
            if 'Cash' in balance_sheet.index:
                cash = balance_sheet.loc['Cash'].iloc[0] if not balance_sheet.loc['Cash'].empty else 0
            else:
                cash = 0
            
            # Calculate equity value
            equity_value = enterprise_value - total_debt + cash
            
            # Get shares outstanding
            shares_outstanding = info.get('sharesOutstanding', 1)
            
            # Calculate per-share value
            per_share_value = equity_value / shares_outstanding if shares_outstanding > 0 else 0
            
            # Get current price
            current_price = info.get('regularMarketPrice', 0)
            
            return {
                'dcf_value_per_share': per_share_value,
                'current_price': current_price,
                'upside_potential': (per_share_value - current_price) / current_price if current_price > 0 else 0,
                'enterprise_value': enterprise_value,
                'equity_value': equity_value,
                'free_cash_flow': fcf,
                'terminal_value': terminal_value,
                'assumptions': {
                    'growth_rate': growth_rate,
                    'discount_rate': discount_rate,
                    'risk_free_rate': self.risk_free_rate,
                    'market_risk_premium': self.market_risk_premium
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating DCF for {symbol}: {str(e)}")
            return {'error': f'DCF calculation failed: {str(e)}'}
    
    def _calculate_dcf_basic(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate basic DCF valuation from financial data"""
        try:
            # Extract cash flow data
            historical_cf = financial_data.get('historical_data', {}).get('cash_flow_5y', [])
            
            if not historical_cf:
                return {'error': 'Insufficient cash flow data'}
            
            # Use most recent cash flow
            fcf = historical_cf[0] if historical_cf else 0
            
            # Simple DCF calculation
            growth_rate = 0.05
            discount_rate = 0.10
            
            terminal_value = fcf * (1 + growth_rate) / (discount_rate - growth_rate)
            pv_fcf = fcf * 5  # Simplified 5-year projection
            
            enterprise_value = pv_fcf + terminal_value / (1 + discount_rate) ** 5
            
            return {
                'dcf_value': enterprise_value,
                'free_cash_flow': fcf,
                'terminal_value': terminal_value,
                'growth_rate': growth_rate,
                'discount_rate': discount_rate
            }
            
        except Exception as e:
            logger.error(f"Error calculating basic DCF: {str(e)}")
            return {'error': 'Basic DCF calculation failed'}
    
    def _calculate_relative_valuations(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate relative valuation metrics"""
        try:
            # Extract financial metrics
            profitability = financial_data.get('profitability_metrics', {})
            growth = financial_data.get('growth_metrics', {})
            
            # Calculate P/E ratio
            pe_ratio = 15.0  # Placeholder - would need actual earnings data
            
            # Calculate P/B ratio
            pb_ratio = 2.0  # Placeholder - would need book value data
            
            # Calculate EV/EBITDA
            ev_ebitda = 12.0  # Placeholder - would need EBITDA data
            
            return {
                'pe_ratio': pe_ratio,
                'pb_ratio': pb_ratio,
                'ev_ebitda': ev_ebitda,
                'peg_ratio': pe_ratio / (growth.get('revenue_growth_1y', 0.05) * 100) if growth.get('revenue_growth_1y') else None
            }
            
        except Exception as e:
            logger.error(f"Error calculating relative valuations: {str(e)}")
            return {}
    
    def _calculate_asset_based(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate asset-based valuation"""
        try:
            # This would need balance sheet data
            # For now, return placeholder values
            return {
                'book_value': 0,  # Would need total equity data
                'tangible_book_value': 0,  # Would need tangible assets data
                'liquidation_value': 0,  # Would need asset liquidation analysis
                'replacement_cost': 0  # Would need asset replacement analysis
            }
            
        except Exception as e:
            logger.error(f"Error calculating asset-based valuation: {str(e)}")
            return {}
    
    def _calculate_ddm(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Dividend Discount Model"""
        try:
            # This would need dividend data
            # For now, return placeholder values
            return {
                'dividend_yield': 0.02,  # Placeholder
                'dividend_growth_rate': 0.03,  # Placeholder
                'ddm_value': 0  # Would calculate based on dividend data
            }
            
        except Exception as e:
            logger.error(f"Error calculating DDM: {str(e)}")
            return {}
    
    def _calculate_valuation_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate various valuation ratios"""
        try:
            profitability = financial_data.get('profitability_metrics', {})
            
            return {
                'price_to_earnings': 15.0,  # Placeholder
                'price_to_book': 2.0,  # Placeholder
                'price_to_sales': 3.0,  # Placeholder
                'price_to_cash_flow': 10.0,  # Placeholder
                'enterprise_value_to_ebitda': 12.0,  # Placeholder
                'return_on_invested_capital': profitability.get('roic', 0),
                'economic_value_added': 0  # Would need detailed calculation
            }
            
        except Exception as e:
            logger.error(f"Error calculating valuation ratios: {str(e)}")
            return {}
    
    def compare_with_peers(self, symbol: str) -> Dict[str, Any]:
        """Compare valuation metrics with peer companies"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get sector/industry for peer comparison
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            
            # Define peer companies (this would typically come from a database)
            peers = self._get_peer_companies(sector, industry)
            
            comparison_data = {
                'company_metrics': {
                    'pe_ratio': info.get('trailingPE', 0),
                    'pb_ratio': info.get('priceToBook', 0),
                    'ps_ratio': info.get('priceToSalesTrailing12Months', 0),
                    'ev_ebitda': info.get('enterpriseToEbitda', 0),
                    'roe': info.get('returnOnEquity', 0),
                    'roa': info.get('returnOnAssets', 0)
                },
                'peer_comparison': [],
                'valuation_percentile': {}
            }
            
            # Compare with each peer
            for peer in peers:
                try:
                    peer_ticker = yf.Ticker(peer['symbol'])
                    peer_info = peer_ticker.info
                    
                    peer_metrics = {
                        'symbol': peer['symbol'],
                        'name': peer['name'],
                        'pe_ratio': peer_info.get('trailingPE', 0),
                        'pb_ratio': peer_info.get('priceToBook', 0),
                        'ps_ratio': peer_info.get('priceToSalesTrailing12Months', 0),
                        'ev_ebitda': peer_info.get('enterpriseToEbitda', 0),
                        'roe': peer_info.get('returnOnEquity', 0),
                        'roa': peer_info.get('returnOnAssets', 0)
                    }
                    
                    comparison_data['peer_comparison'].append(peer_metrics)
                    
                except Exception as e:
                    logger.error(f"Error getting peer data for {peer['symbol']}: {str(e)}")
                    continue
            
            # Calculate percentiles
            if comparison_data['peer_comparison']:
                comparison_data['valuation_percentile'] = self._calculate_percentiles(
                    comparison_data['company_metrics'], 
                    comparison_data['peer_comparison']
                )
            
            return comparison_data
            
        except Exception as e:
            logger.error(f"Error comparing with peers for {symbol}: {str(e)}")
            return {'error': 'Peer comparison failed'}
    
    def _get_peer_companies(self, sector: str, industry: str) -> List[Dict[str, str]]:
        """Get peer companies for comparison"""
        # This would typically use a database or API
        # For now, return some common companies by sector
        peer_map = {
            'Technology': [
                {'symbol': 'AAPL', 'name': 'Apple Inc.'},
                {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
                {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
                {'symbol': 'META', 'name': 'Meta Platforms Inc.'}
            ],
            'Healthcare': [
                {'symbol': 'JNJ', 'name': 'Johnson & Johnson'},
                {'symbol': 'PFE', 'name': 'Pfizer Inc.'},
                {'symbol': 'UNH', 'name': 'UnitedHealth Group Inc.'},
                {'symbol': 'ABBV', 'name': 'AbbVie Inc.'},
                {'symbol': 'TMO', 'name': 'Thermo Fisher Scientific Inc.'}
            ],
            'Financial Services': [
                {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.'},
                {'symbol': 'BAC', 'name': 'Bank of America Corp.'},
                {'symbol': 'WFC', 'name': 'Wells Fargo & Co.'},
                {'symbol': 'GS', 'name': 'Goldman Sachs Group Inc.'},
                {'symbol': 'MS', 'name': 'Morgan Stanley'}
            ]
        }
        
        return peer_map.get(sector, [])
    
    def _calculate_percentiles(self, company_metrics: Dict[str, float], 
                             peer_metrics: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate percentile rankings for valuation metrics"""
        try:
            percentiles = {}
            
            for metric in ['pe_ratio', 'pb_ratio', 'ps_ratio', 'ev_ebitda', 'roe', 'roa']:
                if metric in company_metrics and company_metrics[metric] is not None:
                    # Get peer values for this metric
                    peer_values = [peer[metric] for peer in peer_metrics 
                                 if peer.get(metric) is not None and peer[metric] > 0]
                    
                    if peer_values:
                        # Calculate percentile
                        company_value = company_metrics[metric]
                        peer_values.append(company_value)
                        peer_values.sort()
                        
                        percentile = (peer_values.index(company_value) / len(peer_values)) * 100
                        percentiles[metric] = percentile
            
            return percentiles
            
        except Exception as e:
            logger.error(f"Error calculating percentiles: {str(e)}")
            return {}
    
    def calculate_sensitivity_analysis(self, symbol: str) -> Dict[str, Any]:
        """Calculate DCF sensitivity analysis with different growth and discount rates"""
        try:
            growth_rates = [0.02, 0.05, 0.08, 0.10]
            discount_rates = [0.08, 0.10, 0.12, 0.15]
            
            sensitivity_matrix = {}
            
            for growth_rate in growth_rates:
                sensitivity_matrix[growth_rate] = {}
                for discount_rate in discount_rates:
                    dcf_result = self.calculate_dcf(symbol, growth_rate, discount_rate)
                    if 'dcf_value_per_share' in dcf_result:
                        sensitivity_matrix[growth_rate][discount_rate] = dcf_result['dcf_value_per_share']
                    else:
                        sensitivity_matrix[growth_rate][discount_rate] = None
            
            return {
                'sensitivity_matrix': sensitivity_matrix,
                'growth_rates': growth_rates,
                'discount_rates': discount_rates
            }
            
        except Exception as e:
            logger.error(f"Error calculating sensitivity analysis for {symbol}: {str(e)}")
            return {'error': 'Sensitivity analysis failed'}
    
    def calculate_fair_value_range(self, symbol: str) -> Dict[str, Any]:
        """Calculate fair value range using multiple valuation methods"""
        try:
            # Get DCF valuation
            dcf_result = self.calculate_dcf(symbol)
            
            # Get peer comparison
            peer_result = self.compare_with_peers(symbol)
            
            # Calculate fair value range
            valuations = []
            
            if 'dcf_value_per_share' in dcf_result:
                valuations.append(dcf_result['dcf_value_per_share'])
            
            # Add peer-based valuations if available
            if 'peer_comparison' in peer_result:
                peer_pe_ratios = [peer['pe_ratio'] for peer in peer_result['peer_comparison'] 
                                if peer.get('pe_ratio') and peer['pe_ratio'] > 0]
                
                if peer_pe_ratios:
                    avg_pe = sum(peer_pe_ratios) / len(peer_pe_ratios)
                    # Would need earnings per share for this calculation
                    # valuations.append(avg_pe * eps)
            
            if valuations:
                min_value = min(valuations)
                max_value = max(valuations)
                avg_value = sum(valuations) / len(valuations)
                
                return {
                    'fair_value_range': {
                        'minimum': min_value,
                        'maximum': max_value,
                        'average': avg_value
                    },
                    'valuation_methods': len(valuations),
                    'confidence_level': 'High' if len(valuations) >= 3 else 'Medium'
                }
            else:
                return {'error': 'Insufficient data for fair value calculation'}
                
        except Exception as e:
            logger.error(f"Error calculating fair value range for {symbol}: {str(e)}")
            return {'error': 'Fair value calculation failed'} 