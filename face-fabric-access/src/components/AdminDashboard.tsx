import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import TransactionLogsList, { TransactionLog } from './TransactionLogsList';
import AccessLogsList, { AccessLog } from './AccessLogsList';

// Dummy blockchain transaction logs data
const mockTransactionLogs: TransactionLog[] = [
  {
    id: 't1',
    transactionId: 'TXN12345',
    amount: 100,
    date: new Date('2025-04-06T09:30:00'),
    status: 'Completed',
    blockNumber: 100001,
    transactionHash: '0xabc123def456'
  },
  {
    id: 't2',
    transactionId: 'TXN12346',
    amount: 250,
    date: new Date('2025-04-06T10:45:00'),
    status: 'Pending',
    blockNumber: 100002,
    transactionHash: '0xdef789abc012'
  },
  {
    id: 't3',
    transactionId: 'TXN12347',
    amount: 75,
    date: new Date('2025-04-06T11:20:00'),
    status: 'Failed',
    blockNumber: 100003,
    transactionHash: '0xghi345jkl678'
  },
  {
    id: 't4',
    transactionId: 'TXN12348',
    amount: 300,
    date: new Date('2025-04-06T12:30:00'),
    status: 'Completed',
    blockNumber: 100004,
    transactionHash: '0xjkl901mno234'
  },
  {
    id: 't5',
    transactionId: 'TXN12349',
    amount: 150,
    date: new Date('2025-04-06T13:45:00'),
    status: 'Completed',
    blockNumber: 100005,
    transactionHash: '0xmno567pqr890'
  }
];

// Dummy access logs data for all users in the organization
const mockAccessLogs: AccessLog[] = [
  {
    id: '1',
    userId: 'user1',
    userName: 'John Doe',
    location: 'Main Entrance',
    timestamp: new Date('2025-04-06T09:15:00'),
    accessGranted: true,
    verificationMethod: 'both'
  },
  {
    id: '2',
    userId: 'user2',
    userName: 'Jane Smith',
    location: 'Server Room',
    timestamp: new Date('2025-04-06T10:30:00'),
    accessGranted: true,
    verificationMethod: 'facial'
  },
  {
    id: '3',
    userId: 'user3',
    userName: 'Bob Johnson',
    location: 'Executive Office',
    timestamp: new Date('2025-04-06T11:45:00'),
    accessGranted: false,
    verificationMethod: 'credential'
  },
  {
    id: '4',
    userId: 'user4',
    userName: 'Alice Williams',
    location: 'R&D Lab',
    timestamp: new Date('2025-04-06T13:20:00'),
    accessGranted: true,
    verificationMethod: 'both'
  },
  {
    id: '5',
    userId: 'user5',
    userName: 'Charlie Brown',
    location: 'HR Department',
    timestamp: new Date('2025-04-06T14:10:00'),
    accessGranted: true,
    verificationMethod: 'facial'
  }
];

const AdminDashboard: React.FC = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const [transactionLogs, setTransactionLogs] = useState<TransactionLog[]>([]);
  const [accessLogs, setAccessLogs] = useState<AccessLog[]>([]);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // In a real app, replace these with API calls to fetch blockchain transactions and access logs
    setTransactionLogs(mockTransactionLogs);
    setAccessLogs(mockAccessLogs);
  }, []);

  const handleSignOut = async () => {
    await signOut();
    navigate('/login');
  };

  // Overview statistics for blockchain transactions
  const totalTransactions = transactionLogs.length;
  const completedTransactions = transactionLogs.filter(tx => tx.status === 'Completed').length;
  const pendingTransactions = transactionLogs.filter(tx => tx.status === 'Pending').length;

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-brand-800">Admin Dashboard</h1>
          <p className="text-gray-500">Welcome back, {user?.displayName || 'Admin'}</p>
        </div>
        <Button variant="outline" onClick={handleSignOut} className="mt-4 md:mt-0">
          <LogOut className="mr-2 h-4 w-4" />
          Sign Out
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid grid-cols-3 w-full max-w-md mx-auto">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="access">Access Logs</TabsTrigger>
          <TabsTrigger value="transactions">Transaction Logs</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid gap-6 md:grid-cols-3">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Total Transactions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalTransactions}</div>
                <p className="text-xs text-muted-foreground">
                  All blockchain transactions recorded
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Successful Transactions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{completedTransactions}</div>
                <p className="text-xs text-muted-foreground">Completed transactions</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Pending Transactions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{pendingTransactions}</div>
                <p className="text-xs text-muted-foreground">
                  Transactions awaiting confirmation
                </p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="access">
          <AccessLogsList logs={accessLogs} />
        </TabsContent>

        <TabsContent value="transactions">
          <TransactionLogsList logs={transactionLogs} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdminDashboard;


