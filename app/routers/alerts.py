"""
Alerts and notifications API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session
from app.database import get_db, User, Alert
from app.routers.auth import get_current_user_from_header


router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


# Pydantic models
class AlertCreate(BaseModel):
    title: str
    message: str
    severity: str = "info"  # info, warning, critical
    alert_type: Optional[str] = None
    action_url: Optional[str] = None


class AlertResponse(BaseModel):
    id: int
    title: str
    message: str
    severity: str
    alert_type: Optional[str]
    is_read: bool
    action_url: Optional[str]
    created_at: datetime


@router.get("", response_model=List[AlertResponse])
async def get_alerts(
    unread_only: bool = False,
    limit: int = 50,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get all alerts for current user."""
    query = db.query(Alert).filter(Alert.user_id == current_user.id)

    if unread_only:
        query = query.filter(Alert.is_read == False)

    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()

    return [
        AlertResponse(
            id=a.id,
            title=a.title,
            message=a.message,
            severity=a.severity,
            alert_type=a.alert_type,
            is_read=a.is_read,
            action_url=a.action_url,
            created_at=a.created_at
        )
        for a in alerts
    ]


@router.post("", response_model=AlertResponse)
async def create_alert(
    alert_data: AlertCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Create a new alert."""
    alert = Alert(
        user_id=current_user.id,
        title=alert_data.title,
        message=alert_data.message,
        severity=alert_data.severity,
        alert_type=alert_data.alert_type,
        action_url=alert_data.action_url
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return AlertResponse(
        id=alert.id,
        title=alert.title,
        message=alert.message,
        severity=alert.severity,
        alert_type=alert.alert_type,
        is_read=alert.is_read,
        action_url=alert.action_url,
        created_at=alert.created_at
    )


@router.put("/{alert_id}/read")
async def mark_alert_read(
    alert_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Mark an alert as read."""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_read = True
    db.commit()

    return {"message": "Alert marked as read"}


@router.put("/read-all")
async def mark_all_alerts_read(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Mark all alerts as read."""
    db.query(Alert).filter(
        Alert.user_id == current_user.id,
        Alert.is_read == False
    ).update({"is_read": True})
    db.commit()

    return {"message": "All alerts marked as read"}


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Delete an alert."""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()

    return {"message": "Alert deleted successfully"}


@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get count of unread alerts."""
    count = db.query(Alert).filter(
        Alert.user_id == current_user.id,
        Alert.is_read == False
    ).count()

    return {"unread_count": count}


# Helper function to create system alerts
def create_system_alert(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    severity: str = "info",
    alert_type: str = None
):
    """Create a system alert for a user."""
    alert = Alert(
        user_id=user_id,
        title=title,
        message=message,
        severity=severity,
        alert_type=alert_type
    )
    db.add(alert)
    db.commit()
    return alert
