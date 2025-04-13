
import React, { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useAuth } from "@/context/AuthContext";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/components/ui/use-toast";
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
import FacialCapture from "./FacialCapture";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const formSchema = z.object({
  firstName: z.string().min(2, {
    message: "First name must be at least 2 characters.",
  }),
  lastName: z.string().min(2, {
    message: "Last name must be at least 2 characters.",
  }),
  email: z.string().email({
    message: "Please enter a valid email address.",
  }),
  password: z.string().min(8, {
    message: "Password must be at least 8 characters.",
  }),
  employeeId: z.string().min(1, {
    message: "Employee ID is required.",
  }),
  department: z.string().min(1, {
    message: "Department is required.",
  }),
});

type FormValues = z.infer<typeof formSchema>;

const RegisterForm = () => {
  const [activeTab, setActiveTab] = useState("details");
  const [faceImages, setFaceImages] = useState<string[]>([]);
  const { signUp } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      employeeId: "",
      department: "",
    },
  });

  const handleFaceCapture = (imageSrc: string) => {
    setFaceImages((prev) => [...prev, imageSrc]);
    if (faceImages.length === 2) { // If this is the third image (index 2)
      toast({
        title: "Facial capture complete",
        description: "You can now complete your registration.",
      });
    }
  };

  const handleSubmit = async (data: FormValues) => {
    if (faceImages.length < 3) {
      toast({
        variant: "destructive",
        title: "Facial capture required",
        description: "Please complete the facial capture process (3 photos needed).",
      });
      setActiveTab("biometrics");
      return;
    }

    try {
      const displayName = `${data.firstName} ${data.lastName}`;
      const user = await signUp(data.email, data.password, displayName);
      
      if (user) {
        // Here we would store the additional user data and face images
        // to Firebase or your Hyperledger Fabric backend
        // For now, we'll just mock this with a success message
        toast({
          title: "Registration successful",
          description: "Your account has been created and is pending approval.",
        });
        navigate("/pending-approval");
      }
    } catch (error) {
      console.error("Registration error:", error);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl text-brand-700">Create Account</CardTitle>
        <CardDescription>
          Register for secure access with facial biometrics
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="details">Account Details</TabsTrigger>
            <TabsTrigger value="biometrics">Facial Biometrics</TabsTrigger>
          </TabsList>

          <TabsContent value="details">
            <Form {...form}>
              <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="firstName"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>First Name</FormLabel>
                        <FormControl>
                          <Input placeholder="John" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="lastName"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Last Name</FormLabel>
                        <FormControl>
                          <Input placeholder="Doe" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

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

                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="employeeId"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Employee ID</FormLabel>
                        <FormControl>
                          <Input placeholder="EMP1234" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="department"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Department</FormLabel>
                        <FormControl>
                          <Input placeholder="IT" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <Button 
                  type="button" 
                  className="w-full bg-brand-600 hover:bg-brand-700"
                  onClick={() => setActiveTab("biometrics")}
                >
                  Continue to Facial Biometrics
                </Button>
              </form>
            </Form>
          </TabsContent>

          <TabsContent value="biometrics">
            <div className="space-y-4">
              <div className="text-sm text-muted-foreground mb-4">
                Please capture three photos of your face from different angles. 
                These will be used for verifying your identity when accessing 
                secure areas.
              </div>
              
              <FacialCapture onCapture={handleFaceCapture} maxPhotos={3} />
              
              <div className="flex space-x-4">
                <Button 
                  variant="outline" 
                  className="flex-1"
                  onClick={() => setActiveTab("details")}
                >
                  Back to Details
                </Button>
                <Button 
                  type="button" 
                  className="flex-1 bg-brand-600 hover:bg-brand-700"
                  onClick={form.handleSubmit(handleSubmit)}
                  disabled={faceImages.length < 3}
                >
                  Complete Registration
                </Button>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default RegisterForm;