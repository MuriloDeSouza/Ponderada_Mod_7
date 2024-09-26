import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface LogEntry {
  id: number;
  crypto: string;
  model: string;
  timestamp: string;
}

const LogsPage: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    // Faz a requisição para buscar o histórico de previsões
    const fetchLogs = async () => {
      try {
        const response = await axios.get('/api/logs');
        setLogs(response.data);
      } catch (error) {
        console.error('Erro ao buscar logs:', error);
      }
    };

    fetchLogs();
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md text-black">
      <h2 className="text-xl font-bold mb-4">Histórico de Previsões</h2>
      <ul className="list-disc pl-5">
        {logs.length > 0 ? (
          logs.map((logs, index) => (
            <li key={index}>
              <span>{logs.crypto}</span> - <span>{logs.model}</span> - <span>{new Date(logs.timestamp).toLocaleString()}</span>
            </li>
          ))
        ) : (
          <li>Nenhuma previsão gerada até o momento.</li>
        )}
      </ul>
    </div>
  );
};

export default LogsPage;
