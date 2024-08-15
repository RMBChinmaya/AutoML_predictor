import React, { useState } from 'react';
import axios from 'axios';

function UploadForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [supportedColumns, setSupportedColumns] = useState([]);

  const onFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('target', targetColumn);
    formData.append('supported_columns', supportedColumns);

    try {
      const res = await axios.post('http://localhost:5000/upload', formData);
      console.log(res.data);
      // Handle response and navigate to the next step if needed
    } catch (err) {
      console.error(err);
      // Handle error
    }
  };

  return (
    <div>
      <h2>Upload Form</h2>
      <form onSubmit={onSubmit}>
        {/* Form elements for file upload, target column, supported columns */}
        <input type="file" onChange={onFileChange} />
        {/* Other form fields */}
        <button type="submit">Upload and Train</button>
      </form>
    </div>
  );
}

export default UploadForm;
