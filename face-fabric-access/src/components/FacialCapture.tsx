
import React, { useRef, useState, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Camera, RefreshCw } from "lucide-react";

interface FacialCaptureProps {
  onCapture: (imageSrc: string) => void;
  maxPhotos?: number;
}

const FacialCapture: React.FC<FacialCaptureProps> = ({ 
  onCapture, 
  maxPhotos = 3 
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isActive, setIsActive] = useState(false);
  const [captures, setCaptures] = useState<string[]>([]);

  const startCamera = useCallback(async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: "user" } 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      
      setStream(mediaStream);
      setIsActive(true);
    } catch (error) {
      console.error("Error accessing camera:", error);
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setIsActive(false);
  }, [stream]);

  const capturePhoto = useCallback(() => {
    if (videoRef.current && canvasRef.current && isActive) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(video, 0, 0);
        const imageSrc = canvas.toDataURL('image/jpeg');
        
        if (captures.length < maxPhotos) {
          setCaptures(prev => [...prev, imageSrc]);
          onCapture(imageSrc);
        }
        
        if (captures.length + 1 >= maxPhotos) {
          stopCamera();
        }
      }
    }
  }, [isActive, captures, maxPhotos, onCapture, stopCamera]);

  const resetCaptures = useCallback(() => {
    setCaptures([]);
    stopCamera();
  }, [stopCamera]);

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardContent className="p-4">
        <div className="relative aspect-video bg-gray-100 rounded-md overflow-hidden mb-4">
          {isActive ? (
            <video 
              ref={videoRef} 
              autoPlay 
              playsInline 
              muted 
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="absolute inset-0 flex items-center justify-center">
              <Camera className="w-16 h-16 text-gray-400" />
            </div>
          )}
          <canvas ref={canvasRef} className="hidden" />
        </div>
        
        {captures.length > 0 && (
          <div className="grid grid-cols-3 gap-2 mb-4">
            {captures.map((src, index) => (
              <div key={index} className="aspect-square rounded-md overflow-hidden">
                <img 
                  src={src} 
                  alt={`Capture ${index + 1}`} 
                  className="w-full h-full object-cover"
                />
              </div>
            ))}
            {Array(maxPhotos - captures.length).fill(0).map((_, index) => (
              <div 
                key={`empty-${index}`} 
                className="aspect-square bg-gray-100 rounded-md flex items-center justify-center"
              >
                <span className="text-gray-400">+</span>
              </div>
            ))}
          </div>
        )}
        
        <div className="flex space-x-2">
          {!isActive && captures.length < maxPhotos && (
            <Button onClick={startCamera} className="flex-1">
              <Camera className="mr-2 h-4 w-4" />
              {captures.length === 0 ? 'Start Camera' : 'Continue Capturing'}
            </Button>
          )}
          
          {isActive && (
            <Button onClick={capturePhoto} className="flex-1 bg-brand-600 hover:bg-brand-700">
              Capture Photo {captures.length + 1}/{maxPhotos}
            </Button>
          )}
          
          {captures.length > 0 && (
            <Button 
              variant="outline" 
              onClick={resetCaptures} 
              className="flex-1"
            >
              <RefreshCw className="mr-2 h-4 w-4" />
              Reset
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default FacialCapture;
