from sqlalchemy.orm import Session
from app.models.reported_vehicle import ReportedVehicle
from app.schemas.reported_vehicle import ReportedVehicleCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def report_vehicle(
    vehicle_data: ReportedVehicleCreate,
    user_id: int,
    db: Session
) -> dict:
    """Report a vehicle as stolen."""
    try:
        # Check if this vehicle is already reported by the same user
        existing_report = db.query(ReportedVehicle).filter(
            ReportedVehicle.vehicle_no == vehicle_data.vehicle_no,
            ReportedVehicle.vehicle_type == vehicle_data.vehicle_type,
            ReportedVehicle.reported_by == user_id
        ).first()
        
        if existing_report:
            raise HTTPException(
                status_code=400,
                detail="You have already reported this vehicle"
            )
        
        # Check if this vehicle is already reported by someone else
        existing_report_by_others = db.query(ReportedVehicle).filter(
            ReportedVehicle.vehicle_no == vehicle_data.vehicle_no,
            ReportedVehicle.vehicle_type == vehicle_data.vehicle_type
        ).first()
        
        if existing_report_by_others:
            raise HTTPException(
                status_code=400,
                detail="This vehicle has already been reported as stolen"
            )
        
        # Create new reported vehicle record
        new_report = ReportedVehicle(
            vehicle_no=vehicle_data.vehicle_no,
            vehicle_type=vehicle_data.vehicle_type,
            reported_by=user_id
        )
        
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        
        return {
            "message": "Vehicle reported successfully",
            "report_id": new_report.id,
            "vehicle_no": new_report.vehicle_no,
            "reported_at": new_report.reported_at
        }
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Database error occurred while reporting vehicle"
        )
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to report vehicle: {str(e)}"
        )