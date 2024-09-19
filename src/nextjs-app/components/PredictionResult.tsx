import React from 'react';

interface PredictionResultProps {
  imageUrl: string;
  predictions: string[];
}

const PredictionResult: React.FC<PredictionResultProps> = ({ imageUrl, predictions }) => {
  return (
    <div>
      <h3>Previsão de Preços</h3>
      <img src={imageUrl} alt="Gráfico de Previsão" />
      <ul>
        {predictions.map((prediction, index) => (
          <li key={index}>{prediction}</li>
        ))}
      </ul>
    </div>
  );
};

export default PredictionResult;
