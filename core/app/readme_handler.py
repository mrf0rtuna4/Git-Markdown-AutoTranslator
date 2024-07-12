from app.logger import log_info, log_error

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

    async def build_readme(self, translated_chunks, processor):
        """
        Rebuild the translated chunks into a complete translated README content using MarkdownProcessor.

        :param translated_chunks: List of translated text chunks.
        :param processor: MarkdownProcessor instance.
        :return: Translated README content.
        """
        translated_content = processor.build_readme(translated_chunks)
        return translated_content
