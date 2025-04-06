import React from 'react';

export interface TransactionLog {
  id: string;
  transactionId: string;
  amount: number;
  date: Date;
  status: string;
  blockNumber?: number;
  transactionHash?: string;
}

interface TransactionLogsListProps {
  logs: TransactionLog[];
}

const TransactionLogsList: React.FC<TransactionLogsListProps> = ({ logs }) => {
  return (
    <div className="space-y-4">
      {logs.map((log) => (
        <div key={log.id} className="p-4 border rounded shadow-sm">
          <div className="flex justify-between">
            <span className="font-semibold">{log.transactionId}</span>
            <span>{log.status}</span>
          </div>
          <div className="mt-2 text-sm">
            <p>Amount: ${log.amount}</p>
            <p>Date: {log.date.toLocaleString()}</p>
            {log.blockNumber && <p>Block Number: {log.blockNumber}</p>}
            {log.transactionHash && <p>Transaction Hash: {log.transactionHash}</p>}
          </div>
        </div>
      ))}
    </div>
  );
};

export default TransactionLogsList;

