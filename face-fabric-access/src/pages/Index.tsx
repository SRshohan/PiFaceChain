
import React from 'react';
import { Button } from "@/components/ui/button";
import { useNavigate } from 'react-router-dom';
import { Fingerprint, ShieldCheck, ClipboardList, DoorOpen, Building, UserCheck } from 'lucide-react';

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-b from-brand-800 to-brand-900 text-white">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="flex flex-col items-center text-center md:items-start md:text-left max-w-3xl mx-auto md:mx-0">
            <div className="flex items-center mb-6">
              <Fingerprint className="h-10 w-10 mr-3" />
              <h1 className="text-3xl font-bold">SecureFace Access</h1>
            </div>
            <h2 className="text-4xl md:text-5xl font-bold leading-tight mb-6">
              Enterprise Biometric Access Control
            </h2>
            <p className="text-lg text-gray-200 mb-8 max-w-2xl">
              Secure your organization with facial recognition and blockchain verification. 
              Control physical access to facilities with enterprise-grade biometric security.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                className="bg-white text-brand-800 hover:bg-gray-100"
                size="lg"
                onClick={() => navigate('/login')}
              >
                Sign In
              </Button>
              <Button 
                variant="outline" 
                className="text-black border-white hover:bg-white/10"
                size="lg"
                onClick={() => navigate('/register')}
              >
                Create Account
              </Button>
            </div>
          </div>
        </div>

        {/* Background pattern */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute inset-0 bg-grid-white/5 bg-[length:20px_20px] opacity-20"></div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Enterprise Security Features</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Our platform combines facial biometrics with blockchain verification for 
              unmatched security and auditability.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
              <div className="bg-brand-100 p-3 rounded-lg inline-block mb-4">
                <ShieldCheck className="h-6 w-6 text-brand-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Facial Biometrics</h3>
              <p className="text-gray-600">
                Utilize advanced facial recognition technology for user verification with 
                anti-spoofing measures.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
              <div className="bg-brand-100 p-3 rounded-lg inline-block mb-4">
                <ClipboardList className="h-6 w-6 text-brand-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Blockchain Authentication</h3>
              <p className="text-gray-600">
                Secure, immutable access records stored on Hyperledger Fabric for 
                complete audit trails.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
              <div className="bg-brand-100 p-3 rounded-lg inline-block mb-4">
                <DoorOpen className="h-6 w-6 text-brand-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Access Control</h3>
              <p className="text-gray-600">
                Granular permissions for different access points and security levels 
                throughout your facilities.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
              <div className="bg-brand-100 p-3 rounded-lg inline-block mb-4">
                <Building className="h-6 w-6 text-brand-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Enterprise Management</h3>
              <p className="text-gray-600">
                Comprehensive dashboard for managing users, access points, and 
                security policies.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
              <div className="bg-brand-100 p-3 rounded-lg inline-block mb-4">
                <UserCheck className="h-6 w-6 text-brand-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">User Verification</h3>
              <p className="text-gray-600">
                Multi-factor authentication combining facial biometrics with traditional 
                credentials.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
              <div className="bg-brand-100 p-3 rounded-lg inline-block mb-4">
                <Fingerprint className="h-6 w-6 text-brand-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Biometric Security</h3>
              <p className="text-gray-600">
                Secure storage and handling of biometric data with encryption and 
                privacy controls.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-50 py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to secure your organization?</h2>
          <p className="text-gray-600 max-w-2xl mx-auto mb-8">
            Join the leading companies using SecureFace Access for enterprise security and access control.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Button 
              className="bg-brand-600 hover:bg-brand-700"
              size="lg"
              onClick={() => navigate('/register')}
            >
              Get Started
            </Button>
            <Button 
              variant="outline" 
              className="border-brand-600 text-brand-600 hover:bg-brand-50"
              size="lg"
              onClick={() => navigate('/login')}
            >
              Sign In
            </Button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center mb-6 md:mb-0">
              <Fingerprint className="h-8 w-8 mr-2" />
              <span className="text-xl font-bold">SecureFace Access</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2025 SecureFace Access. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
