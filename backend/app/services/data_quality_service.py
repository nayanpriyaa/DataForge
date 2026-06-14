import pandas as pd


class DataQualityService:

    def analyze(
        self,
        file_path
    ):

        df = pd.read_csv(file_path)

        outlier_report = {}

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns

        for col in numeric_columns:

            Q1 = df[col].quantile(0.25)

            Q3 = df[col].quantile(0.75)

            IQR = Q3 - Q1

            lower_bound = Q1 - (1.5 * IQR)

            upper_bound = Q3 + (1.5 * IQR)

            outliers = df[
                (df[col] < lower_bound)
                |
                (df[col] > upper_bound)
            ][col].tolist()

            if outliers:
                outlier_report[col] = {
                    "count": len(outliers),
                    "values": outliers
                }

        report = {

            "missing_values":
                df.isnull()
                .sum()
                .to_dict(),

            "duplicate_rows":
                int(
                    df.duplicated()
                    .sum()
                ),

            "outliers":
                outlier_report
        }

        return report