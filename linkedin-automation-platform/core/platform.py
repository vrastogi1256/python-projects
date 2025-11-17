"""
LinkedIn Automation Platform Core
Main platform class that integrates all modules and provides unified interface.
"""

from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.ai_content_creator import AIContentCreator, ContentType, UserGoal
from modules.ai_engagement_engine import AIEngagementEngine, EngagementType, TargetAudience, RiskLevel
from modules.automation_system import SmartAutomationSystem, AutomationMode, PostStatus
from modules.analytics_optimizer import AnalyticsOptimizer


class LinkedInAutomationPlatform:
    """
    Main platform class - the all-in-one intelligent ecosystem for LinkedIn automation.
    
    This platform automatically:
    - Creates optimized content
    - Engages with the right audience
    - Analyzes performance
    - Learns from user behavior
    - Optimizes posting strategy
    """

    def __init__(
        self,
        user_profile: Dict,
        automation_mode: AutomationMode = AutomationMode.MANUAL_APPROVAL,
        risk_level: RiskLevel = RiskLevel.SAFE
    ):
        """
        Initialize the LinkedIn Automation Platform.

        Args:
            user_profile: User profile with name, industry, goals, etc.
            automation_mode: Level of automation (fully automatic or manual approval)
            risk_level: Risk level for engagement activities
        """
        self.user_profile = user_profile
        
        # Initialize all modules
        self.content_creator = AIContentCreator(
            user_profile=user_profile,
            niche=user_profile.get("industry", "general")
        )
        
        self.engagement_engine = AIEngagementEngine(
            user_profile=user_profile,
            risk_level=risk_level
        )
        
        # Create properly formatted account for automation system
        primary_account = {
            "id": "account_1",
            "name": user_profile.get("name"),
            "email": user_profile.get("email"),
            "is_primary": True,
            "status": "active"
        }
        
        self.automation_system = SmartAutomationSystem(
            mode=automation_mode,
            user_accounts=[primary_account]
        )
        
        self.analytics_optimizer = AnalyticsOptimizer(
            user_profile=user_profile
        )
        
        self.is_running = False
        self.created_at = datetime.now()

        print("🚀 LinkedIn Automation Platform Initialized")
        print(f"👤 User: {user_profile.get('name', 'Unknown')}")
        print(f"🎯 Industry: {user_profile.get('industry', 'General')}")
        print(f"⚙️ Automation Mode: {automation_mode.value}")
        print(f"🛡️ Risk Level: {risk_level.value}")

    def run_full_automation(
        self,
        duration_days: int = 7,
        posts_per_day: int = 1,
        engagement_hours: int = 4
    ) -> Dict:
        """
        Run complete automation for specified duration.
        Creates content, schedules posts, and engages with audience automatically.

        Args:
            duration_days: How many days to run automation
            posts_per_day: Number of posts to create per day
            engagement_hours: Hours of engagement activity per day

        Returns:
            Summary of automation run
        """
        self.is_running = True
        
        print(f"\n{'='*60}")
        print(f"🤖 STARTING FULL AUTOMATION")
        print(f"{'='*60}")
        print(f"Duration: {duration_days} days")
        print(f"Posts per day: {posts_per_day}")
        print(f"Engagement hours: {engagement_hours}")
        print(f"{'='*60}\n")

        summary = {
            "start_time": datetime.now().isoformat(),
            "duration_days": duration_days,
            "content_created": [],
            "engagement_activities": [],
            "posts_published": []
        }

        # Create and schedule content
        print("📝 Creating content...")
        for day in range(duration_days):
            for post_num in range(posts_per_day):
                content = self.create_optimized_content()
                summary["content_created"].append(content)
                
                # Add to posting queue
                post = self.automation_system.add_post_to_queue(content)
                
                # Auto-approve if in fully automatic mode
                if self.automation_system.mode == AutomationMode.FULLY_AUTOMATIC:
                    self.automation_system.approve_post(post["id"])

        # Run engagement
        print(f"\n🤝 Starting engagement activities...")
        engagement_result = self.engagement_engine.engage_automatically(
            target_audience=TargetAudience.PEERS,
            engagement_types=[
                EngagementType.PROFILE_VIEW,
                EngagementType.LIKE,
                EngagementType.COMMENT,
                EngagementType.CONNECTION_REQUEST
            ],
            duration_hours=engagement_hours
        )
        summary["engagement_activities"] = engagement_result

        # Publish scheduled posts
        print(f"\n📤 Publishing scheduled posts...")
        published = self.automation_system.publish_scheduled_posts()
        summary["posts_published"] = published

        summary["end_time"] = datetime.now().isoformat()
        summary["status"] = "completed"
        
        self.is_running = False

        print(f"\n{'='*60}")
        print(f"✅ AUTOMATION COMPLETED")
        print(f"{'='*60}")
        print(f"Content created: {len(summary['content_created'])}")
        print(f"Posts published: {len(summary['posts_published'])}")
        print(f"Engagement actions: {engagement_result['total_engagements']}")
        print(f"{'='*60}\n")

        return summary

    def create_optimized_content(
        self,
        content_type: Optional[ContentType] = None,
        topic: Optional[str] = None,
        goal: Optional[UserGoal] = None
    ) -> Dict:
        """
        Create AI-optimized content for LinkedIn.

        Args:
            content_type: Type of content (if None, AI chooses best)
            topic: Topic for content (if None, AI suggests trending topic)
            goal: User's goal for this content

        Returns:
            Generated content with metadata
        """
        # Use AI to determine best content type if not specified
        if not content_type:
            content_type = self._suggest_best_content_type()

        # Use default goal from user profile if not specified
        if not goal:
            goal = UserGoal[self.user_profile.get("primary_goal", "BRAND_BUILDING")]

        content = self.content_creator.generate_content(
            content_type=content_type,
            topic=topic,
            goal=goal,
            tone=self.user_profile.get("tone_preference", "professional")
        )

        # Personalize based on user preferences
        personalized = self.content_creator.personalize_content(
            content,
            self.user_profile
        )

        print(f"✨ Created {content_type.value} about '{personalized['topic']}'")

        return personalized

    def _suggest_best_content_type(self) -> ContentType:
        """Use AI learning to suggest best content type."""
        # Check analytics for best performing type
        learning_model = self.analytics_optimizer.learning_model
        
        if learning_model:
            best_type = max(
                learning_model.keys(),
                key=lambda x: learning_model[x]["average_score"]
            )
            return ContentType[best_type.upper().replace(" ", "_")]

        # Default rotation if no data
        types = [
            ContentType.TEXT_POST,
            ContentType.CAROUSEL,
            ContentType.VIRAL_HOOK,
            ContentType.LONG_FORM
        ]
        
        import random
        return random.choice(types)

    def engage_with_audience(
        self,
        target_audience: TargetAudience,
        engagement_types: Optional[List[EngagementType]] = None,
        duration_hours: int = 2
    ) -> Dict:
        """
        Engage with target audience automatically.

        Args:
            target_audience: Type of audience to target
            engagement_types: Types of engagements (if None, uses all)
            duration_hours: How long to run engagement

        Returns:
            Engagement summary
        """
        if not engagement_types:
            engagement_types = [
                EngagementType.PROFILE_VIEW,
                EngagementType.LIKE,
                EngagementType.COMMENT
            ]

        result = self.engagement_engine.engage_automatically(
            target_audience=target_audience,
            engagement_types=engagement_types,
            duration_hours=duration_hours
        )

        return result

    def get_comprehensive_dashboard(self, period: str = "30d") -> Dict:
        """
        Get comprehensive dashboard with all metrics and insights.

        Args:
            period: Time period for analytics

        Returns:
            Complete dashboard data
        """
        dashboard = {
            "platform_status": {
                "is_running": self.is_running,
                "user": self.user_profile.get("name"),
                "industry": self.user_profile.get("industry"),
                "created_at": self.created_at.isoformat()
            },
            "content_analytics": self.content_creator.get_content_analytics(),
            "engagement_analytics": self.engagement_engine.get_engagement_analytics(),
            "automation_status": self.automation_system.get_system_status(),
            "performance_dashboard": self.analytics_optimizer.get_dashboard_data(period),
            "ai_recommendations": self._get_ai_recommendations()
        }

        return dashboard

    def _get_ai_recommendations(self) -> Dict:
        """Get AI-powered recommendations for improvement."""
        optimization = self.analytics_optimizer.optimize_future_strategy()
        
        recommendations = {
            "content_strategy": optimization if optimization else {},
            "engagement_recommendations": [
                "Focus on commenting to build relationships",
                "Target industry leaders for visibility",
                "Maintain consistent engagement schedule"
            ],
            "posting_schedule": "Based on your performance, post on Tuesday and Thursday at 10 AM",
            "growth_opportunities": [
                "Expand into video content",
                "Engage with trending topics",
                "Build strategic partnerships"
            ]
        }

        return recommendations

    def schedule_post(
        self,
        content: Dict,
        schedule_time: Optional[datetime] = None
    ) -> Dict:
        """
        Schedule a post for publication.

        Args:
            content: Post content
            schedule_time: When to publish (None for optimal time)

        Returns:
            Scheduled post info
        """
        post = self.automation_system.add_post_to_queue(
            content=content,
            schedule_time=schedule_time
        )

        print(f"📅 Post scheduled: {post['id']}")
        if post.get("schedule_time"):
            print(f"⏰ Will publish at: {post['schedule_time']}")

        return post

    def approve_pending_posts(self) -> List[Dict]:
        """
        Approve all pending posts.

        Returns:
            List of approved posts
        """
        approved = []
        for post in self.automation_system.pending_approvals[:]:
            result = self.automation_system.approve_post(post["id"])
            approved.append(result)

        print(f"✅ Approved {len(approved)} post(s)")
        return approved

    def track_performance(self, post_id: str, metrics: Dict) -> Dict:
        """
        Track performance of a published post.

        Args:
            post_id: ID of the post
            metrics: Current metrics (impressions, likes, comments, etc.)

        Returns:
            Performance analysis
        """
        # Find the post
        post = self.automation_system._find_post(post_id)
        
        if not post:
            return {"error": "Post not found"}

        # Track in analytics
        performance = self.analytics_optimizer.track_post_performance(post, metrics)
        
        # Update post metrics
        post["metrics"] = metrics

        print(f"📊 Performance tracked for post {post_id}")
        print(f"Score: {performance['performance_score']}")
        print(f"Engagement Rate: {performance['engagement_rate']:.2f}%")

        return performance

    def benchmark_against_competitors(self, competitors: List[Dict]) -> Dict:
        """
        Compare performance with competitors.

        Args:
            competitors: List of competitor data

        Returns:
            Comparison analysis
        """
        return self.analytics_optimizer.benchmark_competitors(competitors)

    def enable_stealth_mode(self):
        """Enable stealth mode for safe, low-profile operation."""
        self.engagement_engine.enable_stealth_mode()
        print("🕵️ Platform operating in stealth mode")

    def set_automation_level(
        self,
        mode: AutomationMode,
        risk_level: Optional[RiskLevel] = None
    ):
        """
        Adjust automation settings.

        Args:
            mode: Automation mode
            risk_level: Optional risk level for engagement
        """
        self.automation_system.set_automation_mode(mode)
        
        if risk_level:
            self.engagement_engine.set_risk_level(risk_level)

        print(f"⚙️ Automation updated: {mode.value}")
        if risk_level:
            print(f"🛡️ Risk level: {risk_level.value}")

    def get_trending_topics(self) -> List[Dict]:
        """
        Get current trending topics for content ideas.

        Returns:
            List of trending topics
        """
        return self.content_creator.analyze_trends()

    def export_all_data(self) -> Dict:
        """
        Export all platform data for backup or analysis.

        Returns:
            Complete platform data
        """
        return {
            "user_profile": self.user_profile,
            "content_history": self.content_creator.content_history,
            "engagement_history": self.engagement_engine.engagement_history,
            "post_queue": self.automation_system.post_queue,
            "published_posts": self.automation_system.published_posts,
            "performance_data": self.analytics_optimizer.performance_data,
            "learning_model": self.analytics_optimizer.learning_model
        }

    def get_status(self) -> Dict:
        """
        Get current platform status.

        Returns:
            Status information
        """
        return {
            "is_running": self.is_running,
            "automation_mode": self.automation_system.mode.value,
            "risk_level": self.engagement_engine.risk_level.value,
            "pending_approvals": len(self.automation_system.pending_approvals),
            "scheduled_posts": len([
                p for p in self.automation_system.post_queue
                if p["status"] == PostStatus.SCHEDULED.value
            ]),
            "total_published": len(self.automation_system.published_posts),
            "engagement_today": len([
                e for e in self.engagement_engine.engagement_history
                if e["timestamp"].startswith(datetime.now().date().isoformat())
            ])
        }

    def __repr__(self) -> str:
        """String representation of the platform."""
        return (
            f"LinkedInAutomationPlatform("
            f"user={self.user_profile.get('name')}, "
            f"mode={self.automation_system.mode.value}, "
            f"status={'Running' if self.is_running else 'Idle'})"
        )
