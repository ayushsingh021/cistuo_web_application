import React, { useEffect, useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Before from "../components/Before/Before";
import After from "../components/After/After";

function Dashboard() {
  const [images, setImages] = useState([]);
  const [refresh, setRefresh] = useState(false);
  const [before, setBefore] = useState([]);
  const [after, setAfter] = useState([]);
  const [count,setCount] = useState(0);


  const onChange = (e) => {
    setImages(Array.from(e.target.files));
  };

  const onSubmitHandler = async (e) => {
    e.preventDefault();

    try {
      const formData = new FormData();
      images.forEach((image) => {
        formData.append("files", image);
      });

      const response = await axios.post(
        "http://localhost:8000/api/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      toast.success("Successfully Uploaded");
      // console.log(response.data.filenames);
      setImages(response.data.filenames);
      // console.log(images[0].name);
      setRefresh((prevRefresh) => !prevRefresh);
      // setTimeout(() => window.location.reload(), 5000)
    } catch (error) {
      console.error(error);
    }
  };

  const onClickhandler = async () =>{
    try {
      const response = await axios.get(
        "http://localhost:8000/api/process_images",
      );
      // console.log();
      setCount(response.data.vehicles_count)
    } catch (error) {
      console.log(error);
    }
  }
  useEffect(() => {
    // This code will execute whenever the refresh state changes
    // Reset the file input to clear the selected images
    async function cloudinaryUpload() {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/upload-images/"
        );

        // console.log(response.data.cloudinary_urls);
        setBefore(response.data.cloudinary_urls);
      } catch (error) {
        console.log(error);
      }
    }

    cloudinaryUpload();

    async function cloudinaryShow() {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/download-images/"
        );

        // console.log(response.data.cloudinary_urls);
        setAfter(response.data.cloudinary_urls);
      } catch (error) {
        console.log(error);
      }
    }

    cloudinaryShow();
    document.getElementById("images").value = "";
    console.log("Component refreshed");
  }, [refresh]);
  console.log(before);

  return (
    <div>
      <main className="w-screen max-w-md px-2 mx-auto mt-10 ">
        <h1 className="text-3xl text-center mt-6 font-bold">
          Upload Multiple Images
        </h1>
        <form onSubmit={onSubmitHandler}>
          <div className="mb-6">
            <p className="text-lg font-semibold">Images</p>
            <fieldset>
              <input
                type="file"
                id="images"
                accept=".jpg, .png, .jpeg"
                multiple
                required
                onChange={onChange}
                className="w-full px-3 py-1.5 bg-white border border-gray-300 rounded transition duration-159 ease-in-out mb-2 focus:bg-white focus:border-slate-600"
              />
            </fieldset>
          </div>
          <button
            type="submit"
            className="w-full text-white uppercase font-medium bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-2 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 active bg-blue-800"
          >
            Upload
          </button>
        </form>
        <button
            onClick={onClickhandler}
            className="w-full text-white uppercase font-medium bg-gradient-to-r from-green-500 via-green-600 to-green-700 hover:bg-gradient-to-br focus:ring-2 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 active bg-green-800"
          >
            Run Script
          </button>
          {/* <h1 className="text-2xl text-center mt-6 font-bold">
            Total Vehicles Count :  {count}
          </h1> */}

        <ToastContainer
          position="top-right"
          autoClose={2000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="dark"
          transition:Bounce
        />
      </main>

      <div  className="grid grid-cols-2 space-x-4">
        <div className="grid grid-cols-1">
          <h1 className="text-3xl text-center mt-6 font-bold">Before</h1>
        {before.map((item) => (
          <Before imageurl={item} />
        ))}
        </div>
        <div className="grid grid-cols-1">
          <h1 className="text-3xl text-center mt-6 font-bold">After</h1>
        {after.map((item) => (
          <After imageurl={item} />
        ))}
        </div>
       
      </div>
    </div>
  );
}

export default Dashboard;
