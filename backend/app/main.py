from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import Base
from app.db.database import engine

from app.db.dependencies import get_db

from app.entities.user import User

from app.schemas.user_schema import RegisterRequest
from app.schemas.login_schema import LoginRequest

from app.services.auth_service import AuthService
from app.entities.dataset import Dataset
from fastapi import UploadFile
from fastapi import File

import os

from app.services.upload_service import UploadService
from app.entities.data_profile import DataProfile
from app.services.profile_service import ProfileService
from app.services.profiling_service import ProfilingService
from app.entities.quality_report import QualityReport
from app.services.data_quality_service import DataQualityService
from app.services.quality_service import QualityService
from app.services.dataset_service import DatasetService
from app.services.cleaning_service import CleaningService

from app.schemas.clean_dataset_request import CleanDatasetRequest
from app.entities.dataset_comparison import DatasetComparison
from app.services.analytics_service import AnalyticsService
from app.services.analytics_report_service import (
    AnalyticsReportService
)
from app.entities.analytics_report import AnalyticsReport
from app.core.auth import (
    get_current_user_id
)
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
analytics_service = AnalyticsService()
analytics_report_service = (
    AnalyticsReportService()
)
profile_service = ProfileService()
profiling_service = ProfilingService()
auth_service = AuthService()
upload_service = UploadService()
quality_analysis_service = DataQualityService()
quality_service = QualityService()
dataset_service = DatasetService()
cleaning_service = CleaningService()


@app.post("/register")
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = auth_service.register(
        db=db,
        name=request.name,
        email=request.email,
        password=request.password
    )
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

@app.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    try:

        result = (
            auth_service.login(
                db=db,
                email=request.email,
                password=request.password
            )
        )

        return {
            "access_token":
                result[
                    "access_token"
                ],
            "token_type":
                result[
                    "token_type"
                ]
        }

    except ValueError:

        raise HTTPException(
            status_code=401,
            detail=
                "Invalid email or password"
        )

@app.post("/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(
        get_current_user_id
    )
):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = f"uploads/{file.filename}"

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(content)

    dataset = upload_service.upload(
        db=db,
        filename=file.filename,
        file_path=file_path,
        owner_id=1
    )
    profile = profiling_service.profile(
    file_path
)
    profile_service.save_profile(
    db=db,
    dataset_id=dataset.id,
    profile_json=profile
) 
    quality_report = quality_analysis_service.analyze(
    file_path
)

    quality_service.save_report(
    db=db,
    dataset_id=dataset.id,
    quality_json=quality_report
)

    analytics = (
    analytics_service.analyze(
        file_path
    )
)

    analytics_report_service.save_report(
    db=db,
    dataset_id=dataset.id,
    analytics_json=analytics
)

    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "status": dataset.status
    }

@app.get("/datasets/{dataset_id}/profile")
def get_dataset_profile(
    dataset_id: int,
    db: Session = Depends(get_db)
):

    profile = profile_service.get_profile(
        db,
        dataset_id
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile.profile_json

@app.get("/datasets/{dataset_id}/quality")
def get_dataset_quality(
    dataset_id: int,
    db: Session = Depends(get_db)
):

    report = quality_service.get_report(
        db,
        dataset_id
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Quality report not found"
        )

    return report.quality_json

@app.post("/datasets/{dataset_id}/clean")
def clean_dataset(
    dataset_id: int,
    request: CleanDatasetRequest,
    db: Session = Depends(get_db)
):

    dataset = dataset_service.get_dataset(
        db,
        dataset_id
    )

    if dataset is None:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    latest_dataset = (
        dataset_service.get_latest_version(
            db,
            dataset.filename
        )
    )

    new_version = (
        latest_dataset.version + 1
    )

    cleaned_file_path = (
        f"cleaned/"
        f"{dataset.filename}"
        f"_v{new_version}.csv"
    )

    cleaning_service.clean(
        input_file_path=dataset.file_path,
        output_file_path=cleaned_file_path,
        missing_values_strategy=request.missing_values,
        duplicate_strategy=request.duplicates,
        outlier_strategy=request.outliers
    )

    new_dataset = (
    dataset_service.create_dataset(
        db=db,
        filename=dataset.filename,
        file_path=cleaned_file_path,
        version=new_version,
        owner_id=dataset.owner_id,
        status="cleaned",
        parent_dataset_id=dataset.id
    )
)

    return {
        "dataset_id": new_dataset.id,
        "version": new_dataset.version,
        "status": new_dataset.status
    }

@app.get("/analytics-test")
def analytics_test():

    return analytics_service.analyze(
        "uploads/Chocolate Sales.csv"
    )

@app.get(
    "/datasets/{dataset_id}/analytics"
)
def get_dataset_analytics(
    dataset_id: int,
    db: Session = Depends(get_db)
):

    report = (
        analytics_report_service
        .get_report(
            db,
            dataset_id
        )
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Analytics not found"
        )

    return report.analytics_json

@app.get("/datasets")
def get_datasets(
    db: Session = Depends(get_db)
):

    datasets = (
        dataset_service
        .get_all_datasets(
            db
        )
    )

    return datasets