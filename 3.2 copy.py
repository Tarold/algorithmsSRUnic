import heapq
import os


class Huffman:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class Node:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def makeFrequencyDict(self, text):
        frequency = {}
        for char in text:
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
        return frequency

    def makeHeap(self, frequency):
        for key in frequency:
            node = self.Node(key, frequency[key])
            heapq.heappush(self.heap, node)

    def mergeNodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = self.Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def buildHuffmanCodes(self, node, current_code):
        if node is None:
            return
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_mapping[current_code] = node.char
        self.buildHuffmanCodes(node.left, current_code + "0")
        self.buildHuffmanCodes(node.right, current_code + "1")

    def getEncodedText(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def padEncodedText(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def getByteArray(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            raise ValueError("Encoded text is not properly padded")
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, text, compressed_file):
        frequency = self.makeFrequencyDict(text)
        self.makeHeap(frequency)
        self.mergeNodes()

        root = self.heap[0]
        self.buildHuffmanCodes(root, "")
        encoded_text = self.getEncodedText(text)
        padded_encoded_text = self.padEncodedText(encoded_text)
        byte_array = self.getByteArray(padded_encoded_text)

        with open(compressed_file, "wb") as f:
            f.write(bytes(byte_array))

        print("Compression completed successfully.")

    def decompress(self, input_file, decompressed_file):
        with open(input_file, "rb") as f:
            bit_string = ""
            byte = f.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = f.read(1)
            extra_padding = int(bit_string[:8], 2)
            bit_string = bit_string[8:]
            encoded_text = bit_string[:-1 * extra_padding]

            current_code = ""
            decoded_text = ""
            for bit in encoded_text:
                current_code += bit
                if current_code in self.reverse_mapping:
                    character = self.reverse_mapping[current_code]
                    decoded_text += character
                    current_code = ""
        with open(decompressed_file, "w") as f:
            f.write(decoded_text)
        print("Decompression completed successfully.")


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

class HuffmanApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Huffman Coding")
        
        self.tabControl = ttk.Notebook(self.master)

        # Compression Tab
        self.compress_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.compress_tab, text='Compression')
        self.setup_compress_tab()

        # Decompression Tab
        self.decompress_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.decompress_tab, text='Decompression')
        self.setup_decompress_tab()

        # Edit Input Tab
        self.edit_input_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.edit_input_tab, text='Edit Input')
        self.setup_edit_input_tab()

        self.tabControl.pack(expand=1, fill="both")

    def setup_compress_tab(self):
        self.compress_label = tk.Label(self.compress_tab, text="Select input file:")
        self.compress_label.grid(row=0, column=0, padx=10, pady=10)

        self.compress_entry = tk.Entry(self.compress_tab, state='readonly', width=40)
        self.compress_entry.grid(row=0, column=1, padx=10, pady=10)

        self.compress_button = tk.Button(self.compress_tab, text="Browse", command=self.browse_input_file_compress)
        self.compress_button.grid(row=0, column=2, padx=10, pady=10)

        self.compress_output_label = tk.Label(self.compress_tab, text="Compressed file:")
        self.compress_output_label.grid(row=1, column=0, padx=10, pady=10)

        self.compress_output_entry = tk.Entry(self.compress_tab, state='readonly', width=40)
        self.compress_output_entry.grid(row=1, column=1, padx=10, pady=10)

        self.compress_output_button = tk.Button(self.compress_tab, text="Browse", command=self.browse_output_file_compress)
        self.compress_output_button.grid(row=1, column=2, padx=10, pady=10)

        self.compress_run_button = tk.Button(self.compress_tab, text="Compress", command=self.compress_file)
        self.compress_run_button.grid(row=2, column=1, pady=10)

    def setup_decompress_tab(self):
        self.decompress_label = tk.Label(self.decompress_tab, text="Select compressed file:")
        self.decompress_label.grid(row=0, column=0, padx=10, pady=10)

        self.decompress_entry = tk.Entry(self.decompress_tab, state='readonly', width=40)
        self.decompress_entry.grid(row=0, column=1, padx=10, pady=10)

        self.decompress_button = tk.Button(self.decompress_tab, text="Browse", command=self.browse_input_file_decompress)
        self.decompress_button.grid(row=0, column=2, padx=10, pady=10)

        self.decompress_output_label = tk.Label(self.decompress_tab, text="Decompressed file:")
        self.decompress_output_label.grid(row=1, column=0, padx=10, pady=10)

        self.decompress_output_entry = tk.Entry(self.decompress_tab, state='readonly', width=40)
        self.decompress_output_entry.grid(row=1, column=1, padx=10, pady=10)

        self.decompress_output_button = tk.Button(self.decompress_tab, text="Browse", command=self.browse_output_file_decompress)
        self.decompress_output_button.grid(row=1, column=2, padx=10, pady=10)

        self.decompress_run_button = tk.Button(self.decompress_tab, text="Decompress", command=self.decompress_file)
        self.decompress_run_button.grid(row=2, column=1, pady=10)

    def setup_edit_input_tab(self):
        self.edit_input_label = tk.Label(self.edit_input_tab, text="Edit Input File:")
        self.edit_input_label.grid(row=0, column=0, padx=10, pady=10)

        self.edit_input_text = tk.Text(self.edit_input_tab, wrap='word', height=10, width=50)
        self.edit_input_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.edit_input_button = tk.Button(self.edit_input_tab, text="Save Changes", command=self.save_changes)
        self.edit_input_button.grid(row=2, column=0, pady=10)

        self.load_input_file()

    def browse_input_file_compress(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.compress_entry.configure(state='normal')
            self.compress_entry.delete(0, tk.END)
            self.compress_entry.insert(0, file_path)
            self.compress_entry.configure(state='readonly')

    def browse_output_file_compress(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin")])
        if file_path:
            self.compress_output_entry.configure(state='normal')
            self.compress_output_entry.delete(0, tk.END)
            self.compress_output_entry.insert(0, file_path)
            self.compress_output_entry.configure(state='readonly')

    def browse_input_file_decompress(self):
        file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
        if file_path:
            self.decompress_entry.configure(state='normal')
            self.decompress_entry.delete(0, tk.END)
            self.decompress_entry.insert(0, file_path)
            self.decompress_entry.configure(state='readonly')

    def browse_output_file_decompress(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.decompress_output_entry.configure(state='normal')
            self.decompress_output_entry.delete(0, tk.END)
            self.decompress_output_entry.insert(0, file_path)
            self.decompress_output_entry.configure(state='readonly')

    def compress_file(self):
        input_file = self.compress_entry.get()
        output_file = self.compress_output_entry.get()

        with open(input_file, 'r') as file:
            text = file.read()

        huffman = Huffman()
        huffman.compress(text, output_file)
        self.show_success_message("Compression completed successfully.")

    def decompress_file(self):
        input_file = self.decompress_entry.get()
        output_file = self.decompress_output_entry.get()

        huffman = Huffman()
        huffman.decompress(input_file, output_file)
        self.show_success_message("Decompression completed successfully.")

    def save_changes(self):
        input_text = self.edit_input_text.get("1.0", tk.END)
        with open("3.2.input.txt", 'w') as file:
            file.write(input_text)
        self.show_success_message("Changes saved successfully.")

    def load_input_file(self):
        try:
            with open("3.2.input.txt", 'r') as file:
                text = file.read()
                self.edit_input_text.insert(tk.END, text)
        except FileNotFoundError:
            pass

    def show_success_message(self, message):
        success_window = tk.Toplevel(self.master)
        success_window.title("Success")
        tk.Label(success_window, text=message).pack(padx=20, pady=20)
        tk.Button(success_window, text="OK", command=success_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
