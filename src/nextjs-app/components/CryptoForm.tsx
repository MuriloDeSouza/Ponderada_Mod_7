import React, { useState } from 'react';
import axios from 'axios';

interface CryptoFormProps {
  onPrediction: (imageUrl: string, predictions: string[]) => void;
}

const CryptoForm: React.FC<CryptoFormProps> = ({ onPrediction }) => {
  const [crypto, setCrypto] = useState('BTC-USD');
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/predict', { crypto });
      const { imageUrl, predictions } = response.data;
      onPrediction(imageUrl, predictions);
    } catch (error) {
      console.error('Error fetching predictions:', error);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Selecione o Criptoativo</h2>
      <select value={crypto} onChange={(e) => setCrypto(e.target.value)}>
        <option value="BTC-USD">Bitcoin (BTC-USD)</option>
        <option value="ETH-USD">Ethereum (ETH-USD)</option>
        <option value="BNB-USD">Binance Coin (BNB-USD)</option>
      </select>
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Carregando...' : 'Prever'}
      </button>
    </div>
  );
};

export default CryptoForm;
