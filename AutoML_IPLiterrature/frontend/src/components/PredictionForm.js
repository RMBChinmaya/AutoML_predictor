import React, { useState } from 'react';
import axios from 'axios';

function PredictionForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [output, setOutput] = useState('');

  const onFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await axios.post('http://localhost:5000/predict', formData);
      setOutput(res.data);
    } catch (err) {
      console.error(err);
      // Handle error
    }
  };

  return (
    <div>
      <h2>Prediction Form</h2>
      <form onSubmit={onSubmit}>
        <input type="file" onChange={onFileChange} />
        <button type="submit">Predict</button>
      </form>
      <div>
        <pre>{output}</pre>
      </div>
    </div>
  );
}

export default PredictionForm;
