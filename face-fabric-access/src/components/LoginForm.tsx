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
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";

// Zod schema for validation
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
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const handleSubmit = async (data: FormValues) => {
    setLoading(true);
    try {
      const user = await signIn(data.email, data.password);
      if (user) {
        // Fetch user logs from backend
        const response = await fetch("http://127.0.0.1:5000/getUserLogs", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ campusID: data.email }),
        });

        const result = await response.json();

        if (!response.ok) {
          throw new Error(result.error || "Failed to fetch user logs");
        }

        // Format the logs for dashboard and access log display
        const formattedLogs = result.logs?.status?.map((entry: any, index: number) => ({
          campusID: result.logs.campusID,
          name: result.logs.name,
          department: result.logs.department,
          timestamp: new Date(entry.timestamp),
          txID: entry.txID,
          decision: entry.decision,
        })) || [];

        // Navigate to dashboard with the formatted logs
        navigate("/dashboard", {
          state: {
            email: data.email,
            accessLogs: formattedLogs,
          },
        });
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl text-brand-700">Secure Access</CardTitle>
        <CardDescription>Login with your credentials</CardDescription>
      </CardHeader>

      <CardContent>
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
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </Button>
          </form>
        </Form>
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

