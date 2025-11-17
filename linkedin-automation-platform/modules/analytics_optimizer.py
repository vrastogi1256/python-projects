"""
Analytics & Optimization System
Advanced analytics dashboard with AI-powered optimization and competitor benchmarking.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


class AnalyticsOptimizer:
    """
    Comprehensive analytics and optimization system that tracks performance,
    learns from data, and continuously improves content strategy.
    """

    def __init__(self, user_profile: Dict):
        """
        Initialize the analytics optimizer.

        Args:
            user_profile: User profile information
        """
        self.user_profile = user_profile
        self.performance_data = []
        self.optimization_history = []
        self.learning_model = {}
        self.competitors = []

    def track_post_performance(self, post: Dict, metrics: Dict) -> Dict:
        """
        Track performance metrics for a post.

        Args:
            post: Post object
            metrics: Current metrics for the post

        Returns:
            Performance record
        """
        performance = {
            "post_id": post.get("id"),
            "published_at": post.get("published_at"),
            "content_type": post.get("content", {}).get("content_type"),
            "metrics": metrics,
            "tracked_at": datetime.now().isoformat()
        }

        # Calculate engagement rate
        total_engagement = metrics.get("likes", 0) + metrics.get("comments", 0) + metrics.get("shares", 0)
        impressions = metrics.get("impressions", 1)
        performance["engagement_rate"] = (total_engagement / impressions) * 100 if impressions > 0 else 0

        # Calculate performance score
        performance["performance_score"] = self._calculate_performance_score(metrics)

        self.performance_data.append(performance)
        
        # Update learning model
        self._update_learning_model(performance)

        return performance

    def _calculate_performance_score(self, metrics: Dict) -> float:
        """
        Calculate overall performance score for a post.

        Args:
            metrics: Post metrics

        Returns:
            Performance score (0-100)
        """
        # Weighted scoring
        impressions_score = min(100, (metrics.get("impressions", 0) / 1000) * 30)
        likes_score = min(100, (metrics.get("likes", 0) / 100) * 25)
        comments_score = min(100, (metrics.get("comments", 0) / 20) * 25)
        shares_score = min(100, (metrics.get("shares", 0) / 10) * 20)

        total_score = impressions_score + likes_score + comments_score + shares_score
        return round(total_score, 2)

    def get_dashboard_data(self, period: str = "30d") -> Dict:
        """
        Get comprehensive dashboard data.

        Args:
            period: Time period (7d, 30d, 90d, all)

        Returns:
            Dashboard data with all key metrics
        """
        filtered_data = self._filter_by_period(period)

        if not filtered_data:
            return {"message": "No data available for the selected period"}

        # Calculate aggregate metrics
        total_impressions = sum(p["metrics"].get("impressions", 0) for p in filtered_data)
        total_likes = sum(p["metrics"].get("likes", 0) for p in filtered_data)
        total_comments = sum(p["metrics"].get("comments", 0) for p in filtered_data)
        total_shares = sum(p["metrics"].get("shares", 0) for p in filtered_data)
        total_profile_views = sum(p["metrics"].get("profile_views", 0) for p in filtered_data)

        total_engagement = total_likes + total_comments + total_shares
        avg_engagement_rate = (total_engagement / total_impressions * 100) if total_impressions > 0 else 0

        # Get trends
        growth_trends = self._calculate_growth_trends(filtered_data)

        # Best performing content
        best_posts = self._get_best_performing_posts(filtered_data, limit=5)

        # Posting patterns
        posting_patterns = self._analyze_posting_patterns(filtered_data)

        dashboard = {
            "period": period,
            "summary": {
                "total_posts": len(filtered_data),
                "total_impressions": total_impressions,
                "total_engagement": total_engagement,
                "average_engagement_rate": f"{avg_engagement_rate:.2f}%",
                "total_profile_views": total_profile_views,
                "follower_growth": self._calculate_follower_growth(period)
            },
            "detailed_metrics": {
                "likes": total_likes,
                "comments": total_comments,
                "shares": total_shares,
                "average_likes_per_post": round(total_likes / len(filtered_data), 2) if filtered_data else 0,
                "average_comments_per_post": round(total_comments / len(filtered_data), 2) if filtered_data else 0
            },
            "growth_trends": growth_trends,
            "best_performing_posts": best_posts,
            "posting_patterns": posting_patterns,
            "recommendations": self._generate_recommendations(filtered_data)
        }

        return dashboard

    def _filter_by_period(self, period: str) -> List[Dict]:
        """Filter performance data by time period."""
        if period == "all":
            return self.performance_data

        days_map = {"7d": 7, "30d": 30, "90d": 90}
        days = days_map.get(period, 30)

        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered = []
        for record in self.performance_data:
            if "published_at" in record and record["published_at"]:
                post_date = datetime.fromisoformat(record["published_at"])
                if post_date >= cutoff_date:
                    filtered.append(record)

        return filtered

    def _calculate_growth_trends(self, data: List[Dict]) -> Dict:
        """Calculate growth trends over time."""
        if len(data) < 2:
            return {"message": "Need more data to calculate trends"}

        # Split data into two halves
        mid_point = len(data) // 2
        first_half = data[:mid_point]
        second_half = data[mid_point:]

        def avg_metric(dataset, metric):
            values = [p["metrics"].get(metric, 0) for p in dataset]
            return sum(values) / len(values) if values else 0

        metrics = ["impressions", "likes", "comments", "shares"]
        trends = {}

        for metric in metrics:
            first_avg = avg_metric(first_half, metric)
            second_avg = avg_metric(second_half, metric)
            
            if first_avg > 0:
                change = ((second_avg - first_avg) / first_avg) * 100
            else:
                change = 0

            trends[metric] = {
                "previous_average": round(first_avg, 2),
                "current_average": round(second_avg, 2),
                "change_percentage": f"{change:+.2f}%",
                "trend": "up" if change > 0 else "down" if change < 0 else "stable"
            }

        return trends

    def _get_best_performing_posts(self, data: List[Dict], limit: int = 5) -> List[Dict]:
        """Get best performing posts."""
        sorted_posts = sorted(
            data,
            key=lambda x: x.get("performance_score", 0),
            reverse=True
        )

        return [{
            "post_id": post["post_id"],
            "performance_score": post["performance_score"],
            "engagement_rate": f"{post['engagement_rate']:.2f}%",
            "impressions": post["metrics"].get("impressions", 0),
            "total_engagement": (
                post["metrics"].get("likes", 0) +
                post["metrics"].get("comments", 0) +
                post["metrics"].get("shares", 0)
            )
        } for post in sorted_posts[:limit]]

    def _analyze_posting_patterns(self, data: List[Dict]) -> Dict:
        """Analyze when posts perform best."""
        if not data:
            return {}

        hourly_performance = defaultdict(list)
        daily_performance = defaultdict(list)

        for record in data:
            if not record.get("published_at"):
                continue

            post_time = datetime.fromisoformat(record["published_at"])
            hour = post_time.hour
            day = post_time.strftime("%A")

            score = record.get("performance_score", 0)
            hourly_performance[hour].append(score)
            daily_performance[day].append(score)

        best_hours = {}
        for hour, scores in hourly_performance.items():
            best_hours[hour] = round(sum(scores) / len(scores), 2)

        best_days = {}
        for day, scores in daily_performance.items():
            best_days[day] = round(sum(scores) / len(scores), 2)

        # Find optimal times
        optimal_hour = max(best_hours, key=best_hours.get) if best_hours else None
        optimal_day = max(best_days, key=best_days.get) if best_days else None

        return {
            "best_hours": best_hours,
            "best_days": best_days,
            "optimal_posting_hour": optimal_hour,
            "optimal_posting_day": optimal_day,
            "recommendation": f"Best time to post: {optimal_day} at {optimal_hour}:00" if optimal_day and optimal_hour else "Need more data"
        }

    def _calculate_follower_growth(self, period: str) -> Dict:
        """Calculate follower growth for period."""
        # Simulate follower growth based on engagement
        days = {"7d": 7, "30d": 30, "90d": 90, "all": 365}.get(period, 30)
        
        estimated_growth = random.randint(10, 50) * (days // 7)
        growth_rate = random.uniform(1.5, 4.5)

        return {
            "new_followers": estimated_growth,
            "growth_rate": f"+{growth_rate:.1f}%",
            "projection": f"+{estimated_growth * 2} in next {period}"
        }

    def _generate_recommendations(self, data: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on performance."""
        recommendations = []

        if not data:
            return ["Start posting to get personalized recommendations"]

        # Analyze engagement rates
        avg_engagement_rate = sum(p.get("engagement_rate", 0) for p in data) / len(data)

        if avg_engagement_rate < 2:
            recommendations.append("💡 Engagement rate is below average. Try more interactive content like polls or questions.")
        elif avg_engagement_rate > 5:
            recommendations.append("🎉 Excellent engagement rate! Keep up the good work with your current content strategy.")

        # Analyze posting frequency
        posting_frequency = len(data) / 30  # posts per day
        if posting_frequency < 0.5:
            recommendations.append("📅 Consider posting more frequently (at least 3-4 times per week) for better visibility.")
        elif posting_frequency > 2:
            recommendations.append("⚠️ You're posting frequently. Ensure quality isn't compromised for quantity.")

        # Content type analysis
        content_types = defaultdict(int)
        for record in data:
            ct = record.get("content_type")
            if ct:
                content_types[ct] += 1

        if len(content_types) < 3:
            recommendations.append("🎨 Diversify your content types (text, carousel, video) to reach different audience segments.")

        # Time-based recommendations
        patterns = self._analyze_posting_patterns(data)
        if patterns.get("optimal_posting_hour"):
            recommendations.append(
                f"⏰ Your best performing hour is {patterns['optimal_posting_hour']}:00. "
                f"Schedule more posts around this time."
            )

        return recommendations

    def _update_learning_model(self, performance: Dict):
        """Update the AI learning model based on new performance data."""
        content_type = performance.get("content_type")
        score = performance.get("performance_score", 0)

        if content_type not in self.learning_model:
            self.learning_model[content_type] = {
                "total_posts": 0,
                "average_score": 0,
                "best_score": 0,
                "trends": []
            }

        model = self.learning_model[content_type]
        model["total_posts"] += 1
        
        # Update average
        current_avg = model["average_score"]
        model["average_score"] = (current_avg * (model["total_posts"] - 1) + score) / model["total_posts"]
        
        # Update best
        if score > model["best_score"]:
            model["best_score"] = score

        # Track trend
        model["trends"].append(score)
        if len(model["trends"]) > 10:
            model["trends"].pop(0)

    def optimize_future_strategy(self) -> Dict:
        """
        Use AI learning to optimize future content strategy.

        Returns:
            Optimization recommendations
        """
        if not self.learning_model:
            return {"message": "Need more data to optimize strategy"}

        # Find best performing content type
        best_type = max(
            self.learning_model.keys(),
            key=lambda x: self.learning_model[x]["average_score"]
        )

        # Find worst performing
        worst_type = min(
            self.learning_model.keys(),
            key=lambda x: self.learning_model[x]["average_score"]
        )

        optimization = {
            "best_content_type": {
                "type": best_type,
                "average_score": round(self.learning_model[best_type]["average_score"], 2),
                "recommendation": f"Increase frequency of {best_type} posts"
            },
            "needs_improvement": {
                "type": worst_type,
                "average_score": round(self.learning_model[worst_type]["average_score"], 2),
                "recommendation": f"Experiment with different approaches for {worst_type}"
            },
            "content_mix_recommendation": self._recommend_content_mix(),
            "posting_frequency": self._recommend_posting_frequency(),
            "engagement_tactics": self._recommend_engagement_tactics()
        }

        self.optimization_history.append({
            "timestamp": datetime.now().isoformat(),
            "optimization": optimization
        })

        return optimization

    def _recommend_content_mix(self) -> Dict:
        """Recommend optimal content type mix."""
        if not self.learning_model:
            return {"message": "Need more data"}

        total_score = sum(m["average_score"] for m in self.learning_model.values())
        
        recommendations = {}
        for content_type, model in self.learning_model.items():
            percentage = (model["average_score"] / total_score * 100) if total_score > 0 else 0
            recommendations[content_type] = f"{percentage:.1f}%"

        return recommendations

    def _recommend_posting_frequency(self) -> str:
        """Recommend optimal posting frequency."""
        if len(self.performance_data) < 10:
            return "Post 3-4 times per week to build consistency"

        recent_data = self.performance_data[-30:]  # Last 30 posts
        avg_score = sum(p.get("performance_score", 0) for p in recent_data) / len(recent_data)

        if avg_score > 80:
            return "Your current posting frequency is optimal. Maintain 5-7 posts per week."
        elif avg_score > 60:
            return "Solid performance. Consider posting 4-5 times per week."
        else:
            return "Focus on quality over quantity. Post 2-3 high-quality posts per week."

    def _recommend_engagement_tactics(self) -> List[str]:
        """Recommend tactics to boost engagement."""
        return [
            "Ask questions in your posts to encourage comments",
            "Use relevant hashtags (5-10 per post)",
            "Respond to comments within the first hour of posting",
            "Tag relevant people or companies when appropriate",
            "Share personal stories and experiences",
            "Use engaging visuals (images, carousels, videos)",
            "Post during peak activity hours",
            "End posts with a clear call-to-action"
        ]

    def benchmark_competitors(self, competitors: List[Dict]) -> Dict:
        """
        Benchmark performance against competitors.

        Args:
            competitors: List of competitor profiles with metrics

        Returns:
            Comparison data
        """
        self.competitors = competitors

        # Calculate user's average metrics
        user_avg = self._calculate_average_metrics()

        # Compare with each competitor
        comparisons = []
        for competitor in competitors:
            comparison = {
                "competitor_name": competitor.get("name"),
                "user_vs_competitor": {
                    "engagement_rate": self._compare_metric(
                        user_avg.get("engagement_rate", 0),
                        competitor.get("engagement_rate", 0)
                    ),
                    "posting_frequency": self._compare_metric(
                        user_avg.get("posting_frequency", 0),
                        competitor.get("posting_frequency", 0)
                    ),
                    "follower_growth": self._compare_metric(
                        user_avg.get("follower_growth", 0),
                        competitor.get("follower_growth", 0)
                    )
                },
                "insights": self._generate_competitor_insights(competitor, user_avg)
            }
            comparisons.append(comparison)

        return {
            "user_metrics": user_avg,
            "competitor_comparisons": comparisons,
            "overall_standing": self._calculate_overall_standing(user_avg, competitors),
            "improvement_areas": self._identify_improvement_areas(user_avg, competitors)
        }

    def _calculate_average_metrics(self) -> Dict:
        """Calculate user's average metrics."""
        if not self.performance_data:
            return {}

        recent = self.performance_data[-30:]
        
        total_engagement = sum(
            p["metrics"].get("likes", 0) + 
            p["metrics"].get("comments", 0) + 
            p["metrics"].get("shares", 0)
            for p in recent
        )
        total_impressions = sum(p["metrics"].get("impressions", 1) for p in recent)

        return {
            "engagement_rate": (total_engagement / total_impressions * 100) if total_impressions > 0 else 0,
            "posting_frequency": len(recent) / 30,  # posts per day
            "follower_growth": random.uniform(2, 5),  # Simulated
            "average_impressions": total_impressions / len(recent) if recent else 0
        }

    def _compare_metric(self, user_value: float, competitor_value: float) -> Dict:
        """Compare a metric between user and competitor."""
        if competitor_value == 0:
            return {"comparison": "N/A"}

        difference = ((user_value - competitor_value) / competitor_value) * 100

        return {
            "user": round(user_value, 2),
            "competitor": round(competitor_value, 2),
            "difference": f"{difference:+.1f}%",
            "status": "ahead" if difference > 0 else "behind" if difference < -5 else "comparable"
        }

    def _generate_competitor_insights(self, competitor: Dict, user_avg: Dict) -> List[str]:
        """Generate insights from competitor comparison."""
        insights = []

        if competitor.get("engagement_rate", 0) > user_avg.get("engagement_rate", 0) * 1.2:
            insights.append(f"{competitor['name']} has significantly higher engagement. Study their content strategy.")

        if competitor.get("posting_frequency", 0) > user_avg.get("posting_frequency", 0):
            insights.append(f"{competitor['name']} posts more frequently. Consider increasing your posting cadence.")

        return insights

    def _calculate_overall_standing(self, user_avg: Dict, competitors: List[Dict]) -> str:
        """Calculate overall standing vs competitors."""
        user_score = user_avg.get("engagement_rate", 0) + user_avg.get("posting_frequency", 0) * 10

        ahead_of = sum(
            1 for c in competitors
            if (c.get("engagement_rate", 0) + c.get("posting_frequency", 0) * 10) < user_score
        )

        total = len(competitors)
        
        if ahead_of / total > 0.7:
            return "Leading - You're outperforming most competitors"
        elif ahead_of / total > 0.3:
            return "Competitive - You're performing on par with competitors"
        else:
            return "Developing - There's room to improve vs competitors"

    def _identify_improvement_areas(self, user_avg: Dict, competitors: List[Dict]) -> List[str]:
        """Identify areas for improvement."""
        areas = []

        avg_competitor_engagement = sum(c.get("engagement_rate", 0) for c in competitors) / len(competitors)
        
        if user_avg.get("engagement_rate", 0) < avg_competitor_engagement:
            areas.append("Improve engagement rate through more interactive content")

        avg_competitor_frequency = sum(c.get("posting_frequency", 0) for c in competitors) / len(competitors)
        
        if user_avg.get("posting_frequency", 0) < avg_competitor_frequency * 0.7:
            areas.append("Increase posting frequency to stay competitive")

        return areas if areas else ["You're performing well across all metrics!"]

    def export_analytics(self, format: str = "json") -> str:
        """
        Export analytics data.

        Args:
            format: Export format (json, csv)

        Returns:
            Exported data
        """
        import json as json_lib

        dashboard = self.get_dashboard_data("all")
        
        if format == "json":
            return json_lib.dumps(dashboard, indent=2)
        
        # For CSV or other formats
        return str(dashboard)
