# app/domain/entities.py
from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel

class PieChartItem(BaseModel):
    category: str
    value: int
    percentage: float

class UserMetrics(BaseModel):
    user_id: str
    shares_count: int
    like_count: int
    positive_comment_count: int
    pie_chart: List[PieChartItem]
    last_updated: datetime

    def to_api_response(self):
        return {
            "userId": self.user_id,
            "metrics": {
                "sharesCount": self.shares_count,
                "likeCount": self.like_count,
                "positiveCommentCount": self.positive_comment_count
            },
            "chartData": {
                "pieChart": [item.dict() for item in self.pie_chart]
            },
            "lastUpdated": self.last_updated.isoformat()
        }