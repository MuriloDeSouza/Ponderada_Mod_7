import React from 'react';

interface PredictionResultProps {
  imageUrl: string;
  predictions: string[];
}

const PredictionResult: React.FC<PredictionResultProps> = ({ imageUrl, predictions }) => {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md mt-4 text-black">
      <h3 className="text-xl font-bold mb-4">Previsão de Preços</h3>
      <img src={imageUrl} alt="Gráfico de Previsão" className="w-full mb-4" />
      <ul className="list-disc pl-5">
        {predictions.map((prediction, index) => (
          <li key={index} className="mb-2">{prediction}</li>
        ))}
      </ul>
    </div>
  );
};

export default PredictionResult;
