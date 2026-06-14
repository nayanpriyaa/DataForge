from pydantic import BaseModel


class CleanDatasetRequest(BaseModel):

    missing_values: str

    duplicates: str

    outliers: str