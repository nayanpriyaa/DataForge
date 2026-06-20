import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

export default function DatasetDetailsPage() {

  const { id } = useParams();

  const [profile, setProfile] =
    useState<any>(null);

  const [quality, setQuality] =
    useState<any>(null);

  const [analytics, setAnalytics] =
    useState<any>(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {

    const loadData =
      async () => {

        try {

          const profileResponse =
            await api.get(
              `/datasets/${id}/profile`
            );

          const qualityResponse =
            await api.get(
              `/datasets/${id}/quality`
            );

          const analyticsResponse =
            await api.get(
              `/datasets/${id}/analytics`
            );

          setProfile(
            profileResponse.data
          );

          setQuality(
            qualityResponse.data
          );

          setAnalytics(
            analyticsResponse.data
          );

        } catch (error) {

          console.error(error);

        } finally {

          setLoading(false);
        }
      };

    loadData();

  }, [id]);

  if (loading) {

    return (

      <div className="p-8">
        Loading...
      </div>

    );
  }

  return (

    <div className="p-8 bg-slate-100 min-h-screen">

      <h1
        className="
          text-4xl
          font-bold
          mb-8
        "
      >
        Dataset Overview
      </h1>

      <div
        className="
          grid
          md:grid-cols-4
          gap-6
          mb-8
        "
      >

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">
            Rows
          </p>
          <h2 className="text-3xl font-bold">
            {analytics?.rows ?? 0}
          </h2>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">
            Columns
          </p>
          <h2 className="text-3xl font-bold">
            {analytics?.columns ?? 0}
          </h2>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">
            Numeric Columns
          </p>
          <h2 className="text-3xl font-bold">
            {
              Object.keys(
                analytics?.numeric_columns || {}
              ).length
            }
          </h2>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-gray-500">
            Datetime Columns
          </p>
          <h2 className="text-3xl font-bold">
            {
              Object.keys(
                analytics?.datetime_columns || {}
              ).length
            }
          </h2>
        </div>

      </div>

      <div
        className="
          grid
          md:grid-cols-2
          gap-6
        "
      >

        <div
          className="
            bg-white
            p-6
            rounded-xl
            shadow
          "
        >

          <h2
            className="
              text-xl
              font-bold
              mb-4
            "
          >
            Quality Summary
          </h2>

          <p>
            Duplicate Rows:
            {" "}
            {quality?.duplicate_rows}
          </p>

          <p className="mt-2">
            Columns With Missing Values:
            {" "}
            {
              Object.values(
                quality?.missing_values || {}
              )
              .filter(
                (value: any) =>
                  value > 0
              )
              .length
            }
          </p>

          <p className="mt-2">
            Outlier Columns:
            {" "}
            {
              Object.keys(
                quality?.outliers || {}
              ).length
            }
          </p>

        </div>

        <div
          className="
            bg-white
            p-6
            rounded-xl
            shadow
          "
        >

          <h2
            className="
              text-xl
              font-bold
              mb-4
            "
          >
            Dataset Profile
          </h2>

          <p>
            Total Columns:
            {" "}
            {profile?.columns}
          </p>

          <p className="mt-2">
            Total Rows:
            {" "}
            {profile?.rows}
          </p>

          <p className="mt-2">
            Column Names:
          </p>

          <div
            className="
              flex
              flex-wrap
              gap-2
              mt-2
            "
          >

            {
              profile?.column_names?.map(
                (
                  column: string
                ) => (

                  <span
                    key={column}
                    className="
                      bg-blue-100
                      px-2
                      py-1
                      rounded
                      text-sm
                    "
                  >
                    {column}
                  </span>

                )
              )
            }

          </div>

        </div>

      </div>

    </div>

  );
}