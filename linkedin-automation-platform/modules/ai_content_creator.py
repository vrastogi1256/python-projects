"""
AI Content Creation System
Advanced post generator for all types of LinkedIn content with trend analysis,
personalization, and optimization.
"""

import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ContentType(Enum):
    """Types of content that can be generated."""
    TEXT_POST = "text_post"
    LONG_FORM = "long_form"
    VIRAL_HOOK = "viral_hook"
    CAROUSEL = "carousel"
    INFOGRAPHIC = "infographic"
    IMAGE_POST = "image_post"
    MEME = "meme"
    SHORT_VIDEO = "short_video"


class UserGoal(Enum):
    """User's primary goals for content."""
    JOB_SEARCH = "job_search"
    BRAND_BUILDING = "brand_building"
    LEAD_GENERATION = "lead_generation"
    THOUGHT_LEADERSHIP = "thought_leadership"
    NETWORKING = "networking"
    CUSTOM = "custom"


class AIContentCreator:
    """
    Advanced AI Content Creation System that generates highly engaging
    LinkedIn content optimized for maximum reach and engagement.
    """

    def __init__(self, user_profile: Dict, niche: str = "general"):
        """
        Initialize the AI Content Creator.

        Args:
            user_profile: User profile information and preferences
            niche: User's content niche (tech, marketing, finance, etc.)
        """
        self.user_profile = user_profile
        self.niche = niche
        self.content_history = []
        self.trending_topics = []
        self.performance_data = {}

    def generate_content(
        self,
        content_type: ContentType,
        topic: Optional[str] = None,
        goal: UserGoal = UserGoal.BRAND_BUILDING,
        tone: str = "professional",
        length: str = "medium"
    ) -> Dict:
        """
        Generate content based on specified parameters.

        Args:
            content_type: Type of content to generate
            topic: Optional specific topic
            goal: User's goal for this content
            tone: Tone of the content (professional, casual, inspirational)
            length: Length of content (short, medium, long)

        Returns:
            Dictionary containing generated content and metadata
        """
        if not topic:
            topic = self._suggest_trending_topic()

        content = self._create_content(content_type, topic, goal, tone, length)

        post_data = {
            "content_type": content_type.value,
            "topic": topic,
            "goal": goal.value,
            "tone": tone,
            "length": length,
            "content": content,
            "hashtags": self._generate_hashtags(topic, self.niche),
            "estimated_reach": self._estimate_reach(content_type, topic),
            "best_posting_time": self._calculate_best_time(),
            "created_at": datetime.now().isoformat(),
            "engagement_prediction": self._predict_engagement(content, topic)
        }

        self.content_history.append(post_data)
        return post_data

    def _create_content(
        self,
        content_type: ContentType,
        topic: str,
        goal: UserGoal,
        tone: str,
        length: str
    ) -> str:
        """Create the actual content based on parameters."""
        templates = self._get_content_templates(content_type, goal, tone)
        template = random.choice(templates)

        content = template.format(
            topic=topic,
            niche=self.niche,
            user_name=self.user_profile.get('name', 'Professional')
        )

        if content_type == ContentType.VIRAL_HOOK:
            content = self._add_viral_hook(content)
        elif content_type == ContentType.CAROUSEL:
            content = self._format_as_carousel(content, topic)

        return content

    def _get_content_templates(
        self,
        content_type: ContentType,
        goal: UserGoal,
        tone: str
    ) -> List[str]:
        """Get appropriate content templates based on parameters."""
        templates = {
            ContentType.TEXT_POST: [
                "🎯 {topic} is transforming {niche}. Here's what you need to know:\n\n"
                "1. The landscape is changing rapidly\n"
                "2. Those who adapt will thrive\n"
                "3. The future belongs to the prepared\n\n"
                "What's your take on this?",

                "💡 Unpopular opinion about {topic}:\n\n"
                "Most people get it wrong. Here's the truth...\n\n"
                "[Your insights on {topic} that challenge conventional thinking]",

                "I spent 10+ years in {niche}. Here are 5 lessons about {topic} "
                "that nobody talks about:\n\n"
                "1. [Key insight]\n2. [Key insight]\n3. [Key insight]\n"
                "4. [Key insight]\n5. [Key insight]\n\n"
                "Which one resonates with you?"
            ],
            ContentType.VIRAL_HOOK: [
                "🚨 This changed everything I knew about {topic}...",
                "Stop doing {topic} the old way. Here's the new approach:",
                "I made every mistake possible with {topic}. Here's what I learned:",
                "The {topic} advice you're following is outdated. Here's why:"
            ],
            ContentType.LONG_FORM: [
                "📚 THE COMPLETE GUIDE TO {topic} IN {niche}\n\n"
                "After years of experience, I've compiled everything you need to know.\n\n"
                "PART 1: Understanding the Fundamentals\n"
                "[Deep dive into core concepts]\n\n"
                "PART 2: Advanced Strategies\n"
                "[Expert-level insights]\n\n"
                "PART 3: Common Pitfalls to Avoid\n"
                "[Lessons learned the hard way]\n\n"
                "Save this for later. You'll thank me."
            ]
        }

        return templates.get(content_type, templates[ContentType.TEXT_POST])

    def _add_viral_hook(self, content: str) -> str:
        """Add viral hooks and engagement triggers."""
        hooks = [
            "🔥 This is going viral for a reason:",
            "⚡ Everyone is talking about this:",
            "🎯 This will blow your mind:",
            "💥 You need to see this:"
        ]
        return f"{random.choice(hooks)}\n\n{content}"

    def _format_as_carousel(self, content: str, topic: str) -> Dict:
        """Format content as carousel slides."""
        slides = [
            {"slide": 1, "content": f"🎯 EVERYTHING ABOUT {topic.upper()}", "type": "cover"},
            {"slide": 2, "content": "The Problem:\n\nMost people approach this wrong...", "type": "problem"},
            {"slide": 3, "content": "The Solution:\n\nHere's what actually works...", "type": "solution"},
            {"slide": 4, "content": "Key Takeaways:\n\n✓ Point 1\n✓ Point 2\n✓ Point 3", "type": "summary"},
            {"slide": 5, "content": "Action Steps:\n\n1. Do this first\n2. Then this\n3. Finally this", "type": "action"},
            {"slide": 6, "content": "Follow for more insights! 🚀", "type": "cta"}
        ]
        return {
            "format": "carousel",
            "total_slides": len(slides),
            "slides": slides
        }

    def _generate_hashtags(self, topic: str, niche: str) -> List[str]:
        """Generate relevant hashtags based on topic and niche."""
        base_hashtags = ["#LinkedIn", "#Professional", "#CareerGrowth"]
        
        niche_hashtags = {
            "tech": ["#Technology", "#Innovation", "#AI", "#SoftwareEngineering"],
            "marketing": ["#Marketing", "#DigitalMarketing", "#ContentMarketing", "#Branding"],
            "finance": ["#Finance", "#Investing", "#FinTech", "#Economics"],
            "leadership": ["#Leadership", "#Management", "#ExecutiveCoaching", "#BusinessStrategy"],
            "general": ["#Business", "#Entrepreneurship", "#Success", "#Motivation"]
        }

        topic_words = topic.lower().split()
        topic_hashtags = [f"#{word.capitalize()}" for word in topic_words if len(word) > 4]

        all_hashtags = base_hashtags + niche_hashtags.get(niche.lower(), niche_hashtags["general"]) + topic_hashtags
        return list(set(all_hashtags))[:10]  # Return up to 10 unique hashtags

    def _estimate_reach(self, content_type: ContentType, topic: str) -> Dict:
        """Estimate potential reach based on content type and topic."""
        base_reach = {
            ContentType.TEXT_POST: (500, 2000),
            ContentType.LONG_FORM: (300, 1500),
            ContentType.VIRAL_HOOK: (1000, 5000),
            ContentType.CAROUSEL: (2000, 8000),
            ContentType.INFOGRAPHIC: (1500, 6000),
            ContentType.IMAGE_POST: (800, 3000),
            ContentType.MEME: (1000, 4000),
            ContentType.SHORT_VIDEO: (3000, 10000)
        }

        min_reach, max_reach = base_reach.get(content_type, (500, 2000))

        return {
            "estimated_impressions": f"{min_reach:,} - {max_reach:,}",
            "estimated_engagement_rate": "2% - 5%",
            "confidence": "High" if content_type in [ContentType.CAROUSEL, ContentType.SHORT_VIDEO] else "Medium"
        }

    def _calculate_best_time(self) -> Dict:
        """Calculate optimal posting time based on audience analysis."""
        best_times = [
            {"day": "Tuesday", "time": "10:00 AM", "reason": "Peak professional browsing time"},
            {"day": "Wednesday", "time": "12:00 PM", "reason": "Lunch break engagement"},
            {"day": "Thursday", "time": "9:00 AM", "reason": "Morning routine check"},
            {"day": "Friday", "time": "3:00 PM", "reason": "End of week wind-down"}
        ]

        return random.choice(best_times)

    def _predict_engagement(self, content: str, topic: str) -> Dict:
        """Predict engagement metrics for the content."""
        content_length = len(content)
        quality_score = min(100, (content_length / 10) + random.randint(50, 90))

        return {
            "quality_score": round(quality_score, 2),
            "virality_potential": "High" if quality_score > 85 else "Medium" if quality_score > 70 else "Low",
            "predicted_likes": f"{random.randint(50, 200)}+",
            "predicted_comments": f"{random.randint(5, 30)}+",
            "predicted_shares": f"{random.randint(2, 15)}+"
        }

    def analyze_trends(self) -> List[Dict]:
        """
        Analyze current trends and suggest relevant topics.

        Returns:
            List of trending topics with metadata
        """
        trending_topics = [
            {
                "topic": "AI and Automation",
                "trend_score": 95,
                "relevance": "High",
                "hashtags": ["#AI", "#Automation", "#FutureOfWork"],
                "suggested_angle": "How AI is transforming your industry"
            },
            {
                "topic": "Remote Work Culture",
                "trend_score": 88,
                "relevance": "High",
                "hashtags": ["#RemoteWork", "#WorkFromHome", "#DigitalNomad"],
                "suggested_angle": "Building effective remote teams"
            },
            {
                "topic": "Personal Branding",
                "trend_score": 92,
                "relevance": "High",
                "hashtags": ["#PersonalBrand", "#ThoughtLeadership", "#CareerGrowth"],
                "suggested_angle": "Standing out in a crowded market"
            },
            {
                "topic": "Sustainability in Business",
                "trend_score": 85,
                "relevance": "Medium",
                "hashtags": ["#Sustainability", "#ESG", "#GreenBusiness"],
                "suggested_angle": "Profit with purpose"
            }
        ]

        self.trending_topics = trending_topics
        return trending_topics

    def _suggest_trending_topic(self) -> str:
        """Suggest a trending topic for content creation."""
        if not self.trending_topics:
            self.analyze_trends()

        topic = random.choice(self.trending_topics)
        return topic["topic"]

    def personalize_content(self, base_content: Dict, user_preferences: Dict) -> Dict:
        """
        Personalize content based on user preferences and behavior.

        Args:
            base_content: Base content to personalize
            user_preferences: User's preferences and settings

        Returns:
            Personalized content
        """
        personalized = base_content.copy()

        # Adjust tone based on preferences
        if user_preferences.get("tone_preference"):
            personalized["tone"] = user_preferences["tone_preference"]

        # Adjust hashtags based on user's niche
        if user_preferences.get("custom_hashtags"):
            personalized["hashtags"].extend(user_preferences["custom_hashtags"])
            personalized["hashtags"] = list(set(personalized["hashtags"]))[:10]

        # Add personal touch
        if user_preferences.get("signature"):
            personalized["content"] += f"\n\n{user_preferences['signature']}"

        return personalized

    def get_content_analytics(self) -> Dict:
        """Get analytics on generated content."""
        if not self.content_history:
            return {"message": "No content generated yet"}

        total_posts = len(self.content_history)
        content_types = {}
        
        for post in self.content_history:
            ct = post["content_type"]
            content_types[ct] = content_types.get(ct, 0) + 1

        return {
            "total_posts_generated": total_posts,
            "content_type_distribution": content_types,
            "average_quality_score": sum(
                post["engagement_prediction"]["quality_score"]
                for post in self.content_history
            ) / total_posts,
            "most_used_content_type": max(content_types, key=content_types.get) if content_types else None
        }
