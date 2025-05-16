let mediaRecorder;
let audioChunks = [];

voiceBtn.addEventListener("mousedown", async () => {
  voiceBtn.classList.add("recording");
  audioChunks = [];

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("Your browser does not support audio recording.");
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener("stop", async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      addMessage("You sent a voice note 🎤", "user");

      // Send audio to backend for transcription
      try {
        const response = await fetch("/transcribe", {
          method: "POST",
          body: formData
        });

        const data = await response.json();
        if (data.transcript) {
          addMessage("Transcription: " + data.transcript, "user");

          // Send transcribed text to chat endpoint
          const chatRes = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: data.transcript})
          });
          const chatData = await chatRes.json();
          addMessage(chatData.reply || "Sorry, no reply received.", "bot");
        } else {
          addMessage("Failed to transcribe audio.", "bot");
        }
      } catch (error) {
        addMessage("Error processing voice note.", "bot");
      }
    });
  } catch (err) {
    alert("Microphone permission denied or error: " + err.message);
    voiceBtn.classList.remove("recording");
  }
});

voiceBtn.addEventListener("mouseup", () => {
  voiceBtn.classList.remove("recording");
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
});
