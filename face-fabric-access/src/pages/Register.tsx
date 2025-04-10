
import React from 'react';
import RegisterForm from '@/components/RegisterForm';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useEffect } from 'react';
import { Fingerprint } from 'lucide-react';

const Register = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <div className="mb-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-brand-100 mb-4">
          <Fingerprint className="w-8 h-8 text-brand-600" />
        </div>
        <h1 className="text-3xl font-bold text-brand-800">SecureFace Access</h1>
        <p className="text-gray-500 mt-2">Enterprise Biometric Access Control</p>
      </div>
      <RegisterForm />
    </div>
  );
};

export default Register;
