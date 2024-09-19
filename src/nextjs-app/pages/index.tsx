import React, { useState } from 'react';
import CryptoForm from '../components/CryptoForm';
import PredictionResult from '../components/PredictionResult';

const Home: React.FC = () => {
  const [imageUrl, setImageUrl] = useState('');
  const [predictions, setPredictions] = useState<string[]>([]);

  const handlePrediction = (imageUrl: string, predictions: string[]) => {
    setImageUrl(imageUrl);
    setPredictions(predictions);
  };

  return (
    <div>
      <h1>Previsão de Preços de Criptoativos</h1>
      <CryptoForm onPrediction={handlePrediction} />
      {imageUrl && <PredictionResult imageUrl={imageUrl} predictions={predictions} />}
    </div>
  );
};

export default Home;
