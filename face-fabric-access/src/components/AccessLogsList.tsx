import React, { useEffect, useState } from 'react';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { format } from "date-fns";
import { useAuth } from "@/context/AuthContext";

interface AccessLog {
  campusID: string;
  name: string;
  department: string;
  timestamp: Date;
  txID: string;
  decision: string;
}

const AccessLogsList: React.FC = () => {
  const { user } = useAuth();
  const [logs, setLogs] = useState<AccessLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5001/getUserLogs", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ campusID: user?.email }),
        });

        const data = await response.json();
        const profile = data.logs;
        const statusEntries = profile?.status || [];

        const formattedLogs: AccessLog[] = statusEntries.map((entry: any) => ({
          campusID: profile.campusID,
          name: profile.name,
          department: profile.department,
          timestamp: new Date(entry.timestamp),
          txID: entry.txID,
          decision: entry.decision,
        }));

        setLogs(formattedLogs);
      } catch (err) {
        console.error("Failed to fetch logs:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
  }, [user]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Access Logs</CardTitle>
        <CardDescription>
          Recent access decisions with full blockchain context
        </CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <p>Loading logs...</p>
        ) : logs.length === 0 ? (
          <p>No logs found.</p>
        ) : (
          <Table>
            <TableCaption>Access verification records</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Campus ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Timestamp</TableHead>
                <TableHead>TxID</TableHead>
                <TableHead>Decision</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {logs.map((log, idx) => (
                <TableRow key={`${log.txID}-${idx}`}>
                  <TableCell>{log.campusID}</TableCell>
                  <TableCell>{log.name}</TableCell>
                  <TableCell>{log.department}</TableCell>
                  <TableCell>{format(log.timestamp, 'MMM d, yyyy h:mm:ss a')}</TableCell>
                  <TableCell className="break-all">{log.txID}</TableCell>
                  <TableCell>
                    {log.decision === "Granted" ? (
                      <Badge className="bg-green-100 text-green-800">Granted</Badge>
                    ) : (
                      <Badge variant="destructive">Denied</Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
};

export default AccessLogsList;




