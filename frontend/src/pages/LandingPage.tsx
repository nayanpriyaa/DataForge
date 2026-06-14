import { Link } from "react-router-dom";

export default function LandingPage() {

  return (

    <div
      className="
        min-h-screen
        flex
        flex-col
        items-center
        justify-center
        bg-gray-100
      "
    >

      <h1
        className="
          text-6xl
          font-bold
          mb-6
        "
      >
        DataForge
      </h1>

      <p
        className="
          text-xl
          text-gray-600
          mb-8
        "
      >
        Dataset Analytics & Quality Platform
      </p>

      <div className="flex gap-4">

        <Link
          to="/register"
          className="
            bg-blue-600
            text-white
            px-6
            py-3
            rounded
          "
        >
          Get Started
        </Link>

        <Link
          to="/login"
          className="
            bg-gray-700
            text-white
            px-6
            py-3
            rounded
          "
        >
          Login
        </Link>

      </div>

    </div>
  );
}