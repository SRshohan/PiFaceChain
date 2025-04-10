
import React, { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useAuth } from "@/context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import FacialCapture from "./FacialCapture";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const formSchema = z.object({
  email: z.string().email({
    message: "Please enter a valid email address.",
  }),
  password: z.string().min(1, {
    message: "Password is required.",
  }),
});

type FormValues = z.infer<typeof formSchema>;

const LoginForm = () => {
  const [activeTab, setActiveTab] = useState("credentials");
  const [faceImage, setFaceImage] = useState<string | null>(null);
  const { signIn } = useAuth();
  const navigate = useNavigate();

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const handleFaceCapture = (imageSrc: string) => {
    setFaceImage(imageSrc);
    // In a real app, here we would verify the facial biometric with the backend
  };

  const handleSubmit = async (data: FormValues) => {
    try {
      const user = await signIn(data.email, data.password);
      if (user) {
        // For a full implementation, we would verify both password and facial
        // biometrics before granting access
        if (activeTab === "credentials" || faceImage) {
          navigate("/dashboard");
        } else {
          setActiveTab("biometrics");
        }
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl text-brand-700">Secure Access</CardTitle>
        <CardDescription>
          Login with your credentials and facial verification
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="credentials">Credentials</TabsTrigger>
            <TabsTrigger value="biometrics">Face Verification</TabsTrigger>
          </TabsList>

          <TabsContent value="credentials">
            <Form {...form}>
              <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input placeholder="john.doe@company.com" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <Input type="password" placeholder="********" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <Button 
                  type="submit" 
                  className="w-full bg-brand-600 hover:bg-brand-700"
                >
                  Continue
                </Button>
              </form>
            </Form>
          </TabsContent>

          <TabsContent value="biometrics">
            <div className="space-y-4">
              <div className="text-sm text-muted-foreground mb-4">
                Please look directly at the camera for facial verification.
              </div>
              
              <FacialCapture onCapture={handleFaceCapture} maxPhotos={1} />
              
              <Button 
                type="button" 
                className="w-full bg-brand-600 hover:bg-brand-700"
                onClick={form.handleSubmit(handleSubmit)}
                disabled={!faceImage}
              >
                Complete Login
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
      <CardFooter className="flex justify-center">
        <div className="text-sm text-muted-foreground">
          Don't have an account?{" "}
          <a href="/register" className="text-brand-600 hover:underline">
            Register
          </a>
        </div>
      </CardFooter>
    </Card>
  );
};

export default LoginForm;
