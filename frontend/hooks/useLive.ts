// frontend/hooks/useLive.ts
import { useState, useCallback } from 'react';
import { Room, createLocalAudioTrack, LocalAudioTrack } from 'livekit-client';
import type { WarmTransferResponse } from '../services/api';

export function useLive() {
  const [room, setRoom] = useState<Room | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState(false);

  // Local audio track to manage mute/unmute
  const [localAudioTrack, setLocalAudioTrack] = useState<LocalAudioTrack | null>(null);
  const [isMuted, setIsMuted] = useState(false);

  const log = useCallback((message: string) => {
    setLogs((prev) => [...prev, message]);
  }, []);

  const connect = useCallback(
    async (callerToken: string, roomName: string) => {
      setLoading(true);
      const newRoom = new Room();

      newRoom.on('connected', () => log(`Connected to LiveKit room: ${roomName}`));
      newRoom.on('disconnected', () => log('Disconnected from LiveKit room'));
      newRoom.on('participantConnected', (participant) => log(`Participant connected: ${participant.identity}`));
      newRoom.on('participantDisconnected', (participant) => log(`Participant disconnected: ${participant.identity}`));

      try {
        const livekitUrl = process.env.NEXT_PUBLIC_LIVEKIT_API_URL || 'https://warm-transfer-app-w7ps5kcn.livekit.cloud';
        console.log('Connecting to LiveKit URL:', livekitUrl);
        await newRoom.connect(livekitUrl, callerToken);

        const audioTrack = await createLocalAudioTrack();
        await newRoom.localParticipant.publishTrack(audioTrack);

        setLocalAudioTrack(audioTrack);
        setRoom(newRoom);
      } catch (error: any) {
        log(`Error connecting to room: ${error.message || error}`);
      }
      setLoading(false);
    },
    [log]
  );

  const disconnect = useCallback(() => {
    if (room) {
      room.disconnect();
      setRoom(null);
      log('Disconnected from LiveKit room');
    }
    setLocalAudioTrack(null);
    setIsMuted(false);
  }, [room, log]);

  const toggleMute = useCallback(async () => {
    if (!localAudioTrack) return;

    if (isMuted) {
      await localAudioTrack.unmute();
      setIsMuted(false);
      log('Microphone unmuted');
    } else {
      await localAudioTrack.mute();
      setIsMuted(true);
      log('Microphone muted');
    }
  }, [localAudioTrack, isMuted, log]);

  const startWarmTransfer = useCallback(
    async (data: {
      original_room_id: string;
      agent_a_id: string;
      agent_b_id: string;
      caller_id: string;
    }) => {
      setLoading(true);
      setLogs([]);
      setSummary('');

      try {
        const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000';

        const res: WarmTransferResponse = await fetch(
          `${backendApiUrl}/warm_transfer/initiate`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
          }
        ).then((r) => {
          if (!r.ok) throw new Error(`HTTP ${r.status}`);
          return r.json();
        });

        setSummary(res.summary);
        log(`Warm transfer initiated: new room ${res.new_room_id}`);

        await connect(res.caller_token, res.new_room_id);
      } catch (error: any) {
        log(`Warm transfer failed: ${error.message || error}`);
      }
      setLoading(false);
    },
    [connect, log]
  );

  return {
    room,
    logs,
    summary,
    loading,
    startWarmTransfer,
    disconnect,
    toggleMute,
    isMuted,
  };
}
