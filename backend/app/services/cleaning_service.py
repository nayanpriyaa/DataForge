import pandas as pd
import os


class CleaningService:

    def clean(
        self,
        input_file_path,
        output_file_path,
        missing_values_strategy,
        duplicate_strategy,
        outlier_strategy
    ):

        df = pd.read_csv(
            input_file_path
        )

        #
        # Missing Values
        #

        if missing_values_strategy == "median":

            numeric_columns = (
                df.select_dtypes(
                    include=["number"]
                )
                .columns
            )

            for col in numeric_columns:

                median_value = (
                    df[col]
                    .median()
                )

                df[col] = (
                    df[col]
                    .fillna(
                        median_value
                    )
                )

        #
        # Duplicates
        #

        if duplicate_strategy == "remove":

            df = (
                df
                .drop_duplicates()
            )

        #
        # Outliers
        #

        if outlier_strategy == "remove":

            numeric_columns = (
                df.select_dtypes(
                    include=["number"]
                )
                .columns
            )

            for col in numeric_columns:

                Q1 = (
                    df[col]
                    .quantile(0.25)
                )

                Q3 = (
                    df[col]
                    .quantile(0.75)
                )

                IQR = Q3 - Q1

                lower_bound = (
                    Q1 - 1.5 * IQR
                )

                upper_bound = (
                    Q3 + 1.5 * IQR
                )

                df = df[
                    (df[col] >= lower_bound)
                    &
                    (df[col] <= upper_bound)
                ]

        os.makedirs(
            os.path.dirname(
                output_file_path
            ),
            exist_ok=True
        )

        df.to_csv(
            output_file_path,
            index=False
        )

        return output_file_path