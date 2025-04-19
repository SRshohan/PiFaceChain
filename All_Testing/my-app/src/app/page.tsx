interface LogEntry {
  TxId: string;      // Note the lowercase "d" to match the API response
  Timestamp: Date;   // Adjust the type if the API returns a string timestamp
  Value: any;        // Replace `any` with a more specific type if known
}

interface GetUserLogsResponse {
  logs: LogEntry[];
  message: string;
}


async function fetchAccessLogs(url: string): Promise<GetUserLogsResponse> {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        campusID: '12340',
      }),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data: GetUserLogsResponse = await response.json();
    console.log('Access logs fetched:', data);
    return data;
  } catch (error) {
    console.error('Error fetching access logs:', error);
    // You might return a default shape if needed
    return { logs: [], message: '' };
  }
}

async function printFirstTxID() {
  try {
    const data = await fetchAccessLogs('http://127.0.0.1:5000/getUserLogs');
    if (data.logs.length > 0) {
      console.log(data.logs[0].TxId); // Use TxId as per the API response
    } else {
      console.error('No logs available.');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

printFirstTxID();





