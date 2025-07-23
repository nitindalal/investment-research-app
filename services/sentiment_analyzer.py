import requests
import json
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import os
from textblob import TextBlob
import pandas as pd

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Service for analyzing market sentiment, news sentiment, and social media sentiment"""
    
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY', 'demo')
        self.news_api_url = "https://newsapi.org/v2/everything"
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN', '')
        
    def analyze_sentiment(self, company_name: str) -> Dict[str, Any]:
        """Analyze overall sentiment for a company"""
        try:
            # Get news sentiment
            news_sentiment = self._analyze_news_sentiment(company_name)
            
            # Get social media sentiment
            social_sentiment = self._analyze_social_sentiment(company_name)
            
            # Get market sentiment
            market_sentiment = self._analyze_market_sentiment(company_name)
            
            # Combine all sentiment data
            overall_sentiment = self._calculate_overall_sentiment(
                news_sentiment, social_sentiment, market_sentiment
            )
            
            return {
                'overall_sentiment': overall_sentiment,
                'news_sentiment': news_sentiment,
                'social_sentiment': social_sentiment,
                'market_sentiment': market_sentiment,
                'sentiment_trends': self._get_sentiment_trends(company_name),
                'key_sentiment_drivers': self._identify_sentiment_drivers(company_name)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {company_name}: {str(e)}")
            return {}
    
    def _analyze_news_sentiment(self, company_name: str) -> Dict[str, Any]:
        """Analyze news sentiment for a company"""
        try:
            # Get news articles
            articles = self._get_news_articles(company_name)
            
            if not articles:
                return {
                    'sentiment_score': 0,
                    'sentiment_label': 'Neutral',
                    'article_count': 0,
                    'positive_articles': 0,
                    'negative_articles': 0,
                    'neutral_articles': 0
                }
            
            # Analyze sentiment for each article
            sentiments = []
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for article in articles[:20]:  # Limit to 20 articles
                title = article.get('title', '')
                description = article.get('description', '')
                content = f"{title} {description}"
                
                # Use TextBlob for sentiment analysis
                blob = TextBlob(content)
                sentiment_score = blob.sentiment.polarity
                sentiments.append(sentiment_score)
                
                if sentiment_score > 0.1:
                    positive_count += 1
                elif sentiment_score < -0.1:
                    negative_count += 1
                else:
                    neutral_count += 1
            
            # Calculate average sentiment
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            
            # Determine sentiment label
            if avg_sentiment > 0.1:
                sentiment_label = 'Positive'
            elif avg_sentiment < -0.1:
                sentiment_label = 'Negative'
            else:
                sentiment_label = 'Neutral'
            
            # Generate a summary paragraph
            summary = f"Based on {len(articles[:5])} recent articles from credible sources, the overall news sentiment for {company_name} is {sentiment_label.lower()}. "
            if sentiment_label == 'Positive':
                summary += "Most news coverage is optimistic, highlighting positive developments and outlook."
            elif sentiment_label == 'Negative':
                summary += "Recent news coverage is largely critical or highlights challenges facing the company."
            else:
                summary += "The news coverage is balanced, with both positive and negative perspectives."

            # Collect unique sources from the top 5 articles
            sources = list({a.get('source', {}).get('name', 'Unknown') for a in articles[:5] if a.get('source')})

            return {
                'sentiment_score': avg_sentiment,
                'sentiment_label': sentiment_label,
                'article_count': len(articles),
                'positive_articles': positive_count,
                'negative_articles': negative_count,
                'neutral_articles': neutral_count,
                'recent_articles': articles[:5],  # Return 5 most recent articles
                'summary': summary,
                'sources': sources
            }
            
        except Exception as e:
            logger.error(f"Error analyzing news sentiment: {str(e)}")
            return {
                'sentiment_score': 0,
                'sentiment_label': 'Neutral',
                'article_count': 0,
                'error': str(e)
            }
    
    def _get_news_articles(self, company_name: str) -> List[Dict[str, Any]]:
        """Get news articles for a company"""
        try:
            # Use News API to get articles
            params = {
                'q': company_name,
                'apiKey': self.news_api_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 20
            }
            
            response = requests.get(self.news_api_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                logger.warning(f"News API request failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting news articles: {str(e)}")
            return []
    
    def _analyze_social_sentiment(self, company_name: str) -> Dict[str, Any]:
        """Analyze social media sentiment"""
        try:
            # This would typically use Twitter API or other social media APIs
            # For now, return placeholder data
            
            # Simulate social media sentiment analysis
            import random
            sentiment_score = random.uniform(-0.3, 0.3)
            
            if sentiment_score > 0.1:
                sentiment_label = 'Positive'
                positive_posts = random.randint(60, 80)
                negative_posts = random.randint(10, 30)
                neutral_posts = random.randint(10, 20)
            elif sentiment_score < -0.1:
                sentiment_label = 'Negative'
                positive_posts = random.randint(10, 30)
                negative_posts = random.randint(60, 80)
                neutral_posts = random.randint(10, 20)
            else:
                sentiment_label = 'Neutral'
                positive_posts = random.randint(30, 50)
                negative_posts = random.randint(30, 50)
                neutral_posts = random.randint(20, 40)
            
            return {
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'total_posts': positive_posts + negative_posts + neutral_posts,
                'positive_posts': positive_posts,
                'negative_posts': negative_posts,
                'neutral_posts': neutral_posts,
                'engagement_rate': random.uniform(0.02, 0.08),
                'trending_topics': self._get_trending_topics(company_name)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing social sentiment: {str(e)}")
            return {
                'sentiment_score': 0,
                'sentiment_label': 'Neutral',
                'error': str(e)
            }
    
    def _get_trending_topics(self, company_name: str) -> List[str]:
        """Get trending topics related to the company"""
        # This would typically use social media APIs
        # For now, return placeholder topics
        topics = [
            f"{company_name} earnings",
            f"{company_name} stock",
            f"{company_name} news",
            f"{company_name} products",
            f"{company_name} leadership"
        ]
        return topics[:3]  # Return top 3 topics
    
    def _analyze_market_sentiment(self, company_name: str) -> Dict[str, Any]:
        """Analyze market sentiment indicators"""
        try:
            # This would typically analyze technical indicators, options data, etc.
            # For now, return placeholder data
            
            import random
            
            # Simulate market sentiment indicators
            return {
                'options_sentiment': {
                    'put_call_ratio': random.uniform(0.5, 1.5),
                    'implied_volatility': random.uniform(0.2, 0.4),
                    'sentiment': 'Bullish' if random.random() > 0.5 else 'Bearish'
                },
                'technical_indicators': {
                    'rsi': random.uniform(30, 70),
                    'macd': random.uniform(-2, 2),
                    'moving_averages': 'Bullish' if random.random() > 0.5 else 'Bearish'
                },
                'institutional_sentiment': {
                    'institutional_ownership': random.uniform(0.3, 0.8),
                    'insider_trading': 'Buying' if random.random() > 0.5 else 'Selling',
                    'analyst_ratings': {
                        'buy': random.randint(5, 15),
                        'hold': random.randint(3, 10),
                        'sell': random.randint(1, 5)
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market sentiment: {str(e)}")
            return {}
    
    def _calculate_overall_sentiment(self, news_sentiment: Dict, 
                                   social_sentiment: Dict, 
                                   market_sentiment: Dict) -> float:
        """Calculate overall sentiment score"""
        try:
            # Weight different sentiment sources
            news_weight = 0.4
            social_weight = 0.3
            market_weight = 0.3
            
            news_score = news_sentiment.get('sentiment_score', 0)
            social_score = social_sentiment.get('sentiment_score', 0)
            
            # Calculate market sentiment score
            market_score = 0
            if market_sentiment:
                options_sentiment = market_sentiment.get('options_sentiment', {})
                put_call_ratio = options_sentiment.get('put_call_ratio', 1.0)
                
                # Convert put/call ratio to sentiment score
                if put_call_ratio < 0.8:
                    market_score = 0.3  # Bullish
                elif put_call_ratio > 1.2:
                    market_score = -0.3  # Bearish
                else:
                    market_score = 0  # Neutral
            
            # Calculate weighted average
            overall_score = (news_score * news_weight + 
                           social_score * social_weight + 
                           market_score * market_weight)
            
            return overall_score
            
        except Exception as e:
            logger.error(f"Error calculating overall sentiment: {str(e)}")
            return 0
    
    def get_sentiment_trends(self, symbol: str) -> Dict[str, Any]:
        """Get sentiment trends over time"""
        try:
            # This would typically analyze historical sentiment data
            # For now, return simulated trend data
            
            import random
            from datetime import datetime, timedelta
            
            # Generate trend data for the last 30 days
            trends = []
            base_sentiment = random.uniform(-0.2, 0.2)
            
            for i in range(30):
                date = datetime.now() - timedelta(days=29-i)
                # Add some random variation to the trend
                sentiment = base_sentiment + random.uniform(-0.1, 0.1)
                trends.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'sentiment_score': sentiment,
                    'volume': random.randint(100, 1000)
                })
            
            return {
                'trend_data': trends,
                'trend_direction': 'Increasing' if base_sentiment > 0 else 'Decreasing',
                'volatility': random.uniform(0.1, 0.3),
                'period': '30 days'
            }
            
        except Exception as e:
            logger.error(f"Error getting sentiment trends for {symbol}: {str(e)}")
            return {}
    
    def _get_sentiment_trends(self, company_name: str) -> Dict[str, Any]:
        """Get sentiment trends for a company (alias for get_sentiment_trends)"""
        return self.get_sentiment_trends(company_name)
    
    def _identify_sentiment_drivers(self, company_name: str) -> List[str]:
        """Identify key drivers of sentiment"""
        try:
            # This would analyze news articles and social media to identify key topics
            # For now, return common sentiment drivers
            
            drivers = [
                'Earnings performance',
                'Product launches',
                'Management changes',
                'Market competition',
                'Regulatory news',
                'Economic conditions'
            ]
            
            # Randomly select 3-4 drivers
            import random
            return random.sample(drivers, random.randint(3, 4))
            
        except Exception as e:
            logger.error(f"Error identifying sentiment drivers: {str(e)}")
            return []
    
    def analyze_competitor_sentiment(self, company_name: str, competitors: List[str]) -> Dict[str, Any]:
        """Compare sentiment with competitors"""
        try:
            competitor_sentiments = {}
            
            for competitor in competitors:
                competitor_sentiment = self.analyze_sentiment(competitor)
                competitor_sentiments[competitor] = competitor_sentiment.get('overall_sentiment', 0)
            
            # Calculate relative sentiment
            company_sentiment = self.analyze_sentiment(company_name)
            company_score = company_sentiment.get('overall_sentiment', 0)
            
            competitor_scores = list(competitor_sentiments.values())
            avg_competitor_score = sum(competitor_scores) / len(competitor_scores) if competitor_scores else 0
            
            relative_sentiment = company_score - avg_competitor_score
            
            return {
                'company_sentiment': company_score,
                'competitor_sentiments': competitor_sentiments,
                'average_competitor_sentiment': avg_competitor_score,
                'relative_sentiment': relative_sentiment,
                'sentiment_ranking': self._calculate_sentiment_ranking(company_score, competitor_scores)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing competitor sentiment: {str(e)}")
            return {}
    
    def _calculate_sentiment_ranking(self, company_score: float, competitor_scores: List[float]) -> int:
        """Calculate sentiment ranking among competitors"""
        try:
            all_scores = [company_score] + competitor_scores
            all_scores.sort(reverse=True)  # Sort in descending order
            
            return all_scores.index(company_score) + 1
            
        except Exception as e:
            logger.error(f"Error calculating sentiment ranking: {str(e)}")
            return 0
    
    def get_sentiment_forecast(self, company_name: str) -> Dict[str, Any]:
        """Forecast sentiment trends"""
        try:
            # This would use machine learning models to forecast sentiment
            # For now, return simple trend projection
            
            current_sentiment = self.analyze_sentiment(company_name)
            current_score = current_sentiment.get('overall_sentiment', 0)
            
            # Simple trend projection
            import random
            
            trend_factor = random.uniform(-0.1, 0.1)
            forecast_score = current_score + trend_factor
            
            return {
                'current_sentiment': current_score,
                'forecasted_sentiment': forecast_score,
                'trend_direction': 'Improving' if trend_factor > 0 else 'Declining',
                'confidence_level': random.uniform(0.6, 0.9),
                'forecast_period': '30 days',
                'key_factors': self._identify_sentiment_drivers(company_name)
            }
            
        except Exception as e:
            logger.error(f"Error getting sentiment forecast for {company_name}: {str(e)}")
            return {} 