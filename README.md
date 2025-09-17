# LiveKit Warm Transfer Project

## Project Overview

This system enables:

- Real-time calls between a caller and Agent A in a LiveKit room.
- Agent A can initiate a warm transfer to Agent B by creating a new LiveKit room.
- Call transcript is captured and summarized via speech-to-text and LLM summarization.
- Call summary and context are shared with Agent B before joining.
- Agent A leaves the original room; Agent B and Caller continue the call in the new room.
- Optional extension with Twilio to bridge calls to real phone/SIP devices.
- Frontend UI in Next.js to operate the flow interactively.

---

## Architectural Components

### 1. Backend (FastAPI)

- **LiveKit Service Layer:**  
  Manage LiveKit API tokens, rooms, and participants.  
  Create and delete rooms, generate join tokens.

- **Warm Transfer Service:**  
  Initiate warm transfer:  
  - Create new LiveKit room.  
  - Generate join tokens for Agent B and Caller.  
  - Retrieve transcript for original room.  
  - Summarize transcript using LLM.  
  - Send summary message to new room.  
  - Remove Agent A from original room.  
  - Return new room ID and tokens.

- **Speech-to-Text and LLM Services:**  
  Accept audio uploads, send to Speech-to-Text API (AssemblyAI).  
  Poll for transcript completion.  
  Pass transcript to LLM service for call summary.  
  Return transcript and summary.

- **API Routes:**  
  Warm transfer initiation route.  
  Speech-to-text + summary route.  
  Optional: routes for Twilio and call management if implemented.

---

### 2. Frontend (Next.js, React)

- **Connection and Audio Management Hook:**  
  Connect/disconnect to LiveKit rooms with tokens.  
  Manage local audio tracks, mute/unmute.  
  Show participant and room events in logs.

- **UI Components:**  
  Input fields for room and participant IDs.  
  Buttons to start warm transfer, disconnect, mute/unmute.  
  Speech-to-text recording UI with recording, stop, and summarize buttons.  
  Display call summary and transcript.  
  Logs display for connection and call events.

- **Warm Transfer Flow:**  
  Agent A fills in caller, agent IDs and original room ID.  
  On transfer initiation:  
  - Call backend warm transfer API.  
  - Receive new room tokens and call summary.  
  - Connect caller client to new room.  
  - Optionally, Agent B connects independently with their token.  
  - Disconnect Agent A from original room.

---

### 3. Speech Recognition Integration

- Use AssemblyAI API:  
  Upload audio bytes.  
  Request transcription using returned upload URL.  
  Poll for transcription completion.  
  Generate summary with LLM service.

- Frontend records audio, sends to backend speech API, displays transcript and summary.

---

### Optional Extensions

- **Twilio Integration to dial phone/SIP:**  
  Bridge LiveKit audio with phone calls.  
  Agent A speaks call summary live.  
  Requires Twilio API backend and frontend UI.

- **State synchronization / signaling for multi-agent coordination.**

---

## Development Steps

1. **Setup Backend:**  
   Configure FastAPI and environment variables.  
   Implement LiveKit service and warm transfer logic.  
   Implement speech-to-text and summary API endpoint.  
   Test with mock data.

2. **Setup Frontend:**  
   Create React hooks (`useLive`) for LiveKit connection.  
   Build warm transfer form UI.  
   Integrate recording and speech-to-text UI.  
   Handle room connect/disconnect flows.  
   Show logs and summaries.

3. **Integrate Third-Party APIs:**  
   AssemblyAI for speech-to-text.  
   OpenAI or custom LLM for summarization.

4. **Testing and Debugging:**  
   Test warm transfer scenarios end-to-end.  
   Validate transcript and summarization flows.  
   Test edge cases and network errors.

5. **Optional Enhancements:**  
   Twilio SIP/phone bridges.  
   Persistent call history and transcripts.  
   Multiple agent support and UI improvements.

---

## Technologies and Tools

- Python FastAPI backend with `httpx` for async API calls.  
- Next.js React frontend with `livekit-client` SDK.  
- AssemblyAI for speech-to-text transcription.  
- OpenAI or custom LLM for text summarization.  
- Env variable management for API keys and URLs.  
- Docker (optional) for containerized deployment.

---

## Challenges Encountered

1. **Token Management and Authorization**  
   - Generating correct LiveKit join tokens for multiple participants (Agent A, Agent B, Caller) with proper permissions.  
   - Ensuring tokens are valid for the right rooms and identities.  
   - Handling token expiration and renewal during long calls or transfers.

2. **Room and Participant Management**  
   - Properly creating, reusing, or deleting LiveKit rooms.  
   - Correctly removing Agent A from the original room after transfer without disrupting call stability.  
   - Synchronizing participant states across multiple clients (agents and caller).  
   - Handling edge cases when participants disconnect unexpectedly.

3. **Audio Streaming and Quality**  
   - Ensuring low-latency, high-quality audio streaming across LiveKit rooms.  
   - Managing local audio tracks, mute/unmute functionality, and audio device permissions.  
   - Handling network fluctuations and reconnections gracefully.

4. **Speech-to-Text Integration**  
   - Uploading audio in supported formats and handling large files efficiently.  
   - Dealing with asynchronous transcription APIs requiring polling for results.  
   - Handling transcription errors, timeouts, or incomplete transcripts.  
   - Ensuring API rate limits and quotas are not exceeded.

5. **Call Summarization with LLMs**  
   - Generating meaningful and concise summaries from noisy/partial transcripts.  
   - Managing API costs and latency of LLM-based summarization.  
   - Handling edge cases such as empty transcripts or ambiguous content.

6. **Frontend/Backend Synchronization**  
   - Synchronizing transfer initiation and participant connection flows smoothly.  
   - Managing UI states during warm transfer transitions.  
   - Handling error feedback and retry mechanisms in UI.

7. **Environment and Configuration Issues**  
   - Securely managing API keys and environment variables.  
   - Ensuring consistent environment setup across development, staging, and production.  
   - Debugging issues due to misconfiguration (e.g., missing URLs, token keys).

8. **Scaling and Performance**  
   - Scaling backend services for concurrent warm transfers.  
   - Handling multiple simultaneous transcription and summarization requests.  
   - Monitoring resource usage and mitigating bottlenecks.

9. **Testing and Debugging**  
   - Simulating multi-agent call scenarios for testing.  
   - Logging and tracing real-time call flows and errors.  
   - Ensuring robustness under failure or network loss conditions.
