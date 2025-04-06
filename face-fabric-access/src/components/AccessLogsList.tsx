
import React from 'react';
import { 
  Table, 
  TableBody, 
  TableCaption, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow
} from "@/components/ui/table";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { format } from "date-fns";

export interface AccessLog {
  id: string;
  userId: string;
  userName: string;
  location: string;
  timestamp: Date;
  accessGranted: boolean;
  verificationMethod: 'facial' | 'credential' | 'both';
}

interface AccessLogsListProps {
  logs: AccessLog[];
}

const AccessLogsList: React.FC<AccessLogsListProps> = ({ logs }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Access Logs</CardTitle>
        <CardDescription>
          Recent access attempts across the organization
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableCaption>A list of recent access attempts</TableCaption>
          <TableHeader>
            <TableRow>
              {/* <TableHead>User</TableHead> */}
              <TableHead>Location</TableHead>
              <TableHead>Time</TableHead>
              <TableHead>Method</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {logs.map((log) => (
              <TableRow key={log.id}>
                {/* <TableCell className="font-medium">{log.userName}</TableCell> */}
                <TableCell>{log.location}</TableCell>
                <TableCell>{format(log.timestamp, 'MMM d, yyyy h:mm a')}</TableCell>
                <TableCell>
                  {log.verificationMethod === 'facial' && 'Facial Recognition'}
                  {log.verificationMethod === 'credential' && 'Credentials'}
                  {log.verificationMethod === 'both' && 'Facial + Credentials'}
                </TableCell>
                <TableCell>
                  {log.accessGranted ? (
                    <Badge className="bg-green-100 text-green-800">Granted</Badge>
                  ) : (
                    <Badge variant="destructive">Denied</Badge>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default AccessLogsList;
