from datetime import datetime
from typing import Any, Dict, Optional

from bson import ObjectId


class DatasetRepository:
    def __init__(self):
        # Mock data storage
        self._datasets = {
            "507f1f77bcf86cd799439011": {
                "_id": ObjectId("507f1f77bcf86cd799439011"),
                "name": "Customer Service Agent Evaluation",
                "examples_by_category": [
                    {
                        "category": "empathy_and_tone",
                        "examples": [
                            {
                                "id": "e1",
                                "user_prompt": "I'm really frustrated. My order was supposed to arrive yesterday and it's still not here. This is the third time this has happened!",
                                "expected_output": "I completely understand your frustration, and I sincerely apologize for the repeated delivery delays. This is definitely not the experience we want you to have. Let me immediately look into your order status and find a solution to make this right for you.",
                            },
                            {
                                "id": "e2",
                                "user_prompt": "I accidentally ordered the wrong size. Can you help me exchange it?",
                                "expected_output": "Of course! I'd be happy to help you with that exchange. Mistakes happen, and we want to make sure you get exactly what you need. Let me walk you through our simple exchange process.",
                            },
                        ],
                    },
                    {
                        "category": "problem_resolution",
                        "examples": [
                            {
                                "id": "e3",
                                "user_prompt": "My subscription was charged twice this month. I need a refund for the duplicate charge.",
                                "expected_output": "I apologize for the billing error. Let me review your account right away. I can see the duplicate charge on [date]. I'll process a refund for the extra charge immediately - you should see it back in your account within 3-5 business days. I'll also ensure this doesn't happen again.",
                            },
                            {
                                "id": "e4",
                                "user_prompt": "The product I received is defective. It stopped working after just two days.",
                                "expected_output": "I'm sorry to hear about the defective product. That's certainly not acceptable, especially after just two days. Let me arrange a replacement for you right away. I can also provide a prepaid return label so you don't have to pay for shipping the defective item back.",
                            },
                        ],
                    },
                    {
                        "category": "information_accuracy",
                        "examples": [
                            {
                                "id": "e5",
                                "user_prompt": "What's your return policy for electronics?",
                                "expected_output": "Our electronics return policy allows returns within 30 days of purchase for a full refund. Items must be in original packaging and working condition. We provide free return shipping labels for defective items, while customer-initiated returns may have a small shipping fee.",
                            },
                            {
                                "id": "e6",
                                "user_prompt": "Do you offer international shipping to Canada?",
                                "expected_output": "Yes, we do ship to Canada! International shipping typically takes 7-14 business days. Shipping costs start at $15, and customers are responsible for any applicable customs duties or taxes upon delivery.",
                            },
                        ],
                    },
                    {
                        "category": "escalation_handling",
                        "examples": [
                            {
                                "id": "e7",
                                "user_prompt": "This is unacceptable! I want to speak to your manager right now! You people have no idea what you're doing!",
                                "expected_output": "I understand you're very upset, and I want to help resolve this situation. While I work to address your concerns directly, I can certainly connect you with my supervisor if you'd prefer. May I first try to understand what's happened so I can work toward a solution?",
                            },
                            {
                                "id": "e8",
                                "user_prompt": "I've been waiting on hold for 45 minutes and nobody has helped me yet. This is ridiculous!",
                                "expected_output": "I sincerely apologize for the long wait time - that's definitely not acceptable, and I understand your frustration. You have my full attention now, and I'm committed to resolving your issue today. What can I help you with?",
                            },
                        ],
                    },
                ],
                "created_at": datetime.fromisoformat("2024-01-20T14:30:00"),
                "updated_at": datetime.fromisoformat("2024-01-20T14:30:00"),
            }
        }

    async def get_dataset_by_id(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        return self._datasets.get(dataset_id)
