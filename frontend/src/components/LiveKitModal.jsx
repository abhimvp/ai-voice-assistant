import { useState, useCallback } from "react";
import { LiveKitRoom, RoomAudioRenderer } from "@livekit/components-react";
import "@livekit/components-styles";
import SimpleVoiceAssistant from "./SimpleVoiceAssistant";

const LiveKitModal = ({ setShowSupport }) => {
  const [isSubmittingName, setIsSubmittingName] = useState(true);
  const [name, setName] = useState("");
  const [token, setToken] = useState(null); // access credentials to connect to this room
  //   In order for us to connect from our frontend to the LiveKit server, we need to have some kind of access credential
  // In prod , backend server that issues us new credentials anytime we want to connect to a room, and then we have complete control who is able to connect.

  const getToken = useCallback(async (userName) => {
    try {
      console.log("run");
      const response = await fetch(
        `/api/getToken?name=${encodeURIComponent(userName)}`
      );
      const token = await response.text();
      setToken(token);
      setIsSubmittingName(false);
    } catch (error) {
      console.error(error);
    }
  }, []);

  const handleNameSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      getToken(name);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="support-room">
          {isSubmittingName ? (
            <form onSubmit={handleNameSubmit} className="name-form">
              <h2>Enter your name to connect with support</h2>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
                required
              />
              <button type="submit">Connect</button>
              <button
                type="button"
                className="cancel-button"
                onClick={() => setShowSupport(false)}
              >
                Cancel
              </button>
            </form>
          ) : token ? (
            // LiveKitRoom is where we can render the audio and we can show all of the liveKit related components
            <LiveKitRoom
              serverUrl={import.meta.env.VITE_LIVEKIT_URL} // import env variable in react this way
              //   token={token}
              //   token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzk5NzI1NTksImlzcyI6IkFQSWdudE888888*********TczOTk3MTY1OSwic3ViIjoiYWJoaSIsInZpZGVvIjp7ImNhblB1Ymxpc2giOnRydWUsImNhblB1Ymxpc2hEYXRhIjp0cnVlLCJjYW5TdWJzY3JpYmUiOnRydWUsInJvb20iOiJyb29tMSIsInJvb21Kb2luIjp0cnVlfX0.0oz9v5AlFDJJgrsQZ6Cw6WCE61hfYou00Jr6ItH7lN8" // temp for testing - lasts for only 900 seconds
              connect={true} // this means that as soon as the room is rendered we're by default going to connect to it.
              video={false} // don't want video
              audio={true} // i need audio
              onDisconnected={() => {
                setShowSupport(false);
                setIsSubmittingName(true);
              }}
            >
              <RoomAudioRenderer />
              <SimpleVoiceAssistant />
            </LiveKitRoom>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default LiveKitModal;
