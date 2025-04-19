import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { DoorOpen, Clock, Shield, LogOut } from 'lucide-react';
import AccessLogsList, { AccessLog } from './AccessLogsList';
import AccessPoints from './AccessPoints';

const Dashboard: React.FC = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const passedLogs = location.state?.accessLogs || [];
  const userEmail = location.state?.email || user?.email;

  const [accessLogs, setAccessLogs] = useState<AccessLog[]>(passedLogs);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // Only use logs if passed in from Login
    setAccessLogs(passedLogs);
  }, [passedLogs]);

  const handleSignOut = async () => {
    await signOut();
    navigate('/login');
  };

  const successfulAttempts = accessLogs.filter(log => log.accessGranted).length;
  const failedAttempts = accessLogs.filter(log => !log.accessGranted).length;

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-brand-800">Secure Access Dashboard</h1>
          <p className="text-gray-500">Welcome back, {user?.displayName || userEmail || 'User'}</p>
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
          <AccessPoints />
        </TabsContent>

        <TabsContent value="logs">
          <AccessLogsList logs={accessLogs} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Dashboard;
