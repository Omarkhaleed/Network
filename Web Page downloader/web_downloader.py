import socket
import tkinter as tk
from tkinter import ttk
import threading
from tkinter import filedialog



class Downloader:
    def __init__(self, url):
        self.url = url
        self.host = self.get_host()
        self.path = self.get_path()

    def get_host(self):
        # Extract the host name from the URL
        return self.url.split('/')[2]

    def get_path(self):
        # Extract the path from the URL
        return '/' + '/'.join(self.url.split('/')[3:])

    def download(self, file_path):
        # Open a TCP socket connection to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {self.host}...")
        s.connect((self.host, 80))
        print(f"Connected to {self.host}.")

        # Send an HTTP GET request to the server
        request = f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\nAccept:text/html\r\n\r\n"
        s.send(request.encode())

        # Receive the response from the server
        response = ''
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data.decode('utf-8', errors='replace')

        # Close the socket connection
        s.close()

        # Save the response to a file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                content = response.split('\r\n\r\n')[1]
                print(f"Writing {len(content)} bytes to file...")
                f.write(content)
                print("File write completed successfully!")
        except Exception as e:
            print(f"Error writing file: {e}")

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x100")
        self.root.title("Web Page Downloader")

        self.url_label = tk.Label(self.root, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()

        self.save_button = tk.Button(self.root, text="Save As", command=self.choose_file)
        self.save_button.pack()

        self.download_button = tk.Button(self.root, text="Save", command=self.download)
        self.download_button.pack()

        self.file_path = None

        self.root.mainloop()

    def choose_file(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".html")
        if self.file_path:
            print(f"Selected file: {self.file_path}")

    def download(self):
        if self.file_path is None:
            print("Please select a file to save the response to.")
            return

        url = self.url_entry.get()
        downloader = Downloader(url)
        t = threading.Thread(target=downloader.download, args=(self.file_path,))
        t.start()
        
    
 

if __name__ == '__main__':
    gui = GUI()
    

