import pandas as pd


class AnalyticsService:

    def analyze(
        self,
        file_path
    ):

        df = pd.read_csv(file_path)

        #
        # Detect Currency Columns
        #

        for col in df.columns:

            if df[col].dtype == "object":

                sample = (
                    df[col]
                    .dropna()
                    .astype(str)
                    .head(10)
                )

                if len(sample) > 0:

                    if sample.str.contains(
                        r"^\$?[\d,]+(\.\d+)?\s*$",
                        regex=True
                    ).all():

                        df[col] = (
                            df[col]
                            .astype(str)
                            .str.replace(
                                "$",
                                "",
                                regex=False
                            )
                            .str.replace(
                                ",",
                                "",
                                regex=False
                            )
                            .str.strip()
                        )

                        df[col] = pd.to_numeric(
                            df[col],
                            errors="coerce"
                        )

        #
        # Detect Date Columns
        #

        datetime_columns = []

        for col in df.columns:

            if df[col].dtype == "object":

                try:

                    converted = pd.to_datetime(
                        df[col],
                        errors="raise"
                    )

                    df[col] = converted

                    datetime_columns.append(col)

                except Exception:

                    pass

        report = {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_columns": {},
            "categorical_columns": {},
            "datetime_columns": {}
        }

        #
        # Numeric Analytics
        #

        numeric_columns = (
            df.select_dtypes(
                include=["number"]
            )
            .columns
        )

        for col in numeric_columns:

            report["numeric_columns"][col] = {

                "mean":
                    float(df[col].mean()),

                "median":
                    float(df[col].median()),

                "min":
                    float(df[col].min()),

                "max":
                    float(df[col].max()),

                "std":
                    float(df[col].std())
                    if not pd.isna(
                        df[col].std()
                    )
                    else 0.0,

                "missing_values":
                    int(
                        df[col]
                        .isnull()
                        .sum()
                    )
            }

        #
        # Datetime Analytics
        #

        for col in datetime_columns:

            report["datetime_columns"][col] = {

                "earliest_date":
                    str(
                        df[col].min()
                    ),

                "latest_date":
                    str(
                        df[col].max()
                    ),

                "unique_dates":
                    int(
                        df[col]
                        .nunique()
                    ),

                "missing_values":
                    int(
                        df[col]
                        .isnull()
                        .sum()
                    )
            }

        #
        # Categorical Analytics
        #

        categorical_columns = []

        for col in df.columns:

            if (
                col not in numeric_columns
                and col not in datetime_columns
            ):

                categorical_columns.append(col)

        for col in categorical_columns:

            mode_values = (
                df[col]
                .mode()
            )

            most_common = (
                str(mode_values.iloc[0])
                if not mode_values.empty
                else None
            )

            report["categorical_columns"][col] = {

                "unique_count":
                    int(
                        df[col]
                        .nunique()
                    ),

                "most_common":
                    most_common,

                "missing_values":
                    int(
                        df[col]
                        .isnull()
                        .sum()
                    )
            }

        return report