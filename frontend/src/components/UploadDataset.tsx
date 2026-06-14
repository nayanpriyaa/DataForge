import { useState } from "react";
import api from "../services/api";

export default function UploadDataset() {

  const [file, setFile] =
    useState<File | null>(null);

  const upload = async () => {

    if (!file) {
      alert("Select a file");
      return;
    }

    const formData =
      new FormData();

    formData.append(
      "file",
      file
    );

    try {

      const response =
        await api.post(
          "/datasets/upload",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data"
            }
          }
        );

      alert(
        `Dataset uploaded. ID: ${response.data.dataset_id}`
      );

    } catch {

      alert(
        "Upload failed"
      );
    }
  };

  return (

    <div className="bg-white p-6 rounded-xl shadow">

      <h3 className="text-xl font-bold mb-4">
        Upload Dataset
      </h3>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => {

          if (
            e.target.files &&
            e.target.files[0]
          ) {

            setFile(
              e.target.files[0]
            );
          }

        }}
      />

      <button
        onClick={upload}
        className="
          block
          mt-4
          bg-blue-600
          text-white
          px-4
          py-2
          rounded
        "
      >
        Upload
      </button>

    </div>
  );
}