// frontend/app/page.tsx
"use client";

import React, { useState } from "react";
import { useLive } from "../hooks/useLive";
import Button from "../components/Buttons";
import Logs from "../components/Logs";
import InputField from "../components/Input";

export default function HomePage() {
  const { logs, summary, loading, startWarmTransfer, disconnect, toggleMute, isMuted, room } = useLive();

  const [originalRoomId, setOriginalRoomId] = useState("");
  const [agentAId, setAgentAId] = useState("");
  const [agentBId, setAgentBId] = useState("");
  const [callerId, setCallerId] = useState("");

  const handleStartTransfer = () => {
    if (!originalRoomId || !agentAId || !agentBId || !callerId) {
      alert("Please fill in all fields");
      return;
    }
    startWarmTransfer({
      original_room_id: originalRoomId,
      agent_a_id: agentAId,
      agent_b_id: agentBId,
      caller_id: callerId,
    });
  };

  return (
    <main className="max-w-xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Warm Transfer Flow</h1>

      <div className="space-y-4 mb-6">
        <InputField label="Original Room ID" value={originalRoomId} onChange={(e) => setOriginalRoomId(e.target.value)} />
        <InputField label="Agent A ID" value={agentAId} onChange={(e) => setAgentAId(e.target.value)} />
        <InputField label="Agent B ID" value={agentBId} onChange={(e) => setAgentBId(e.target.value)} />
        <InputField label="Caller ID" value={callerId} onChange={(e) => setCallerId(e.target.value)} />
      </div>

      <div className="flex space-x-4 mb-6">
        <Button onClick={handleStartTransfer} disabled={loading}>
          {loading ? "Starting Transfer..." : "Start Warm Transfer"}
        </Button>
        <Button onClick={disconnect} disabled={loading} className="bg-red-600 hover:bg-red-700">
          Disconnect
        </Button>
        <Button onClick={toggleMute} disabled={!room}>
          {isMuted ? "Unmute Mic" : "Mute Mic"}
        </Button>
      </div>

      {summary && (
        <section className="mb-6 p-4 border rounded bg-gray-50">
          <h2 className="font-bold mb-2">Call Summary</h2>
          <p>{summary}</p>
        </section>
      )}

      <Logs logs={logs} />
    </main>
  );
}
