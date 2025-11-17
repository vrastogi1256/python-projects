"""
Smart Automation & Posting System
Intelligent posting system with automatic and manual modes, schedule optimization,
and multi-account management.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum


class AutomationMode(Enum):
    """Automation modes."""
    FULLY_AUTOMATIC = "fully_automatic"
    MANUAL_APPROVAL = "manual_approval"
    SCHEDULED = "scheduled"
    HYBRID = "hybrid"


class PostStatus(Enum):
    """Post status types."""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class SmartAutomationSystem:
    """
    Intelligent automation system that handles post scheduling, approval workflows,
    and multi-account management.
    """

    def __init__(
        self,
        mode: AutomationMode = AutomationMode.MANUAL_APPROVAL,
        user_accounts: Optional[List[Dict]] = None
    ):
        """
        Initialize the automation system.

        Args:
            mode: Automation mode
            user_accounts: List of LinkedIn accounts to manage
        """
        self.mode = mode
        self.user_accounts = user_accounts or []
        self.post_queue = []
        self.published_posts = []
        self.pending_approvals = []
        self.schedule_history = []

    def add_post_to_queue(
        self,
        content: Dict,
        account_id: Optional[str] = None,
        schedule_time: Optional[datetime] = None
    ) -> Dict:
        """
        Add a post to the publishing queue.

        Args:
            content: Post content and metadata
            account_id: Specific account to post from
            schedule_time: When to publish (None for immediate)

        Returns:
            Post object with queue information
        """
        post = {
            "id": f"post_{len(self.post_queue) + 1}",
            "content": content,
            "account_id": account_id or self._get_primary_account(),
            "created_at": datetime.now().isoformat(),
            "status": PostStatus.DRAFT.value,
            "schedule_time": schedule_time.isoformat() if schedule_time else None,
            "approval_required": self.mode == AutomationMode.MANUAL_APPROVAL
        }

        if self.mode == AutomationMode.FULLY_AUTOMATIC:
            post["status"] = PostStatus.APPROVED.value
            if not schedule_time:
                schedule_time = self._calculate_optimal_time(content)
                post["schedule_time"] = schedule_time.isoformat()
            post["status"] = PostStatus.SCHEDULED.value
            
        elif self.mode == AutomationMode.MANUAL_APPROVAL:
            post["status"] = PostStatus.PENDING_APPROVAL.value
            self.pending_approvals.append(post)

        self.post_queue.append(post)
        print(f"✅ Post added to queue: {post['id']}")
        print(f"📊 Status: {post['status']}")
        
        return post

    def approve_post(self, post_id: str) -> Dict:
        """
        Approve a pending post.

        Args:
            post_id: ID of the post to approve

        Returns:
            Updated post object
        """
        post = self._find_post(post_id)
        
        if not post:
            return {"error": "Post not found"}

        if post["status"] != PostStatus.PENDING_APPROVAL.value:
            return {"error": f"Post is not pending approval. Current status: {post['status']}"}

        post["status"] = PostStatus.APPROVED.value
        post["approved_at"] = datetime.now().isoformat()

        # Schedule if not already scheduled
        if not post["schedule_time"]:
            schedule_time = self._calculate_optimal_time(post["content"])
            post["schedule_time"] = schedule_time.isoformat()

        post["status"] = PostStatus.SCHEDULED.value

        # Remove from pending approvals
        self.pending_approvals = [p for p in self.pending_approvals if p["id"] != post_id]

        print(f"✅ Post {post_id} approved and scheduled for {post['schedule_time']}")
        return post

    def reject_post(self, post_id: str, reason: Optional[str] = None) -> Dict:
        """
        Reject a pending post.

        Args:
            post_id: ID of the post to reject
            reason: Optional rejection reason

        Returns:
            Result of rejection
        """
        post = self._find_post(post_id)
        
        if not post:
            return {"error": "Post not found"}

        post["status"] = "rejected"
        post["rejected_at"] = datetime.now().isoformat()
        post["rejection_reason"] = reason

        # Remove from queues
        self.post_queue = [p for p in self.post_queue if p["id"] != post_id]
        self.pending_approvals = [p for p in self.pending_approvals if p["id"] != post_id]

        print(f"❌ Post {post_id} rejected")
        return {"status": "rejected", "post_id": post_id}

    def publish_scheduled_posts(self) -> List[Dict]:
        """
        Publish all posts that are due to be published.

        Returns:
            List of published posts
        """
        now = datetime.now()
        published = []

        for post in self.post_queue:
            if post["status"] != PostStatus.SCHEDULED.value:
                continue

            schedule_time = datetime.fromisoformat(post["schedule_time"])
            
            if schedule_time <= now:
                result = self._publish_post(post)
                if result["success"]:
                    published.append(post)

        # Remove published posts from queue
        self.post_queue = [p for p in self.post_queue if p["status"] != PostStatus.PUBLISHED.value]

        if published:
            print(f"📤 Published {len(published)} post(s)")

        return published

    def _publish_post(self, post: Dict) -> Dict:
        """
        Actually publish a post to LinkedIn.

        Args:
            post: Post object to publish

        Returns:
            Result of publishing attempt
        """
        # Simulate publishing
        post["status"] = PostStatus.PUBLISHED.value
        post["published_at"] = datetime.now().isoformat()
        post["post_url"] = f"https://linkedin.com/posts/{post['id']}"
        
        # Add initial metrics
        post["metrics"] = {
            "impressions": 0,
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "profile_views": 0
        }

        self.published_posts.append(post)
        self.schedule_history.append({
            "post_id": post["id"],
            "scheduled_time": post["schedule_time"],
            "published_time": post["published_at"],
            "account_id": post["account_id"]
        })

        print(f"🎉 Successfully published post {post['id']}")
        print(f"🔗 URL: {post['post_url']}")

        return {"success": True, "post": post}

    def _calculate_optimal_time(self, content: Dict) -> datetime:
        """
        Calculate optimal posting time based on content and performance data.

        Args:
            content: Post content

        Returns:
            Optimal datetime to post
        """
        # Analyze historical performance
        best_hours = self._get_best_performing_hours()
        best_days = self._get_best_performing_days()

        now = datetime.now()
        
        # Find next best time slot
        target_hour = best_hours[0] if best_hours else 10  # Default to 10 AM
        target_day = now.weekday()

        # If it's too late today, schedule for tomorrow
        if now.hour >= target_hour:
            target_date = now + timedelta(days=1)
        else:
            target_date = now

        # Adjust to best day of week if needed
        while target_date.weekday() not in best_days:
            target_date += timedelta(days=1)

        optimal_time = target_date.replace(
            hour=target_hour,
            minute=random.randint(0, 59),  # Add randomness
            second=0,
            microsecond=0
        )

        return optimal_time

    def _get_best_performing_hours(self) -> List[int]:
        """Analyze which hours have best performance."""
        # Based on LinkedIn research and historical data
        return [8, 10, 12, 17, 18]  # Best times: morning, lunch, evening

    def _get_best_performing_days(self) -> List[int]:
        """Analyze which days have best performance."""
        # Tuesday to Thursday are typically best for LinkedIn
        return [1, 2, 3]  # Monday=0, Tuesday=1, etc.

    def set_custom_schedule(
        self,
        post_id: str,
        schedule_time: datetime
    ) -> Dict:
        """
        Set a custom schedule time for a post.

        Args:
            post_id: ID of the post
            schedule_time: Custom time to schedule

        Returns:
            Updated post
        """
        post = self._find_post(post_id)
        
        if not post:
            return {"error": "Post not found"}

        post["schedule_time"] = schedule_time.isoformat()
        post["custom_schedule"] = True
        
        if post["status"] == PostStatus.APPROVED.value:
            post["status"] = PostStatus.SCHEDULED.value

        print(f"⏰ Custom schedule set for post {post_id}: {schedule_time}")
        return post

    def add_account(self, account_info: Dict) -> Dict:
        """
        Add a LinkedIn account to manage.

        Args:
            account_info: Account information

        Returns:
            Added account info
        """
        account = {
            "id": f"account_{len(self.user_accounts) + 1}",
            "name": account_info.get("name"),
            "email": account_info.get("email"),
            "profile_url": account_info.get("profile_url"),
            "is_primary": len(self.user_accounts) == 0,  # First account is primary
            "added_at": datetime.now().isoformat(),
            "status": "active"
        }

        self.user_accounts.append(account)
        print(f"✅ Account added: {account['name']} ({account['id']})")
        
        return account

    def get_account_analytics(self, account_id: str) -> Dict:
        """
        Get analytics for a specific account.

        Args:
            account_id: ID of the account

        Returns:
            Analytics data
        """
        account_posts = [p for p in self.published_posts if p["account_id"] == account_id]
        
        if not account_posts:
            return {"message": "No posts for this account yet"}

        total_impressions = sum(p["metrics"]["impressions"] for p in account_posts)
        total_engagement = sum(
            p["metrics"]["likes"] + p["metrics"]["comments"] + p["metrics"]["shares"]
            for p in account_posts
        )

        return {
            "account_id": account_id,
            "total_posts": len(account_posts),
            "total_impressions": total_impressions,
            "total_engagement": total_engagement,
            "average_engagement_rate": f"{(total_engagement / total_impressions * 100):.2f}%" if total_impressions > 0 else "0%",
            "posts_this_week": len([p for p in account_posts if self._is_this_week(p["published_at"])]),
            "posts_this_month": len([p for p in account_posts if self._is_this_month(p["published_at"])])
        }

    def _is_this_week(self, timestamp: str) -> bool:
        """Check if timestamp is within current week."""
        post_date = datetime.fromisoformat(timestamp)
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        return post_date >= week_start

    def _is_this_month(self, timestamp: str) -> bool:
        """Check if timestamp is within current month."""
        post_date = datetime.fromisoformat(timestamp)
        now = datetime.now()
        return post_date.year == now.year and post_date.month == now.month

    def get_queue_status(self) -> Dict:
        """Get current status of post queue."""
        status_counts = {}
        for post in self.post_queue:
            status = post["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "total_in_queue": len(self.post_queue),
            "status_breakdown": status_counts,
            "pending_approvals": len(self.pending_approvals),
            "scheduled_posts": len([p for p in self.post_queue if p["status"] == PostStatus.SCHEDULED.value]),
            "next_scheduled": self._get_next_scheduled_post()
        }

    def _get_next_scheduled_post(self) -> Optional[Dict]:
        """Get the next post scheduled to be published."""
        scheduled = [p for p in self.post_queue if p["status"] == PostStatus.SCHEDULED.value]
        
        if not scheduled:
            return None

        # Sort by schedule time
        scheduled.sort(key=lambda x: x["schedule_time"])
        
        next_post = scheduled[0]
        return {
            "post_id": next_post["id"],
            "schedule_time": next_post["schedule_time"],
            "account_id": next_post["account_id"]
        }

    def _find_post(self, post_id: str) -> Optional[Dict]:
        """Find a post by ID."""
        for post in self.post_queue:
            if post["id"] == post_id:
                return post
        for post in self.published_posts:
            if post["id"] == post_id:
                return post
        return None

    def _get_primary_account(self) -> str:
        """Get primary account ID."""
        for account in self.user_accounts:
            if account.get("is_primary"):
                return account["id"]
        
        if self.user_accounts:
            return self.user_accounts[0]["id"]
        
        return "default_account"

    def set_automation_mode(self, mode: AutomationMode):
        """Change automation mode."""
        old_mode = self.mode
        self.mode = mode
        print(f"🔄 Automation mode changed from {old_mode.value} to {mode.value}")

    def get_system_status(self) -> Dict:
        """Get overall system status."""
        return {
            "automation_mode": self.mode.value,
            "total_accounts": len(self.user_accounts),
            "queue_status": self.get_queue_status(),
            "total_published": len(self.published_posts),
            "system_health": "operational"
        }


# Need to import random at the top
import random
