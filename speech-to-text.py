import threading
import time

import keyboard
import speech_recognition as sr


class Main:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.listening = True

    def toggle_listener(self):
        print("Press 'ctrl + 0' to toggle on/off")
        while True:
            if keyboard.is_pressed('ctrl+0'):
                self.listening = not self.listening
                print(f"Listener: {'on' if self.listening else 'off'}")

                # Cooldown
                time.sleep(0.5)

    def speech_to_text(self):
        with sr.Microphone() as source:
            print('Adjusting for ambient noise...')
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            listener_thread = threading.Thread(target=self.toggle_listener)
            listener_thread.start()

            while True:
                try:
                    if self.listening:
                        print('Listening...')
                        audio = self.recognizer.listen(
                            source, timeout=1, phrase_time_limit=10
                        )
                        text = self.recognizer.recognize_google(audio)
                        print('Output:', text)
                except sr.UnknownValueError:
                    # Cannot recognize speech
                    pass
                except sr.WaitTimeoutError as e:
                    # Waited too long
                    print(f'Timeout: {e}')
                except sr.RequestError as e:
                    # Some other error occurred with the API
                    print(f'Error with the API request: {e}')
                except KeyboardInterrupt:
                    # Exit the loop if Ctrl+C is pressed
                    break

                # Cooldown
                time.sleep(0.5)

            listener_thread.join()


if __name__ == '__main__':
    test = Main()
    test.speech_to_text()
