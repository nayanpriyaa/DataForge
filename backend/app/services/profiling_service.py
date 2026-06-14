import pandas as pd


class ProfilingService:

    def profile(
        self,
        file_path
    ):

        df = pd.read_csv(file_path)

        profile = {

            "rows": len(df),

            "columns": len(df.columns),

            "column_names": list(df.columns),

            "data_types": {
                col: str(dtype)
                for col, dtype
                in df.dtypes.items()
            },

            "missing_values": (
                df.isnull()
                .sum()
                .to_dict()
            )
        }

        return profile