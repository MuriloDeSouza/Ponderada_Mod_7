"use client";
import React, { useState } from 'react';
import CryptoForm from '../components/CryptoForm';
import PredictionResult from '../components/PredictionResult';

const Home = () => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [predictions, setPredictions] = useState<string[]>([]);

  const handlePrediction = (imageUrl: string, predictions: string[]) => {
    setImageUrl(imageUrl);
    setPredictions(predictions);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <CryptoForm onPrediction={handlePrediction} />
      {imageUrl && predictions.length > 0 && (
        <PredictionResult imageUrl={imageUrl} predictions={predictions} />
      )}
    </div>
  );
};

export default Home;





// "use client";
// import React, { useState } from 'react';
// import CryptoForm from '../components/CryptoForm';
// import PredictionResult from '../components/PredictionResult';

// const Home = () => {
//   const [predictions, setPredictions] = useState<string[]>([]);
//   const [imageUrl, setImageUrl] = useState<string | null>(null);
//   const [crypto, setCrypto] = useState<string>("BTC-USD");  // Estado para o dropdown

//   // Função para enviar a requisição ao FastAPI
//   const predictCrypto = async (crypto: string) => {
//     const response = await fetch("http://localhost:8000/predict", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ crypto }), // Envia o dado como JSON
//     });

//     const data = await response.json();
//     return data;
//   };

//   // Chamada da função no clique
//   const handlePredict = async () => {
//     const result = await predictCrypto(crypto);
//     setPredictions(result.predictions);
//     setImageUrl(result.imageUrl);  // Define o caminho da imagem gerada
//   };

//   return (
//     <div>
//       <h1>Previsão de Criptoativos</h1>
      
//       {/* Dropdown para selecionar o criptoativo */}
//       <select value={crypto} onChange={(e) => setCrypto(e.target.value)}>
//         <option value="BTC-USD">Bitcoin</option>
//         <option value="ETH-USD">Ethereum</option>
//         <option value="BNB-USD">BNB</option>
//       </select>

//       {/* Botão para fazer a previsão */}
//       <button onClick={handlePredict}>Prever</button>

//       {/* Exibe as previsões */}
//       <div>
//         <h2>Previsões:</h2>
//         <ul>
//           {predictions.map((prediction, index) => (
//             <li key={index}>{prediction}</li>
//           ))}
//         </ul>
//       </div>

//       {/* Exibe o gráfico */}
//       {imageUrl && (
//         <div>
//           <h2>Gráfico de Previsão</h2>
//           <img src={imageUrl} alt="Gráfico de Previsão" />
//         </div>
//       )}
//     </div>
//   );
// };

// export default Home;
