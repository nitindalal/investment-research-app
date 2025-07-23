import yfinance as yf
import pandas as pd
import requests
import json
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class MarketDataService:
    """Service for retrieving and analyzing market data"""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
        self.base_url = "https://www.alphavantage.co/query"
        
    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive market data for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get historical price data
            hist = ticker.history(period="1y")
            
            # Get options data
            options = self._get_options_data(symbol)
            
            # Get institutional data
            institutional_data = self._get_institutional_data(symbol)
            
            return {
                'current_price': info.get('regularMarketPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'price_change': info.get('regularMarketChange', 0),
                'price_change_percent': info.get('regularMarketChangePercent', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'year_high': info.get('fiftyTwoWeekHigh', 0),
                'year_low': info.get('fiftyTwoWeekLow', 0),
                'beta': info.get('beta', 0),
                'pe_ratio': info.get('trailingPE', None),
                'shares_outstanding': info.get('sharesOutstanding', 0),
                'float_shares': info.get('floatShares', 0),
                'short_ratio': info.get('shortRatio', 0),
                'options_data': options,
                'institutional_data': institutional_data,
                'price_history': self._format_price_history(hist),
                'technical_indicators': self._calculate_technical_indicators(hist)
            }
            
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {str(e)}")
            return {}
    
    def _get_options_data(self, symbol: str) -> Dict[str, Any]:
        """Get options data for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get options expiration dates
            expirations = ticker.options
            
            if not expirations:
                return {}
            
            # Get options for nearest expiration
            nearest_exp = expirations[0]
            options = ticker.option_chain(nearest_exp)
            
            calls = options.calls
            puts = options.puts
            
            # Calculate put/call ratio
            put_volume = puts['volume'].sum() if not puts.empty else 0
            call_volume = calls['volume'].sum() if not calls.empty else 0
            put_call_ratio = put_volume / call_volume if call_volume > 0 else 0
            
            return {
                'put_call_ratio': put_call_ratio,
                'total_call_volume': call_volume,
                'total_put_volume': put_volume,
                'nearest_expiration': nearest_exp,
                'implied_volatility': self._calculate_avg_iv(calls, puts)
            }
            
        except Exception as e:
            logger.error(f"Error getting options data for {symbol}: {str(e)}")
            return {}
    
    def _calculate_avg_iv(self, calls: pd.DataFrame, puts: pd.DataFrame) -> float:
        """Calculate average implied volatility"""
        try:
            all_iv = []
            
            if not calls.empty and 'impliedVolatility' in calls.columns:
                all_iv.extend(calls['impliedVolatility'].dropna().tolist())
            
            if not puts.empty and 'impliedVolatility' in puts.columns:
                all_iv.extend(puts['impliedVolatility'].dropna().tolist())
            
            return sum(all_iv) / len(all_iv) if all_iv else 0
            
        except Exception as e:
            logger.error(f"Error calculating average IV: {str(e)}")
            return 0
    
    def _get_institutional_data(self, symbol: str) -> Dict[str, Any]:
        """Get institutional ownership data"""
        try:
            # This would typically use a financial data API
            # For now, return placeholder data
            import random
            
            return {
                'institutional_ownership': random.uniform(0.3, 0.8),
                'insider_ownership': random.uniform(0.01, 0.15),
                'top_institutional_holders': [
                    {'name': 'Vanguard Group', 'shares': random.randint(1000000, 10000000)},
                    {'name': 'BlackRock', 'shares': random.randint(500000, 5000000)},
                    {'name': 'State Street', 'shares': random.randint(200000, 2000000)}
                ],
                'recent_institutional_activity': 'Buying' if random.random() > 0.5 else 'Selling'
            }
            
        except Exception as e:
            logger.error(f"Error getting institutional data for {symbol}: {str(e)}")
            return {}
    
    def _format_price_history(self, hist: pd.DataFrame) -> List[Dict[str, Any]]:
        """Format price history data"""
        try:
            if hist.empty:
                return []
            
            formatted_data = []
            for date, row in hist.iterrows():
                formatted_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume'])
                })
            
            return formatted_data
            
        except Exception as e:
            logger.error(f"Error formatting price history: {str(e)}")
            return []
    
    def _calculate_technical_indicators(self, hist: pd.DataFrame) -> Dict[str, Any]:
        """Calculate technical indicators"""
        try:
            if hist.empty:
                return {}
            
            close_prices = hist['Close']
            
            # Calculate moving averages
            sma_20 = close_prices.rolling(window=20).mean().iloc[-1]
            sma_50 = close_prices.rolling(window=50).mean().iloc[-1]
            sma_200 = close_prices.rolling(window=200).mean().iloc[-1]
            
            # Calculate RSI
            delta = close_prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            # Calculate MACD
            ema_12 = close_prices.ewm(span=12).mean()
            ema_26 = close_prices.ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            current_macd = macd.iloc[-1]
            current_signal = signal.iloc[-1]
            
            # Calculate Bollinger Bands
            bb_middle = close_prices.rolling(window=20).mean()
            bb_std = close_prices.rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            current_price = close_prices.iloc[-1]
            current_bb_upper = bb_upper.iloc[-1]
            current_bb_lower = bb_lower.iloc[-1]
            
            return {
                'moving_averages': {
                    'sma_20': float(sma_20) if not pd.isna(sma_20) else 0,
                    'sma_50': float(sma_50) if not pd.isna(sma_50) else 0,
                    'sma_200': float(sma_200) if not pd.isna(sma_200) else 0,
                    'price_vs_sma_20': 'Above' if current_price > sma_20 else 'Below',
                    'price_vs_sma_50': 'Above' if current_price > sma_50 else 'Below',
                    'price_vs_sma_200': 'Above' if current_price > sma_200 else 'Below'
                },
                'rsi': {
                    'value': float(current_rsi) if not pd.isna(current_rsi) else 50,
                    'interpretation': 'Overbought' if current_rsi > 70 else 'Oversold' if current_rsi < 30 else 'Neutral'
                },
                'macd': {
                    'value': float(current_macd) if not pd.isna(current_macd) else 0,
                    'signal': float(current_signal) if not pd.isna(current_signal) else 0,
                    'interpretation': 'Bullish' if current_macd > current_signal else 'Bearish'
                },
                'bollinger_bands': {
                    'upper': float(current_bb_upper) if not pd.isna(current_bb_upper) else 0,
                    'lower': float(current_bb_lower) if not pd.isna(current_bb_lower) else 0,
                    'position': 'Upper' if current_price > current_bb_upper else 'Lower' if current_price < current_bb_lower else 'Middle'
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {str(e)}")
            return {}
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Get overall market overview and sector performance"""
        try:
            # Get major indices
            indices = {
                'S&P 500': '^GSPC',
                'NASDAQ': '^IXIC',
                'DOW': '^DJI',
                'VIX': '^VIX'
            }
            
            market_data = {}
            for name, symbol in indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    market_data[name] = {
                        'price': info.get('regularMarketPrice', 0),
                        'change': info.get('regularMarketChange', 0),
                        'change_percent': info.get('regularMarketChangePercent', 0),
                        'volume': info.get('volume', 0)
                    }
                except Exception as e:
                    logger.error(f"Error getting data for {name}: {str(e)}")
                    market_data[name] = {}
            
            # Get sector performance
            sectors = self._get_sector_performance()
            
            # Get market breadth
            market_breadth = self._calculate_market_breadth()
            
            return {
                'indices': market_data,
                'sectors': sectors,
                'market_breadth': market_breadth,
                'market_sentiment': self._assess_market_sentiment(market_data),
                'trading_volume': self._get_market_volume(),
                'volatility': self._get_market_volatility()
            }
            
        except Exception as e:
            logger.error(f"Error getting market overview: {str(e)}")
            return {}
    
    def _get_sector_performance(self) -> Dict[str, Any]:
        """Get sector performance data"""
        try:
            # Sector ETFs for performance tracking
            sector_etfs = {
                'Technology': 'XLK',
                'Healthcare': 'XLV',
                'Financial Services': 'XLF',
                'Consumer Discretionary': 'XLY',
                'Consumer Staples': 'XLP',
                'Industrials': 'XLI',
                'Energy': 'XLE',
                'Materials': 'XLB',
                'Real Estate': 'XLRE',
                'Utilities': 'XLU',
                'Communication Services': 'XLC'
            }
            
            sector_data = {}
            for sector, etf in sector_etfs.items():
                try:
                    ticker = yf.Ticker(etf)
                    info = ticker.info
                    
                    sector_data[sector] = {
                        'price': info.get('regularMarketPrice', 0),
                        'change_percent': info.get('regularMarketChangePercent', 0),
                        'volume': info.get('volume', 0)
                    }
                except Exception as e:
                    logger.error(f"Error getting sector data for {sector}: {str(e)}")
                    sector_data[sector] = {}
            
            return sector_data
            
        except Exception as e:
            logger.error(f"Error getting sector performance: {str(e)}")
            return {}
    
    def _calculate_market_breadth(self) -> Dict[str, Any]:
        """Calculate market breadth indicators"""
        try:
            # This would typically analyze all stocks in an index
            # For now, return placeholder data
            import random
            
            return {
                'advancing_stocks': random.randint(200, 300),
                'declining_stocks': random.randint(100, 200),
                'advance_decline_ratio': random.uniform(1.2, 2.0),
                'new_highs': random.randint(20, 50),
                'new_lows': random.randint(5, 20),
                'high_low_ratio': random.uniform(2.0, 5.0)
            }
            
        except Exception as e:
            logger.error(f"Error calculating market breadth: {str(e)}")
            return {}
    
    def _assess_market_sentiment(self, market_data: Dict[str, Any]) -> str:
        """Assess overall market sentiment"""
        try:
            # Analyze major indices for sentiment
            positive_count = 0
            total_count = 0
            
            for index_data in market_data.values():
                if index_data and 'change_percent' in index_data:
                    if index_data['change_percent'] > 0:
                        positive_count += 1
                    total_count += 1
            
            if total_count == 0:
                return 'Neutral'
            
            positive_ratio = positive_count / total_count
            
            if positive_ratio >= 0.7:
                return 'Bullish'
            elif positive_ratio <= 0.3:
                return 'Bearish'
            else:
                return 'Neutral'
                
        except Exception as e:
            logger.error(f"Error assessing market sentiment: {str(e)}")
            return 'Neutral'
    
    def _get_market_volume(self) -> Dict[str, Any]:
        """Get market volume data"""
        try:
            # This would typically aggregate volume data
            # For now, return placeholder data
            import random
            
            return {
                'total_volume': random.randint(1000000000, 5000000000),
                'average_volume': random.randint(800000000, 3000000000),
                'volume_trend': 'Increasing' if random.random() > 0.5 else 'Decreasing',
                'unusual_volume': random.randint(10, 50)
            }
            
        except Exception as e:
            logger.error(f"Error getting market volume: {str(e)}")
            return {}
    
    def _get_market_volatility(self) -> Dict[str, Any]:
        """Get market volatility data"""
        try:
            # Get VIX data
            vix_ticker = yf.Ticker('^VIX')
            vix_info = vix_ticker.info
            
            current_vix = vix_info.get('regularMarketPrice', 20)
            
            # Interpret VIX levels
            if current_vix < 15:
                volatility_level = 'Low'
            elif current_vix < 25:
                volatility_level = 'Normal'
            elif current_vix < 35:
                volatility_level = 'High'
            else:
                volatility_level = 'Extreme'
            
            return {
                'vix_level': current_vix,
                'volatility_level': volatility_level,
                'fear_greed_index': self._calculate_fear_greed_index(current_vix)
            }
            
        except Exception as e:
            logger.error(f"Error getting market volatility: {str(e)}")
            return {}
    
    def _calculate_fear_greed_index(self, vix: float) -> str:
        """Calculate fear/greed index based on VIX"""
        try:
            if vix < 15:
                return 'Extreme Greed'
            elif vix < 20:
                return 'Greed'
            elif vix < 25:
                return 'Neutral'
            elif vix < 30:
                return 'Fear'
            else:
                return 'Extreme Fear'
                
        except Exception as e:
            logger.error(f"Error calculating fear/greed index: {str(e)}")
            return 'Neutral'
    
    def get_sector_analysis(self, sector: str) -> Dict[str, Any]:
        """Get detailed analysis for a specific sector"""
        try:
            # Get sector ETF
            sector_etfs = {
                'Technology': 'XLK',
                'Healthcare': 'XLV',
                'Financial Services': 'XLF',
                'Consumer Discretionary': 'XLY',
                'Consumer Staples': 'XLP',
                'Industrials': 'XLI',
                'Energy': 'XLE',
                'Materials': 'XLB',
                'Real Estate': 'XLRE',
                'Utilities': 'XLU',
                'Communication Services': 'XLC'
            }
            
            etf_symbol = sector_etfs.get(sector)
            if not etf_symbol:
                return {'error': 'Sector not found'}
            
            ticker = yf.Ticker(etf_symbol)
            info = ticker.info
            hist = ticker.history(period="1y")
            
            return {
                'sector_name': sector,
                'etf_symbol': etf_symbol,
                'current_price': info.get('regularMarketPrice', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'technical_analysis': self._calculate_technical_indicators(hist),
                'sector_trends': self._get_sector_trends(sector),
                'key_drivers': self._get_sector_drivers(sector)
            }
            
        except Exception as e:
            logger.error(f"Error getting sector analysis for {sector}: {str(e)}")
            return {}
    
    def _get_sector_trends(self, sector: str) -> List[str]:
        """Get current trends for a sector"""
        trends = {
            'Technology': ['AI/ML adoption', 'Cloud computing growth', 'Cybersecurity focus'],
            'Healthcare': ['Digital health', 'Biotech innovation', 'Telemedicine expansion'],
            'Financial Services': ['Fintech disruption', 'Digital banking', 'Regulatory changes'],
            'Consumer Discretionary': ['E-commerce growth', 'Digital transformation', 'Sustainability focus'],
            'Energy': ['Renewable energy transition', 'Oil price volatility', 'ESG focus'],
            'Real Estate': ['Remote work impact', 'Urban migration', 'Interest rate sensitivity']
        }
        
        return trends.get(sector, ['General market trends'])
    
    def _get_sector_drivers(self, sector: str) -> List[str]:
        """Get key drivers for a sector"""
        drivers = {
            'Technology': ['Innovation', 'Digital transformation', 'Global competition'],
            'Healthcare': ['Demographics', 'Regulation', 'Technology adoption'],
            'Financial Services': ['Interest rates', 'Regulation', 'Technology disruption'],
            'Consumer Discretionary': ['Consumer confidence', 'Economic growth', 'Technology adoption'],
            'Energy': ['Oil prices', 'Geopolitics', 'Climate policy'],
            'Real Estate': ['Interest rates', 'Economic growth', 'Demographics']
        }
        
        return drivers.get(sector, ['Economic conditions', 'Market sentiment']) 