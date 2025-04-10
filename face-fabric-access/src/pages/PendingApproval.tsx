
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { Clock, AlertCircle } from 'lucide-react';

const PendingApproval = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <Clock className="w-16 h-16 text-brand-600" />
              <span className="absolute -top-1 -right-1">
                <span className="flex h-4 w-4">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-4 w-4 bg-brand-500"></span>
                </span>
              </span>
            </div>
          </div>
          <CardTitle className="text-2xl text-center text-brand-800">Approval Pending</CardTitle>
          <CardDescription className="text-center">
            Your account is awaiting administrator approval
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="bg-amber-50 p-4 rounded-md border border-amber-200">
            <div className="flex items-start">
              <AlertCircle className="w-5 h-5 text-amber-600 mr-2 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-amber-800">Account Verification</h3>
                <p className="text-sm text-amber-700 mt-1">
                  Your facial biometric data and account information are being reviewed by an administrator.
                  This process typically takes 1-2 business days.
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="text-sm font-medium">What happens next?</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li className="flex items-start">
                <span className="w-4 h-4 rounded-full bg-brand-100 text-brand-600 flex items-center justify-center text-xs mr-2 mt-0.5">1</span>
                <span>Administrator reviews your registration</span>
              </li>
              <li className="flex items-start">
                <span className="w-4 h-4 rounded-full bg-brand-100 text-brand-600 flex items-center justify-center text-xs mr-2 mt-0.5">2</span>
                <span>Your biometric data is verified and added to the system</span>
              </li>
              <li className="flex items-start">
                <span className="w-4 h-4 rounded-full bg-brand-100 text-brand-600 flex items-center justify-center text-xs mr-2 mt-0.5">3</span>
                <span>You'll receive an email notification when approved</span>
              </li>
            </ul>
          </div>

          <div className="flex flex-col space-y-2">
            <Button 
              onClick={() => navigate('/login')}
              variant="outline"
              className="w-full"
            >
              Return to Login
            </Button>
            <div className="text-xs text-center text-gray-500">
              If you have questions, please contact your system administrator
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PendingApproval;
