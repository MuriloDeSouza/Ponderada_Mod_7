"use client";
import React, { useState } from 'react';
import CryptoForm from '../components/CryptoForm';
import PredictionResult from '../components/PredictionResult';
// import Link from 'next/link';
// import jsPDF from 'jspdf';

const Home = () => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [predictions, setPredictions] = useState<string[]>([]);

  const [imageUrlProphet, setImageUrlProphet] = useState<string | null>(null);
  const [predictionsProphet, setPredictionsProphet] = useState<string[]>([]);

  const handlePrediction = (imageUrl: string, predictions: string[]) => {
    setImageUrl(imageUrl);
    setPredictions(predictions);
  };

  const handlePredictionProphet = (imageUrl: string, predictions: string[]) => {
    setImageUrlProphet(imageUrl);
    setPredictionsProphet(predictions);
  };

  // const handleGeneratePdf = (filename: string) => {
  //   const doc = new jsPDF();
  //   doc.save(`${filename}.pdf`);
  // }

  // const handlePredictLSTMandPh = (imageUrl: string, predictions: string[]) => {
  //   setImageUrl(imageUrl);
  //   setPredictions(predictions);
  // };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <CryptoForm 
        onPrediction={handlePrediction}
        onPredictionProphet={handlePredictionProphet}
        // onGeneratePdf={handleGeneratePdf}
        // onPredictionLSTMandPh={handlePredictLSTMandPh}
      />
      
      {imageUrl && predictions.length > 0 && (
        <PredictionResult imageUrl={imageUrl} predictions={predictions} />
      )}

      {imageUrlProphet && predictionsProphet.length > 0 && (
        <PredictionResult imageUrl={imageUrlProphet} predictions={predictionsProphet} />
      )}
    </div>
  );
};

export default Home;