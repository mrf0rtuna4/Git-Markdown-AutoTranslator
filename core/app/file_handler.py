"""
MIT License

Copyright (c) 2024 Mr_Fortuna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_file(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()

    async def decompile(self, processor):
        content = self.load_file()
        chunks, placeholder_map = processor.decompile_file(content)
        return chunks, placeholder_map

    @staticmethod
    async def build_file(translated_chunks, processor):
        translated_content = processor.build_file(translated_chunks)
        return translated_content
