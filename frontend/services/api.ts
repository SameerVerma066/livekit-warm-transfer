
export interface WarmTransferRequest {
  original_room_id: string;
  agent_a_id: string;
  agent_b_id: string;
  caller_id: string;
}

export interface WarmTransferResponse {
  new_room_id: string;
  agent_b_token: string;
  caller_token: string;
  summary: string;
  status: string;
}

export async function initiateWarmTransfer(
  data: WarmTransferRequest
): Promise<WarmTransferResponse> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/warm_transfer/initiate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.statusText}`);
  }

  return response.json();
}
