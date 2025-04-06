
import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { UserCircle, DoorOpen, Clock, Shield, LogOut } from 'lucide-react';
import AccessLogsList, { AccessLog } from './AccessLogsList';

// This would be fetched from an API in a real application
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

const Dashboard: React.FC = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const [accessLogs, setAccessLogs] = useState<AccessLog[]>([]);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // In a real app, this would be an API call to fetch access logs
    setAccessLogs(mockAccessLogs);
  }, []);

  const handleSignOut = async () => {
    await signOut();
    navigate('/login');
  };

  // Count of successful and failed access attempts
  const successfulAttempts = accessLogs.filter(log => log.accessGranted).length;
  const failedAttempts = accessLogs.filter(log => !log.accessGranted).length;

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-brand-800">Secure Access Dashboard</h1>
          <p className="text-gray-500">Welcome back, {user?.displayName || 'User'}</p>
        </div>
        <Button variant="outline" onClick={handleSignOut} className="mt-4 md:mt-0">
          <LogOut className="mr-2 h-4 w-4" />
          Sign Out
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid grid-cols-3 w-full max-w-md mx-auto">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="access">Access Points</TabsTrigger>
          <TabsTrigger value="logs">Access Logs</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid gap-6 md:grid-cols-3">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Total Access Points</CardTitle>
                <DoorOpen className="h-4 w-4 text-brand-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">12</div>
                <p className="text-xs text-muted-foreground">
                  3 high security, 9 standard
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Recent Access Attempts</CardTitle>
                <Clock className="h-4 w-4 text-brand-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{accessLogs.length}</div>
                <p className="text-xs text-muted-foreground">
                  In the last 24 hours
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Security Status</CardTitle>
                <Shield className="h-4 w-4 text-brand-500" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">Normal</div>
                <p className="text-xs text-muted-foreground">
                  All systems operational
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="mt-6">
            <AccessLogsList logs={accessLogs.slice(0, 3)} />
          </div>
        </TabsContent>

        <TabsContent value="access">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {['Main Entrance', 'Server Room', 'Executive Office', 'R&D Lab', 'HR Department', 'Finance Department'].map((location, index) => (
              <Card key={index}>
                <CardHeader className="pb-2">
                  <CardTitle>{location}</CardTitle>
                  <CardDescription>
                    {index % 2 === 0 ? 'Standard Security' : 'High Security'}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-4">
                    <div className={`relative w-3 h-3 ${index !== 2 ? 'bg-green-500' : 'bg-amber-500'} rounded-full`}>
                      <span className={`absolute -inset-2 rounded-full ${index !== 2 ? 'bg-green-500' : 'bg-amber-500'} opacity-20 animate-pulse-ring`}></span>
                    </div>
                    <span className="text-sm font-medium">
                      {index !== 2 ? 'Available' : 'Restricted'}
                    </span>
                  </div>
                  <div className="mt-4">
                    <Button variant="outline" size="sm" className="w-full">
                      Request Access
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="logs">
          <AccessLogsList logs={accessLogs} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Dashboard;
