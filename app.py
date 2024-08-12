import speech_recognition as sr
import ollama
import pyttsx3

engine = pyttsx3.init()
r = sr.Recognizer()

def listen_and_respond():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Recognize speech using Google Web Speech API
    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
        
        # Check for the skip command
        if text.lower() == "skip":
            print("Exiting the conversation...")
            return False

        # Get the response from the LLaMA model
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': text,
            },
        ])
        
        # Output the response
        response_text = response['message']['content']
        print("Chatbot says: " + response_text)
        
        # Convert the response text to speech
        engine.say(response_text)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error with the request; {0}".format(e))

    return True

def main():
    while True:
        # Check for user input to skip
        user_input = input("Press Enter to ask a question, or type 'skip' to exit: ")
        if user_input.lower() == "skip":
            print("Exiting...")
            break
        
        # Listen and respond
        if not listen_and_respond():
            break

if __name__ == "__main__":
    main()
