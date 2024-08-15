import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import UploadForm from './components/UploadForm';
import TrainingProgress from './components/TrainingProgress';
import PredictionForm from './components/PredictionForm';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={UploadForm} />
        <Route path="/training" component={TrainingProgress} />
        <Route path="/prediction" component={PredictionForm} />
        {/* Add other routes as needed */}
      </Switch>
    </Router>
  );
}

export default App;
