import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TrainingProgress() {
  const [trainingOutput, setTrainingOutput] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/training-progress');
        setTrainingOutput(response.data);
      } catch (error) {
        console.error('Error fetching training progress:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>Training Progress</h2>
      <div>
        <pre>{trainingOutput}</pre>
      </div>
    </div>
  );
}

export default TrainingProgress;
