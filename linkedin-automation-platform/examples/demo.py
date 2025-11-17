"""
LinkedIn Automation Platform - Demo Script
Complete demonstration of all platform features
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.platform import LinkedInAutomationPlatform
from modules.ai_content_creator import ContentType, UserGoal
from modules.ai_engagement_engine import TargetAudience, EngagementType, RiskLevel
from modules.automation_system import AutomationMode


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_content_creation(platform):
    """Demonstrate AI content creation capabilities."""
    print_section("AI CONTENT CREATION DEMO")
    
    # Generate different types of content
    content_types = [
        (ContentType.TEXT_POST, "AI and Machine Learning"),
        (ContentType.VIRAL_HOOK, "Remote Work Best Practices"),
        (ContentType.CAROUSEL, "Python Tips for Developers")
    ]
    
    for content_type, topic in content_types:
        print(f"\n📝 Creating {content_type.value} about '{topic}'...")
        content = platform.create_optimized_content(
            content_type=content_type,
            topic=topic,
            goal=UserGoal.THOUGHT_LEADERSHIP
        )
        
        print(f"\n✨ Generated Content:")
        print(f"Topic: {content['topic']}")
        print(f"Type: {content['content_type']}")
        print(f"Hashtags: {', '.join(content['hashtags'][:5])}")
        print(f"Estimated Reach: {content['estimated_reach']['estimated_impressions']}")
        print(f"Best Time: {content['best_posting_time']['day']} at {content['best_posting_time']['time']}")
        print(f"\nContent Preview:")
        if isinstance(content['content'], dict):
            print(f"  Format: {content['content']['format']}")
            print(f"  Slides: {content['content']['total_slides']}")
        else:
            preview = content['content'][:200] + "..." if len(content['content']) > 200 else content['content']
            print(f"  {preview}")


def demo_trending_topics(platform):
    """Demonstrate trend analysis."""
    print_section("TRENDING TOPICS ANALYSIS")
    
    print("🔍 Analyzing current LinkedIn trends...\n")
    trends = platform.get_trending_topics()
    
    for trend in trends[:3]:
        print(f"📈 {trend['topic']}")
        print(f"   Trend Score: {trend['trend_score']}/100")
        print(f"   Relevance: {trend['relevance']}")
        print(f"   Suggested Angle: {trend['suggested_angle']}")
        print(f"   Hashtags: {', '.join(trend['hashtags'])}")
        print()


def demo_engagement(platform):
    """Demonstrate AI engagement engine."""
    print_section("AI ENGAGEMENT ENGINE DEMO")
    
    print("🤝 Running automated engagement simulation...\n")
    
    # Simulate engagement with different audiences
    result = platform.engage_with_audience(
        target_audience=TargetAudience.INDUSTRY_LEADERS,
        engagement_types=[
            EngagementType.PROFILE_VIEW,
            EngagementType.LIKE,
            EngagementType.COMMENT
        ],
        duration_hours=1
    )
    
    print(f"✅ Engagement completed!")
    print(f"Total actions: {result['total_engagements']}")
    print(f"Target audience: {result['target_audience']}")
    
    # Check engagement analytics
    analytics = platform.engagement_engine.get_engagement_analytics()
    print(f"\n📊 Engagement Analytics:")
    print(f"Total engagements performed: {analytics['total_engagements']}")
    print(f"Risk level: {analytics['current_risk_level']}")
    print(f"\nBy type:")
    for eng_type, count in analytics['engagement_by_type'].items():
        print(f"  - {eng_type}: {count}")


def demo_scheduling(platform):
    """Demonstrate post scheduling."""
    print_section("SMART SCHEDULING DEMO")
    
    # Create content to schedule
    content = platform.create_optimized_content(
        content_type=ContentType.TEXT_POST,
        topic="Productivity Tips for Developers"
    )
    
    print("📅 Scheduling post with AI-optimized timing...\n")
    
    # Schedule with AI-determined time
    post = platform.schedule_post(content)
    
    print(f"✅ Post scheduled!")
    print(f"Post ID: {post['id']}")
    print(f"Status: {post['status']}")
    print(f"Scheduled for: {post['schedule_time']}")
    
    # Get queue status
    queue_status = platform.automation_system.get_queue_status()
    print(f"\n📋 Queue Status:")
    print(f"Total in queue: {queue_status['total_in_queue']}")
    print(f"Pending approvals: {queue_status['pending_approvals']}")
    print(f"Scheduled posts: {queue_status['scheduled_posts']}")


def demo_analytics(platform):
    """Demonstrate analytics and insights."""
    print_section("ANALYTICS & INSIGHTS DEMO")
    
    # Simulate some post performance data
    print("📊 Simulating performance data...\n")
    
    sample_posts = [
        {"id": "post_1", "published_at": datetime.now().isoformat(), "content": {"content_type": "text_post"}},
        {"id": "post_2", "published_at": datetime.now().isoformat(), "content": {"content_type": "carousel"}},
        {"id": "post_3", "published_at": datetime.now().isoformat(), "content": {"content_type": "viral_hook"}}
    ]
    
    sample_metrics = [
        {"impressions": 1500, "likes": 75, "comments": 12, "shares": 5},
        {"impressions": 2800, "likes": 140, "comments": 23, "shares": 15},
        {"impressions": 1200, "likes": 60, "comments": 8, "shares": 3}
    ]
    
    for post, metrics in zip(sample_posts, sample_metrics):
        platform.track_performance(post["id"], metrics)
    
    # Get content analytics
    content_analytics = platform.content_creator.get_content_analytics()
    print("📈 Content Analytics:")
    print(f"Total posts generated: {content_analytics['total_posts_generated']}")
    print(f"Average quality score: {content_analytics['average_quality_score']:.2f}")
    
    # Get optimization recommendations
    print("\n💡 AI Recommendations:")
    optimization = platform.analytics_optimizer.optimize_future_strategy()
    if isinstance(optimization, dict) and "best_content_type" in optimization:
        print(f"Best performing type: {optimization['best_content_type']['type']}")
        print(f"Recommendation: {optimization['best_content_type']['recommendation']}")


def demo_competitor_benchmarking(platform):
    """Demonstrate competitor benchmarking."""
    print_section("COMPETITOR BENCHMARKING DEMO")
    
    # Simulate competitor data
    competitors = [
        {
            "name": "Industry Leader A",
            "engagement_rate": 4.5,
            "posting_frequency": 5,
            "follower_growth": 3.2
        },
        {
            "name": "Competitor B",
            "engagement_rate": 3.2,
            "posting_frequency": 3,
            "follower_growth": 2.1
        }
    ]
    
    print("🏆 Benchmarking against competitors...\n")
    
    benchmark = platform.benchmark_against_competitors(competitors)
    
    print(f"Your Metrics:")
    print(f"  Engagement Rate: {benchmark['user_metrics'].get('engagement_rate', 0):.2f}%")
    print(f"  Posting Frequency: {benchmark['user_metrics'].get('posting_frequency', 0):.2f} posts/day")
    
    print(f"\nOverall Standing: {benchmark['overall_standing']}")
    
    print(f"\nImprovement Areas:")
    for area in benchmark['improvement_areas']:
        print(f"  • {area}")


def demo_full_automation(platform):
    """Demonstrate full automation mode."""
    print_section("FULL AUTOMATION DEMO")
    
    print("🤖 This would run complete automation including:")
    print("   • AI content creation")
    print("   • Automatic scheduling")
    print("   • Intelligent engagement")
    print("   • Performance tracking")
    print("   • Strategy optimization")
    print("\nFor demo purposes, we're simulating a shorter version...\n")
    
    # Switch to fully automatic mode
    platform.set_automation_level(
        mode=AutomationMode.FULLY_AUTOMATIC,
        risk_level=RiskLevel.SAFE
    )
    
    # Create and schedule some content
    print("📝 Creating and scheduling content...")
    for i in range(3):
        content = platform.create_optimized_content()
        post = platform.schedule_post(content)
        print(f"   ✅ Post {i+1} scheduled for {post['schedule_time']}")
    
    print("\n🎯 In production, this would:")
    print("   • Run continuously for specified duration")
    print("   • Publish posts at optimal times")
    print("   • Engage with target audiences")
    print("   • Track all performance metrics")
    print("   • Learn and optimize automatically")


def demo_dashboard(platform):
    """Demonstrate comprehensive dashboard."""
    print_section("COMPREHENSIVE DASHBOARD")
    
    dashboard = platform.get_comprehensive_dashboard()
    
    print("🎛️ Platform Status:")
    status = dashboard['platform_status']
    print(f"   User: {status['user']}")
    print(f"   Industry: {status['industry']}")
    print(f"   Running: {status['is_running']}")
    
    print(f"\n📊 System Status:")
    auto_status = dashboard['automation_status']
    print(f"   Mode: {auto_status['automation_mode']}")
    print(f"   Total published: {auto_status['total_published']}")
    
    current_status = platform.get_status()
    print(f"   Pending approvals: {current_status['pending_approvals']}")
    print(f"   Scheduled posts: {current_status['scheduled_posts']}")
    
    print(f"\n💡 AI Recommendations:")
    recommendations = dashboard['ai_recommendations']
    print(f"   Posting schedule: {recommendations['posting_schedule']}")
    print(f"   Growth opportunities:")
    for opp in recommendations['growth_opportunities'][:3]:
        print(f"      • {opp}")


def main():
    """Run the complete demo."""
    print("\n" + "="*70)
    print("  LINKEDIN AUTOMATION & AI POST MAKER PLATFORM")
    print("  Complete Feature Demonstration")
    print("="*70)
    
    # Create user profile
    user_profile = {
        "name": "Demo User",
        "email": "demo@example.com",
        "industry": "Technology",
        "title": "Software Engineer",
        "primary_goal": "BRAND_BUILDING",
        "tone_preference": "professional",
        "custom_hashtags": ["#TechInnovation", "#Coding"]
    }
    
    print("\n🚀 Initializing platform...")
    
    # Initialize platform
    platform = LinkedInAutomationPlatform(
        user_profile=user_profile,
        automation_mode=AutomationMode.MANUAL_APPROVAL,
        risk_level=RiskLevel.SAFE
    )
    
    # Run all demos
    demo_content_creation(platform)
    demo_trending_topics(platform)
    demo_engagement(platform)
    demo_scheduling(platform)
    demo_analytics(platform)
    demo_competitor_benchmarking(platform)
    demo_full_automation(platform)
    demo_dashboard(platform)
    
    print_section("DEMO COMPLETED")
    print("✨ All features demonstrated successfully!")
    print("\n📚 For more information:")
    print("   • README.md - Quick start guide")
    print("   • docs/PRODUCT_DESCRIPTION.md - Complete feature overview")
    print("   • docs/PRD.md - Product requirements")
    print("\n🎯 Ready to transform your LinkedIn presence!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
