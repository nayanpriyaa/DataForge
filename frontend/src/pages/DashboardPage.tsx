import { useNavigate } from "react-router-dom";
import UploadDataset from "../components/UploadDataset";
import DatasetList from "../components/DatasetList";
export default function DashboardPage() {

  const navigate =
    useNavigate();

  const logout = () => {

    localStorage.removeItem(
      "token"
    );

    navigate("/");
  };

  return (

    <div className="min-h-screen bg-slate-100">

      <nav className="bg-white shadow px-8 py-4 flex justify-between">

        <h1 className="text-2xl font-bold">
          DataForge
        </h1>

        <button
          onClick={logout}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>

      </nav>

      <div className="p-8">

        <h2 className="text-4xl font-bold mb-8">
          Dashboard
        </h2>

        <div className="grid md:grid-cols-3 gap-6">

          <UploadDataset />

          <DatasetList />

          <div className="bg-white p-6 rounded-xl shadow">
            Quality Reports
          </div>

        </div>

      </div>

    </div>
  );
}