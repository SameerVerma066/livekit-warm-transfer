// frontend/app/page.tsx
"use client";

import React, { useState, useEffect, useRef } from "react";
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

  // Transcript and summary states for speech-to-text
  const [transcript, setTranscript] = useState("");
  const [speechSummary, setSpeechSummary] = useState("");
  const [speechLoading, setSpeechLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Start recording audio
  const handleStartRecording = async () => {
    setTranscript("");
    setSpeechSummary("");
    setIsRecording(true);
    audioChunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const MediaRecorder = window.MediaRecorder;
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      recorder.ondataavailable = (e: BlobEvent) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };
      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await sendAudioToBackend(audioBlob);
      };
      recorder.start();
    } catch (err) {
      setIsRecording(false);
      alert("Microphone access denied or not available.");
    }
  };

  // Stop recording audio
  const handleStopRecording = () => {
    setIsRecording(false);
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  // Send recorded audio to backend and get transcript
  const sendAudioToBackend = async (audioBlob: Blob) => {
    setSpeechLoading(true);
    setTranscript("");
    setSpeechSummary("");
    try {
      const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || "http://localhost:8000";
      const formData = new FormData();
      formData.append("audio", audioBlob, "speech.webm");
      const res = await fetch(`${backendApiUrl}/speech/speech-to-summary`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setTranscript(data.transcript || "No transcript returned.");
      setSpeechSummary(data.summary || "No summary returned.");
    } catch (error) {
      setTranscript("Error generating transcript.");
      setSpeechSummary("");
    }
    setSpeechLoading(false);
  };

  // Request microphone permission on site load
  useEffect(() => {
    async function requestMic() {
      try {
        await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (err) {
        // Optionally handle error
      }
    }
    requestMic();
  }, []);

  // Handler for summarising transcript
  const handleSummarise = async () => {
    if (!transcript) return;
    setSpeechLoading(true);
    setSpeechSummary("");
    try {
      const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || "http://localhost:8000";
      const res = await fetch(`${backendApiUrl}/llm/summary`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setSpeechSummary(data.summary || "No summary returned.");
    } catch (error) {
      setSpeechSummary("Error generating summary.");
    }
    setSpeechLoading(false);
  };

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

      {/* Speech-to-text transcript box, record/stop buttons, and summarise button */}
      <section className="mb-6 p-4 border rounded bg-black">
        <h2 className="font-bold mb-2">Speech Transcript</h2>
        <div className="flex space-x-2 mb-2">
          <Button onClick={handleStartRecording} disabled={isRecording || speechLoading}>
            {isRecording ? "Recording..." : "Record"}
          </Button>
          <Button onClick={handleStopRecording} disabled={!isRecording}>
            Stop
          </Button>
        </div>
        <textarea
          className="w-full p-2 border rounded mb-2"
          rows={4}
          value={transcript}
          onChange={e => setTranscript(e.target.value)}
          placeholder="Converted speech-to-text will appear here..."
        />
        <Button onClick={handleSummarise} disabled={!transcript || speechLoading}>
          {speechLoading ? "Summarising..." : "Summarise"}
        </Button>
        {speechSummary && (
          <div className="mt-4 p-2 border rounded bg-black">
            <h3 className="font-semibold mb-1">Summary</h3>
            <p>{speechSummary}</p>
          </div>
        )}
      </section>

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
