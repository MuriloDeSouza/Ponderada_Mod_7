import React, { useState } from 'react';
import axios from 'axios';

interface CryptoFormProps {
  onPrediction: (imageUrl: string, predictions: string[]) => void;
  onPredictionProphet: (imageUrl: string, predictions: string[]) => void; // Adicionando a função onPredictionProphet
  onGeneratePdf: (filename: string) => void; // Adicionando a função onGeneratePdf
  onPredictionLSTMandPh: (imageUrl: string, predictions: string[]) => void; // Adicionando a função onPredictionLSTMandPh
}

const CryptoForm: React.FC<CryptoFormProps> = ({ onPrediction, onPredictionProphet, onGeneratePdf, onPredictionLSTMandPh }) => {
  const [crypto, setCrypto] = useState('BTC-USD');
  const [loading, setLoading] = useState(false);
  const [showPdfButton, setShowPdfButton] = useState(false);
  const [LstmAndProphet, setLstmAndProphet] = useState(false);

  const handlePredictLSTM = async () => {
    setLoading(true);
    setShowPdfButton(false); // Reseta botão de PDF ao carregar
    try {
      const response = await axios.post('http://localhost:8000/predict', { crypto });
      const { imageUrl, predictions } = response.data;
      onPrediction(imageUrl, predictions);
      setShowPdfButton(true);
    } catch (error) {
      console.error('Erro ao buscar previsões:', error);
    }
    setLoading(false);
  };

  const handlePredictProphet = async () => {
    setLoading(true);
    setShowPdfButton(false); // Reseta botão de PDF ao carregar
    try {
      const response = await axios.post('http://localhost:8000/predict_prophet', { crypto });
      const { imageUrl, predictions } = response.data;
      onPredictionProphet(imageUrl, predictions);
      setShowPdfButton(true);
    } catch (error) {
      console.error('Erro ao buscar previsões Prophet:', error);
    }
    setLoading(false);
  };

  const handlePredictLSTMandPh = async () => {
    setLoading(true);
    setLstmAndProphet(false);
    setShowPdfButton(false); // Reseta botão de PDF ao carregar
    try {
      const response = await axios.post('http://localhost:8000/comparation', { crypto });
      const { imageUrl, predictions } = response.data;
      onPrediction(imageUrl, predictions);
      setLstmAndProphet(true);
      setShowPdfButton(true);
    } catch (error) {
      console.error('Erro ao buscar previsões:', error);
    }
    setLoading(false);
  };
  
  // Parte de gerar PDF
  const handleGeneratePdf = async () => {
    try {
      const response = await axios.post('http://localhost:8000/generate-pdf', { crypto }, { responseType: 'blob' });
      
      if (response.data) {
        const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'report.pdf');
        document.body.appendChild(link);
        link.click();
      }
    } catch (error) {
      console.error('Erro ao gerar PDF:', error);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md text-black">
      <h2 className="text-xl font-bold mb-4">Selecione o Criptoativo que você deseja prever</h2>
      <select 
        value={crypto} 
        onChange={(e) => setCrypto(e.target.value)}
        className="p-2 border rounded-md mb-4"
      >
        <option value="BTC-USD">Bitcoin (BTC-USD)</option>
        <option value="ETH-USD">Ethereum (ETH-USD)</option>
        <option value="BNB-USD">Binance Coin (BNB-USD)</option>
        <option value="ADA-USD">Cardano (ADA-USD)</option>
      </select>
      <button 
        onClick={handlePredictLSTM} 
        disabled={loading}
        className={`p-2 bg-blue-500 text-white rounded-md ${loading ? 'opacity-50' : ''}`}
      >
        {loading ? 'Carregando...' : 'Prever com LSTM'}
      </button>
      <button 
        onClick={handlePredictProphet} 
        disabled={loading}
        className={`p-2 bg-green-500 text-white rounded-md ml-2 ${loading ? 'opacity-50' : ''}`}
      >
        {loading ? 'Carregando...' : 'Prever com Prophet'}
      </button>
      <button 
        onClick={handlePredictLSTMandPh} 
        disabled={loading}
        className={`p-2 bg-yellow-500 text-white rounded-md ml-2 ${LstmAndProphet ? 'opacity-50' : ''}`}
      >
        {LstmAndProphet ? 'Carregando...' : 'Prever com LSTM e Prophet'}
      </button>
    <div>
      <center>
        {showPdfButton && (
          <button 
            onClick={handleGeneratePdf} 
            className="p-2 bg-red-500 text-white rounded-md mt-4"
          >
            Gerar PDF
          </button>
        )}
      </center>
    </div>
    </div>
  );

  
};

export default CryptoForm;
