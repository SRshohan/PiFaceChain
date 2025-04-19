import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { useAuth } from "@/context/AuthContext";

const locations = [
  { name: "Main Entrance", approvalEmail: "sohanrahman182@gmail.com"},
  { name: "Server Room", approvalEmail: "itadmin@company.com" },
  { name: "Executive Office", approvalEmail: "execassistant@company.com" },
  { name: "R&D Lab", approvalEmail: "rndadmin@company.com" },
  { name: "HR Department", approvalEmail: "hr@company.com" },
  { name: "Finance Department", approvalEmail: "finance@company.com" },
];

const AccessPoints = () => {
  const { user } = useAuth();

  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState("");
  const [approvalEmail, setApprovalEmail] = useState("");
  const [fromTime, setFromTime] = useState("");
  const [toTime, setToTime] = useState("");
  const [requestStatus, setRequestStatus] = useState<"Pending" | "None">("None");

  const handleOpenRequest = (location: string, email: string) => {
    setSelectedLocation(location);
    setApprovalEmail(email);
    setDialogOpen(true);
    setRequestStatus("None");
  };

  const handleSubmitRequest = async () => {
    const timestamp = new Date().toISOString();
    const payload = {
      campusID: user?.email,
      location: selectedLocation,
      timestamp,
      fromTime,
      toTime,
      approvalEmail,
    };

    try {
      const response = await fetch("http://127.0.0.1:5001/requestAccess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (!response.ok) throw new Error(result.error || "Access request failed");

      // ✅ Set status to "Pending"
      setRequestStatus("Pending");

      alert(`Access request submitted for ${selectedLocation} (${fromTime} - ${toTime})`);
      setDialogOpen(false);
      setFromTime("");
      setToTime("");
    } catch (error) {
      console.error("Request error:", error);
      alert("Failed to submit access request.");
    }
  };

  return (
    <>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {locations.map((loc, index) => (
          <Card key={index}>
            <CardHeader className="pb-2">
              <CardTitle>{loc.name}</CardTitle>
              <CardDescription>
                {index % 2 === 0 ? "Standard Security" : "High Security"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4">
                <div className={`relative w-3 h-3 ${index !== 2 ? "bg-green-500" : "bg-amber-500"} rounded-full`}>
                  <span className={`absolute -inset-2 rounded-full ${index !== 2 ? "bg-green-500" : "bg-amber-500"} opacity-20 animate-pulse-ring`}></span>
                </div>
                <span className="text-sm font-medium">
                  {index !== 2 ? "Available" : "Restricted"}
                </span>
              </div>
              <div className="mt-4">
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full"
                  onClick={() => handleOpenRequest(loc.name, loc.approvalEmail)}
                >
                  Request Access
                </Button>
              </div>
              {requestStatus === "Pending" && selectedLocation === loc.name && (
                <p className="text-sm text-yellow-600 mt-2">Status: Pending</p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Request Access: {selectedLocation}</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium">Your Email</label>
              <Input type="email" value={user?.email} disabled />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">From</label>
                <Input
                  type="time"
                  value={fromTime}
                  onChange={(e) => setFromTime(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">To</label>
                <Input
                  type="time"
                  value={toTime}
                  onChange={(e) => setToTime(e.target.value)}
                  required
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium">Approval Email</label>
              <Input type="email" value={approvalEmail} disabled />
            </div>
          </div>

          <DialogFooter className="pt-4">
            <Button
              onClick={handleSubmitRequest}
              disabled={!fromTime || !toTime}
              className="w-full bg-brand-600 hover:bg-brand-700"
            >
              Submit Access Request
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default AccessPoints;



