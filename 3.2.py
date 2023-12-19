import os
import heapq
import tkinter as tk
from tkinter import ttk
from functools import partial

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

class HuffmanGUI:
    def __init__(self, root):
        self.huffman_obj = Huffman()
        self.root = root
        self.root.title("Huffman Coding GUI")

        # Create tabs
        self.tabControl = ttk.Notebook(root)
        self.tab_edit = ttk.Frame(self.tabControl)
        self.tab_compress_decompress = ttk.Frame(self.tabControl)
        self.tab_visualize_compressed = ttk.Frame(self.tabControl)
        self.tab_visualize_decompressed = ttk.Frame(self.tabControl)

        # Add tabs to the notebook
        self.tabControl.add(self.tab_edit, text='Edit File')
        self.tabControl.add(self.tab_compress_decompress, text='Compress/Decompress')
        self.tabControl.add(self.tab_visualize_compressed, text='Visualize Compressed')
        self.tabControl.add(self.tab_visualize_decompressed, text='Visualize Decompressed')

        # Set up tabs
        self.setup_edit_tab()
        self.setup_compress_decompress_tab()
        self.setup_visualize_compressed_tab()
        self.setup_visualize_decompressed_tab()

        self.tabControl.pack(expand=1, fill="both")

    def setup_edit_tab(self):
        label = ttk.Label(self.tab_edit, text="Edit 3.2.input.txt file:")
        label.pack(pady=10)

        text_edit = tk.Text(self.tab_edit, wrap=tk.WORD, width=40, height=10)
        text_edit.pack(pady=10)

        save_button = ttk.Button(self.tab_edit, text="Save", command=partial(self.save_file, text_edit))
        save_button.pack(pady=10)

        # Load initial content from the file
        with open("3.2.input.txt", "r") as file:
            content = file.read()
            text_edit.insert("1.0", content)

    def save_file(self, text_widget):
        content = text_widget.get("1.0", tk.END)
        with open("3.2.input.txt", "w") as file:
            file.write(content)

    def setup_compress_decompress_tab(self):
        compress_button = ttk.Button(self.tab_compress_decompress, text="Compress", command=self.compress_file)
        compress_button.grid(row=0, column=0, padx=10, pady=10)

        decompress_button = ttk.Button(self.tab_compress_decompress, text="Decompress", command=self.decompress_file)
        decompress_button.grid(row=0, column=1, padx=10, pady=10)

        # Display default file names
        ttk.Label(self.tab_compress_decompress, text="Input File: 3.2.input.txt").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(self.tab_compress_decompress, text="Compressed File: 3.2.compress.bin").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(self.tab_compress_decompress, text="Decompressed File: 3.2.decompress.txt").grid(row=2, column=0, padx=10, pady=5)

        # Display file sizes
        self.initial_size_label = ttk.Label(self.tab_compress_decompress, text="Initial file size: ")
        self.initial_size_label.grid(row=2, column=1, padx=10, pady=5)

        self.compressed_size_label = ttk.Label(self.tab_compress_decompress, text="Compressed file size: ")
        self.compressed_size_label.grid(row=3, column=1, padx=10, pady=5)

    def compress_file(self):
        self.huffman_obj = Huffman()
        with open("3.2.input.txt", "r") as file:
            text = file.read()

        self.huffman_obj.compress(text, "3.2.compress.bin")
        self.update_file_sizes()
        self.update_visualize_compressed_tab()

    def decompress_file(self):
        self.huffman_obj.decompress("3.2.compress.bin", "3.2.decompress.txt")
        self.update_file_sizes()
        self.update_visualize_decompressed_tab()

    def update_file_sizes(self):
        initial_size = os.path.getsize("3.2.input.txt")
        compressed_size = os.path.getsize("3.2.compress.bin")

        self.initial_size_label.config(text=f"Initial file size: {initial_size} bytes")
        self.compressed_size_label.config(text=f"Compressed file size: {compressed_size} bytes")

    def update_visualize_compressed_tab(self):
        # Destroy the existing text widget
        for widget in self.tab_visualize_compressed.winfo_children():
            widget.destroy()

        # Display content of the compressed file
        with open("3.2.compress.bin", "rb") as file:
            content = file.read()
            text_widget = tk.Text(self.tab_visualize_compressed, wrap=tk.WORD, width=40, height=10)
            text_widget.insert("1.0", content)
            text_widget.pack(pady=10)

    def update_visualize_decompressed_tab(self):
        # Destroy the existing text widget
        for widget in self.tab_visualize_decompressed.winfo_children():
            widget.destroy()

        # Display content of the decompressed file
        with open("3.2.decompress.txt", "r") as file:
            content = file.read()
            text_widget = tk.Text(self.tab_visualize_decompressed, wrap=tk.WORD, width=40, height=10)
            text_widget.insert("1.0", content)
            text_widget.pack(pady=10)

    def setup_visualize_compressed_tab(self):
        # Display content of the compressed file
        with open("3.2.compress.bin", "rb") as file:
            content = file.read()
            text_widget = tk.Text(self.tab_visualize_compressed, wrap=tk.WORD, width=40, height=10)
            text_widget.insert("1.0", content)
            text_widget.pack(pady=10)

    def setup_visualize_decompressed_tab(self):
        # Display content of the decompressed file
        with open("3.2.decompress.txt", "r") as file:
            content = file.read()
            text_widget = tk.Text(self.tab_visualize_decompressed, wrap=tk.WORD, width=40, height=10)
            text_widget.insert("1.0", content)
            text_widget.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()
