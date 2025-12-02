document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('text-input');
    const speakBtn = document.getElementById('speak-btn');
    const avatarDisplay = document.getElementById('avatar-display');
    const statusIndicator = document.getElementById('status-indicator');

    speakBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        if (!text) return;

        // UI Updates
        speakBtn.disabled = true;
        speakBtn.querySelector('span').textContent = 'Generating Audio...';
        statusIndicator.textContent = 'Generating Audio...';
        statusIndicator.classList.add('processing');

        try {
            // 1. Send text to generate audio
            const response = await fetch('/prepare_audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            // Show TTS Success
            statusIndicator.textContent = 'Audio Generated!';
            statusIndicator.style.color = '#4ade80'; // Green
            await new Promise(r => setTimeout(r, 1000)); // Wait 1s to show status

            // 2. Start streaming video
            statusIndicator.textContent = 'Animating Avatar...';
            statusIndicator.style.color = '#3b82f6'; // Blue
            speakBtn.querySelector('span').textContent = 'Speaking...';

            // Play Audio
            const audio = new Audio(`/get_audio/${data.audio_id}`);
            audio.play();

            // Update the image source to the stream URL
            avatarDisplay.src = `/stream_video?audio_id=${data.audio_id}&t=${Date.now()}`;

            // Reset UI after a delay (approx duration of speech)
            setTimeout(() => {
                speakBtn.disabled = false;
                speakBtn.querySelector('span').textContent = 'Speak';
                statusIndicator.textContent = 'Ready';
                statusIndicator.classList.remove('processing');
                statusIndicator.style.color = '#94a3b8'; // Muted
            }, 8000);

        } catch (error) {
            console.error('Error:', error);
            statusIndicator.textContent = 'Error';
            statusIndicator.style.color = '#ef4444'; // Red
            speakBtn.disabled = false;
            speakBtn.querySelector('span').textContent = 'Speak';
        }
    });
});
