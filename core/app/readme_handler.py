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


class ReadmeHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_readme(self):
        """
        Load the README file content.

        :return: Content of the README file.
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()

    async def decompile_readme(self, processor):
        """
        Decompile the README file using MarkdownProcessor.

        :param processor: MarkdownProcessor instance.
        :return: Tuple containing the chunks of text and a dictionary with extracted data.
        """
        readme_content = self.load_readme()
        chunks, placeholder_map = processor.decompile_readme(readme_content)
        return chunks, placeholder_map

    @staticmethod
    async def build_readme(translated_chunks, processor):
        """
        Rebuild the translated chunks into a complete translated README content using MarkdownProcessor.

        :param translated_chunks: List of translated text chunks.
        :param processor: MarkdownProcessor instance.
        :return: Translated README content.
        """
        translated_content = processor.build_readme(translated_chunks)
        return translated_content
