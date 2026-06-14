from app.services.cleaning_service import CleaningService

cleaning_service = CleaningService()


@app.post("/datasets/clean")
def clean_dataset():

    result = cleaning_service.clean_missing_values(
        input_file_path="uploads/sales.csv",
        output_file_path="cleaned/cleaned_sales.csv"
    )

    return result