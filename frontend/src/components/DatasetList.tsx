import {
  useEffect,
  useState
} from "react";

import {
  Link
} from "react-router-dom";

import api from "../services/api";

type Dataset = {
  id: number;
  filename: string;
  version: number;
  status: string;
};

export default function DatasetList() {

  const [
    datasets,
    setDatasets
  ] = useState<Dataset[]>([]);

  const [
    loading,
    setLoading
  ] = useState(true);

  useEffect(() => {

    const fetchDatasets =
      async () => {

        try {

          const response =
            await api.get(
              "/datasets"
            );

          setDatasets(
            response.data
          );

        } catch (error) {

          console.error(
            "Failed to load datasets",
            error
          );

        } finally {

          setLoading(
            false
          );
        }
      };

    fetchDatasets();

  }, []);

  return (

    <div
      className="
        bg-white
        p-6
        rounded-xl
        shadow
      "
    >

      <h3
        className="
          text-xl
          font-bold
          mb-4
        "
      >
        Datasets
      </h3>

      {

        loading ? (

          <p
            className="
              text-gray-500
            "
          >
            Loading...
          </p>

        ) : datasets.length === 0 ? (

          <p
            className="
              text-gray-500
            "
          >
            No datasets found
          </p>

        ) : (

          datasets.map(
            (
              dataset
            ) => (

              <Link
                key={
                  dataset.id
                }
                to={
                  `/datasets/${dataset.id}`
                }
              >

                <div
                  className="
                    border
                    p-4
                    mb-3
                    rounded-lg
                    hover:bg-gray-50
                    transition
                    cursor-pointer
                  "
                >

                  <p
                    className="
                      font-semibold
                    "
                  >
                    {
                      dataset.filename
                    }
                  </p>

                  <p
                    className="
                      text-sm
                      text-gray-600
                    "
                  >
                    Version:
                    {" "}
                    {
                      dataset.version
                    }
                  </p>

                  <p
                    className="
                      text-sm
                      text-gray-600
                    "
                  >
                    Status:
                    {" "}
                    {
                      dataset.status
                    }
                  </p>

                </div>

              </Link>

            )
          )

        )

      }

    </div>

  );
}