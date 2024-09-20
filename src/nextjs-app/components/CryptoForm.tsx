// import React, { useState } from 'react';
// import axios from 'axios';

// interface CryptoFormProps {
//   onPrediction: (imageUrl: string, predictions: string[]) => void;
// }

// const CryptoForm: React.FC<CryptoFormProps> = ({ onPrediction }) => {
//   const [crypto, setCrypto] = useState('BTC-USD');
//   const [loading, setLoading] = useState(false);

//   const handlePredict = async () => {
//     setLoading(true);
//     try {
//       const response = await axios.post('http://localhost:8000/predict', { crypto });
//       const { imageUrl, predictions } = response.data;
//       onPrediction(imageUrl, predictions);
//     } catch (error) {
//       console.error('Erro ao buscar previsões:', error);
//     }
//     setLoading(false);
//   };

//   return (
//     <div className="p-6 bg-white rounded-lg shadow-md text-black">
//       <h2 className="text-xl font-bold mb-4">Selecione o Criptoativo que voce deseja prever</h2>
//       <select 
//         value={crypto} 
//         onChange={(e) => setCrypto(e.target.value)}
//         className="p-2 border rounded-md mb-4"
//       >
//         <option value="BTC-USD">Bitcoin (BTC-USD)</option>
//         <option value="ETH-USD">Ethereum (ETH-USD)</option>
//         <option value="BNB-USD">Binance Coin (BNB-USD)</option>
//         <option value="ADA-USD">Cardano (ADA-USD)</option>
//       </select>
//       <button 
//         onClick={handlePredict} 
//         disabled={loading}
//         className={`p-2 bg-blue-500 text-white rounded-md ${loading && 'bg-gray-400 cursor-not-allowed'}`}
//       >
//         {loading ? 'Carregando...' : 'Prever'}
//       </button>
//     </div>
//   );
// };

// export default CryptoForm;

import React, { useState } from 'react';
import axios from 'axios';

interface CryptoFormProps {
  onPrediction: (imageUrl: string, predictions: string[]) => void;
  onPredictionProphet: (imageUrl: string, predictions: string[]) => void; // Adicionando a função onPredictionProphet
}

const CryptoForm: React.FC<CryptoFormProps> = ({ onPrediction, onPredictionProphet }) => {
  const [crypto, setCrypto] = useState('BTC-USD');
  const [loading, setLoading] = useState(false);

  const handlePredictLSTM = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/predict', { crypto });
      const { imageUrl, predictions } = response.data;
      onPrediction(imageUrl, predictions);
    } catch (error) {
      console.error('Erro ao buscar previsões:', error);
    }
    setLoading(false);
  };

  const handlePredictProphet = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/predict_prophet', { crypto });
      const { imageUrl, predictions } = response.data;
      onPredictionProphet(imageUrl, predictions);
    } catch (error) {
      console.error('Erro ao buscar previsões Prophet:', error);
    }
    setLoading(false);
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
        className={`p-2 bg-blue-500 text-white rounded-md ${loading && 'bg-gray-400 cursor-not-allowed'}`}
      >
        {loading ? 'Carregando...' : 'Prever com LSTM'}
      </button>

      <button 
        onClick={handlePredictProphet} 
        disabled={loading}
        className={`p-2 bg-green-500 text-white rounded-md ml-4 ${loading && 'bg-gray-400 cursor-not-allowed'}`}
      >
        {loading ? 'Carregando...' : 'Prever com Prophet'}
      </button>
    </div>
  );
};

export default CryptoForm;
